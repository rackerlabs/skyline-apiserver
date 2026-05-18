# Copyright 2024 99cloud
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import annotations

import asyncio
import json
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from dateutil import parser as dateparser
from fastapi import APIRouter, Body, Depends, Header, HTTPException, Path, Query, status
from keystoneauth1.session import Session
from novaclient.exceptions import Forbidden as NovaForbidden
from novaclient.exceptions import NotFound as NovaNotFound
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool

from skyline_apiserver import schemas
from skyline_apiserver.api import deps
from skyline_apiserver.client import utils as client_utils
from skyline_apiserver.client.openstack import blazar
from skyline_apiserver.client.utils import generate_session
from skyline_apiserver.log import LOG
from skyline_apiserver.types import constants
from skyline_apiserver.utils.roles import is_system_admin_or_reader

router = APIRouter()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Blazar accepts the literal string "now" in ``start_date`` to mean "the
# current server time". Skyline forwards this literal unchanged and only
# resolves it to a real datetime for the end_date > start_date comparison.
_NOW_LITERAL = "now"

# Precedence used when breaking ties in dominant_type.
# Lower value == higher priority.
_RESOURCE_TYPE_PRIORITY: Dict[str, int] = {
    "physical:host": 0,
    "flavor:instance": 1,
    "virtual:floatingip": 2,
}

# Email regex used to validate ``before_end_notification_emails``.
# The string is comma-separated; each entry is matched individually.
_EMAIL_RE = re.compile(r"^[^@\s,]+@[^@\s,]+\.[^@\s,]+$")

# Cap for the host-allocation fan-out in the calendar route.
_HOST_FANOUT_TIMEOUT = 10.0


# ---------------------------------------------------------------------------
# Wrapper request/response models
# ---------------------------------------------------------------------------


class LeaseCreateRequest(BaseModel):
    """Body of ``POST /reservation/leases`` from the console.

    The console wraps the lease in a ``{"lease": {...}}`` envelope to match
    the Skyline-internal payload shape documented in the design.
    """

    lease: schemas.LeaseCreate = Field(..., description="Lease attributes to create")


class LeaseUpdateRequest(BaseModel):
    """Body of ``PUT /reservation/leases/{lease_id}`` from the console."""

    lease: schemas.LeaseUpdate = Field(..., description="Lease attributes to update")


class LeaseResponse(BaseModel):
    """Wrapped lease forwarded back to the console."""

    lease: Dict[str, Any] = Field(..., description="Lease object returned by Blazar")


class FlavorVisibilityResponse(BaseModel):
    """Result of ``GET /reservation/flavors/{flavor_id}/visibility``."""

    flavor_id: str = Field(..., description="Nova flavor ID that was checked")
    visible: bool = Field(
        ..., description="True when the flavor is visible to the current project."
    )


class FloatingIpsByNetworkResponse(BaseModel):
    """Result of ``GET /reservation/floatingips/by-network/{network_id}``."""

    floatingips: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Blazar-registered floating IPs in the requested Neutron network.",
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _validation_error(loc: List[Any], msg: str) -> HTTPException:
    """Build a single-error 400 response in the FastAPI validation shape."""
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=[{"loc": loc, "msg": msg, "type": "value_error"}],
    )


def _validation_errors(errors: List[Dict[str, Any]]) -> HTTPException:
    """Build a multi-error 400 response in the FastAPI validation shape."""
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors)


def _parse_iso(value: str, loc: List[Any]) -> datetime:
    """Parse an ISO 8601 / Blazar-style timestamp into a UTC ``datetime``.

    Naive timestamps are interpreted as UTC, matching how Blazar treats
    timestamps without an offset. Raises an HTTP 400 ``HTTPException`` when
    parsing fails.
    """
    try:
        parsed = dateparser.parse(value)
    except (ValueError, TypeError, OverflowError) as exc:
        raise _validation_error(loc, f"invalid date: {exc}")
    if parsed is None:
        raise _validation_error(loc, "invalid date")
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _resolve_start_date(start_date: str, loc: List[Any]) -> datetime:
    """Resolve ``start_date`` to a comparable ``datetime`` for validation only.

    The caller still forwards the original string verbatim to Blazar so the
    ``"now"`` literal is preserved end-to-end.
    """
    if start_date.strip().lower() == _NOW_LITERAL:
        return datetime.now(tz=timezone.utc)
    return _parse_iso(start_date, loc)


def _serialize_lease(model: BaseModel) -> Dict[str, Any]:
    """Render a Pydantic lease model as a JSON-safe dict for Blazar.

    ``model.json(exclude_none=True)`` is used so that string enums collapse
    into their value (e.g. ``BeforeEndAction.email -> "email"``) and so that
    optional fields the console did not set are not forwarded.
    """
    return json.loads(model.json(exclude_none=True))


def _dominant_type(reservations: List[Dict[str, Any]]) -> str:
    """Return the dominant Blazar ``resource_type`` for a lease.

    The type that appears most often wins; ties are broken by the fixed
    precedence in ``_RESOURCE_TYPE_PRIORITY`` so the function is deterministic.
    """
    counts: Dict[str, int] = {}
    for reservation in reservations:
        if not isinstance(reservation, dict):
            continue
        rtype = reservation.get("resource_type")
        if not rtype:
            continue
        counts[rtype] = counts.get(rtype, 0) + 1
    if not counts:
        return ""
    return max(
        counts.items(),
        # Higher count first, then lower priority value first for tie-break.
        key=lambda item: (item[1], -_RESOURCE_TYPE_PRIORITY.get(item[0], 99)),
    )[0]


def _resource_type_of(reservation: Any) -> str:
    """Return the ``resource_type`` of a Pydantic reservation variant."""
    rtype = getattr(reservation, "resource_type", None)
    return str(rtype) if rtype is not None else ""


# ---------------------------------------------------------------------------
# Cross-field validators
# ---------------------------------------------------------------------------


def _validate_dates(
    start_date: Optional[str],
    end_date: Optional[str],
    *,
    is_update: bool,
    errors: List[Dict[str, Any]],
) -> None:
    """Validate lease dates.

    On create, both dates are required and ``end_date > resolved(start_date)``
    is enforced. On update, when ``end_date`` is supplied alone the rule is
    ``end_date > now``.
    """
    if start_date is not None and end_date is not None:
        try:
            resolved_start = _resolve_start_date(start_date, ["body", "lease", "start_date"])
            end = _parse_iso(end_date, ["body", "lease", "end_date"])
        except HTTPException as exc:
            if isinstance(exc.detail, list):
                errors.extend(exc.detail)
            else:
                errors.append(
                    {"loc": ["body", "lease"], "msg": str(exc.detail), "type": "value_error"}
                )
            return
        if not (end > resolved_start):
            errors.append(
                {
                    "loc": ["body", "lease", "end_date"],
                    "msg": "end_date must be strictly after start_date",
                    "type": "value_error",
                }
            )
        return

    if is_update and end_date is not None:
        try:
            end = _parse_iso(end_date, ["body", "lease", "end_date"])
        except HTTPException as exc:
            if isinstance(exc.detail, list):
                errors.extend(exc.detail)
            return
        if not (end > datetime.now(tz=timezone.utc)):
            errors.append(
                {
                    "loc": ["body", "lease", "end_date"],
                    "msg": "end_date must be strictly after the current time",
                    "type": "value_error",
                }
            )


def _validate_host_min_max(
    reservations: List[Any],
    errors: List[Dict[str, Any]],
) -> None:
    """Enforce ``1 <= min <= max`` for host reservations."""
    for index, reservation in enumerate(reservations):
        if _resource_type_of(reservation) != "physical:host":
            continue
        host = reservation  # type: schemas.HostReservation
        if host.min < 1 or host.max < 1:
            errors.append(
                {
                    "loc": ["body", "lease", "reservations", index],
                    "msg": "host reservation min and max must be >= 1",
                    "type": "value_error",
                }
            )
            continue
        if host.min > host.max:
            errors.append(
                {
                    "loc": ["body", "lease", "reservations", index],
                    "msg": "host reservation min must be <= max",
                    "type": "value_error",
                }
            )


def _validate_host_exclusivity(
    reservations: List[Any],
    errors: List[Dict[str, Any]],
) -> None:
    """Enforce that a ``physical:host`` reservation cannot share a lease with others.

    We also reject more than one host reservation per lease, matching the
    form-level lock the console enforces.
    """
    types = [_resource_type_of(r) for r in reservations]
    host_count = sum(1 for t in types if t == "physical:host")
    if host_count == 0:
        return
    if host_count > 1 or len(reservations) > 1:
        errors.append(
            {
                "loc": ["body", "lease", "reservations"],
                "msg": (
                    "compute host reservations cannot share a lease with other "
                    "reservations"
                ),
                "type": "value_error",
            }
        )


async def _validate_flavor_visibility(
    profile: schemas.Profile,
    session: Session,
    global_request_id: Optional[str],
    reservations: List[Any],
    errors: List[Dict[str, Any]],
) -> None:
    """Check that every flavor:instance reservation references a flavor
    visible to the current project."""
    flavor_indexes: List[int] = []
    flavor_ids: List[str] = []
    for index, reservation in enumerate(reservations):
        if _resource_type_of(reservation) != "flavor:instance":
            continue
        flavor_id = getattr(reservation, "flavor_id", None)
        if not flavor_id:
            continue
        flavor_indexes.append(index)
        flavor_ids.append(str(flavor_id))

    for index, flavor_id in zip(flavor_indexes, flavor_ids):
        visible = await _is_flavor_visible(
            profile=profile,
            session=session,
            global_request_id=global_request_id,
            flavor_id=flavor_id,
        )
        if not visible:
            errors.append(
                {
                    "loc": ["body", "lease", "reservations", index, "flavor_id"],
                    "msg": (
                        f"flavor '{flavor_id}' is not visible to the current project"
                    ),
                    "type": "value_error",
                }
            )


async def _is_flavor_visible(
    *,
    profile: schemas.Profile,
    session: Session,
    global_request_id: Optional[str],
    flavor_id: str,
) -> bool:
    """Return whether the given flavor id is visible to the current project."""
    try:
        nc = await client_utils.nova_client(
            session=session,
            region=profile.region,
            global_request_id=global_request_id,
        )
        await run_in_threadpool(nc.flavors.get, flavor_id)
        return True
    except (NovaNotFound, NovaForbidden):
        return False
    except Exception as exc:  # pragma: no cover - defensive fallback
        LOG.warning("Failed to check flavor visibility for {}: {!r}", flavor_id, exc)
        return False


async def _validate_required_floatingips(
    session: Session,
    region: str,
    global_request_id: Optional[str],
    reservations: List[Any],
    errors: List[Dict[str, Any]],
) -> None:
    """Check that every address in ``required_floatingips`` is registered
    with Blazar for the chosen network."""
    for index, reservation in enumerate(reservations):
        if _resource_type_of(reservation) != "virtual:floatingip":
            continue
        required = getattr(reservation, "required_floatingips", None) or []
        if not required:
            continue
        network_id = getattr(reservation, "network_id", None)
        if not network_id:
            continue

        try:
            registered = await blazar.list_floatingips(
                session=session,
                region=region,
                global_request_id=global_request_id,
                network_id=str(network_id),
            )
        except HTTPException:
            # Surface Blazar's own error untouched for the caller to handle.
            raise

        registered_addresses = {
            fip.get("floating_ip_address") or fip.get("address")
            for fip in registered
            if isinstance(fip, dict)
        }
        registered_addresses.discard(None)
        for address in required:
            if address not in registered_addresses:
                errors.append(
                    {
                        "loc": [
                            "body",
                            "lease",
                            "reservations",
                            index,
                            "required_floatingips",
                        ],
                        "msg": (
                            f"floating IP '{address}' is not registered with Blazar "
                            f"for network '{network_id}'"
                        ),
                        "type": "value_error",
                    }
                )


def _validate_before_end(
    reservations: List[Any],
    before_end_emails: Optional[str],
    errors: List[Dict[str, Any]],
) -> None:
    """
    The before_end action lives on each host reservation in the Blazar API
    (the console hoists it onto the lease for the form). We accept the action
    when at least one of the per-reservation ``before_end`` values is present
    and apply the rules:

    * ``default`` is always accepted.
    * ``email`` requires non-empty ``before_end_notification_emails`` whose
      comma-separated entries match the standard email regex.
    * ``snapshot`` requires the lease to contain at most one reservation, and
      that reservation must be ``flavor:instance``.
    """
    actions = []
    for reservation in reservations:
        action = getattr(reservation, "before_end", None)
        if action is not None:
            actions.append(str(action))

    if not actions:
        return

    types = [_resource_type_of(r) for r in reservations]

    for action in actions:
        if action == "default":
            continue
        if action == "email":
            if not before_end_emails or not before_end_emails.strip():
                errors.append(
                    {
                        "loc": ["body", "lease", "before_end_notification_emails"],
                        "msg": (
                            "before_end action 'email' requires "
                            "before_end_notification_emails"
                        ),
                        "type": "value_error",
                    }
                )
                continue
            for entry in before_end_emails.split(","):
                cleaned = entry.strip()
                if not _EMAIL_RE.match(cleaned):
                    errors.append(
                        {
                            "loc": ["body", "lease", "before_end_notification_emails"],
                            "msg": f"invalid email address: '{cleaned}'",
                            "type": "value_error",
                        }
                    )
            continue
        if action == "snapshot":
            if len(reservations) > 1 or not types or types[0] != "flavor:instance":
                errors.append(
                    {
                        "loc": ["body", "lease", "reservations"],
                        "msg": (
                            "before_end action 'snapshot' requires a single "
                            "flavor:instance reservation in the lease"
                        ),
                        "type": "value_error",
                    }
                )
            continue
        errors.append(
            {
                "loc": ["body", "lease", "reservations"],
                "msg": f"unsupported before_end action: '{action}'",
                "type": "value_error",
            }
        )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.post(
    "/reservation/leases",
    description="Create a Blazar lease with cross-field validation.",
    responses={
        201: {"model": LeaseResponse},
        400: {"model": schemas.BadRequestMessage},
        401: {"model": schemas.UnauthorizedMessage},
        403: {"model": schemas.ForbiddenMessage},
        500: {"model": schemas.InternalServerErrorMessage},
    },
    response_model=LeaseResponse,
    status_code=status.HTTP_201_CREATED,
    response_description="Created",
)
async def create_lease(
    request_body: LeaseCreateRequest = Body(...),
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header(
        "",
        alias=constants.INBOUND_HEADER,
        regex=constants.INBOUND_HEADER_REGEX,
    ),
) -> LeaseResponse:
    lease = request_body.lease
    errors: List[Dict[str, Any]] = []

    # At least one reservation is required. Pydantic already enforces
    # ``reservations`` is a non-None list, so we only need to assert
    # non-emptiness.
    if not lease.reservations:
        errors.append(
            {
                "loc": ["body", "lease", "reservations"],
                "msg": "at least one reservation is required",
                "type": "value_error",
            }
        )

    _validate_dates(lease.start_date, lease.end_date, is_update=False, errors=errors)
    _validate_host_min_max(lease.reservations or [], errors)
    _validate_host_exclusivity(lease.reservations or [], errors)
    _validate_before_end(
        lease.reservations or [], lease.before_end_notification_emails, errors
    )

    session = await generate_session(profile=profile)

    if not errors:
        await _validate_flavor_visibility(
            profile=profile,
            session=session,
            global_request_id=x_openstack_request_id,
            reservations=lease.reservations,
            errors=errors,
        )
        await _validate_required_floatingips(
            session=session,
            region=profile.region,
            global_request_id=x_openstack_request_id,
            reservations=lease.reservations,
            errors=errors,
        )

    if errors:
        raise _validation_errors(errors)

    body = _serialize_lease(lease)
    created = await blazar.create_lease(
        session=session,
        region=profile.region,
        global_request_id=x_openstack_request_id,
        body=body,
    )
    return LeaseResponse(lease=created or {})


@router.put(
    "/reservation/leases/{lease_id}",
    description="Update a Blazar lease with cross-field validation.",
    responses={
        200: {"model": LeaseResponse},
        400: {"model": schemas.BadRequestMessage},
        401: {"model": schemas.UnauthorizedMessage},
        403: {"model": schemas.ForbiddenMessage},
        404: {"model": schemas.NotFoundMessage},
        500: {"model": schemas.InternalServerErrorMessage},
    },
    response_model=LeaseResponse,
    status_code=status.HTTP_200_OK,
    response_description="OK",
)
async def update_lease(
    lease_id: str = Path(..., description="Blazar lease ID to update"),
    request_body: LeaseUpdateRequest = Body(...),
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header(
        "",
        alias=constants.INBOUND_HEADER,
        regex=constants.INBOUND_HEADER_REGEX,
    ),
) -> LeaseResponse:
    lease = request_body.lease
    errors: List[Dict[str, Any]] = []

    _validate_dates(lease.start_date, lease.end_date, is_update=True, errors=errors)

    if lease.reservations is not None:
        _validate_host_min_max(lease.reservations, errors)
        _validate_host_exclusivity(lease.reservations, errors)
        _validate_before_end(
            lease.reservations, lease.before_end_notification_emails, errors
        )

    session = await generate_session(profile=profile)

    if not errors and lease.reservations is not None:
        await _validate_flavor_visibility(
            profile=profile,
            session=session,
            global_request_id=x_openstack_request_id,
            reservations=lease.reservations,
            errors=errors,
        )
        await _validate_required_floatingips(
            session=session,
            region=profile.region,
            global_request_id=x_openstack_request_id,
            reservations=lease.reservations,
            errors=errors,
        )

    if errors:
        raise _validation_errors(errors)

    body = _serialize_lease(lease)
    updated = await blazar.update_lease(
        session=session,
        region=profile.region,
        global_request_id=x_openstack_request_id,
        lease_id=lease_id,
        body=body,
    )
    return LeaseResponse(lease=updated or {})


@router.get(
    "/reservation/calendar",
    description=(
        "Aggregate Blazar leases (and optionally hosts, for admins) into "
        "calendar rows scoped to a time window."
    ),
    responses={
        200: {"model": schemas.CalendarResponse},
        400: {"model": schemas.BadRequestMessage},
        401: {"model": schemas.UnauthorizedMessage},
        500: {"model": schemas.InternalServerErrorMessage},
    },
    response_model=schemas.CalendarResponse,
    status_code=status.HTTP_200_OK,
    response_description="OK",
)
async def get_calendar(
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header(
        "",
        alias=constants.INBOUND_HEADER,
        regex=constants.INBOUND_HEADER_REGEX,
    ),
    start: str = Query(..., description="Window start as an ISO 8601 timestamp"),
    end: str = Query(..., description="Window end as an ISO 8601 timestamp"),
    include_hosts: bool = Query(
        False, description="Include host availability rows (admin only)."
    ),
) -> schemas.CalendarResponse:
    window_start = _parse_iso(start, ["query", "start"])
    window_end = _parse_iso(end, ["query", "end"])
    if not (window_end > window_start):
        raise _validation_error(["query", "end"], "end must be strictly after start")

    session = await generate_session(profile=profile)

    leases = await blazar.list_leases(
        session=session,
        region=profile.region,
        global_request_id=x_openstack_request_id,
    )
    lease_rows = _build_lease_rows(leases, window_start, window_end)

    is_admin = is_system_admin_or_reader(profile=profile)
    if not include_hosts or not is_admin:
        # Either the caller did not opt in or has no admin scope.
        # The calendar still renders, just without hosts.
        return schemas.CalendarResponse(
            lease_rows=lease_rows, host_rows=None, partial=False
        )

    try:
        host_rows = await asyncio.wait_for(
            _build_host_rows(
                session=session,
                region=profile.region,
                global_request_id=x_openstack_request_id,
                window_start=window_start,
                window_end=window_end,
            ),
            timeout=_HOST_FANOUT_TIMEOUT,
        )
    except asyncio.TimeoutError:
        # Host fan-out timed out — return the lease rows we already have
        # with host_rows=None and partial=True so the console can render
        # a warning while keeping the lease bars.
        LOG.warning(
            "Blazar host fan-out timed out after {}s for calendar window {} -> {}",
            _HOST_FANOUT_TIMEOUT,
            start,
            end,
        )
        return schemas.CalendarResponse(
            lease_rows=lease_rows, host_rows=None, partial=True
        )

    return schemas.CalendarResponse(
        lease_rows=lease_rows, host_rows=host_rows, partial=False
    )


@router.get(
    "/reservation/floatingips/by-network/{network_id}",
    description=(
        "List Blazar-registered floating IPs filtered by Neutron network."
    ),
    responses={
        200: {"model": FloatingIpsByNetworkResponse},
        401: {"model": schemas.UnauthorizedMessage},
        500: {"model": schemas.InternalServerErrorMessage},
    },
    response_model=FloatingIpsByNetworkResponse,
    status_code=status.HTTP_200_OK,
    response_description="OK",
)
async def list_floatingips_by_network(
    network_id: str = Path(..., description="Neutron network ID to filter on"),
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header(
        "",
        alias=constants.INBOUND_HEADER,
        regex=constants.INBOUND_HEADER_REGEX,
    ),
) -> FloatingIpsByNetworkResponse:
    session = await generate_session(profile=profile)
    floatingips = await blazar.list_floatingips(
        session=session,
        region=profile.region,
        global_request_id=x_openstack_request_id,
        network_id=network_id,
    )
    return FloatingIpsByNetworkResponse(floatingips=floatingips)


@router.get(
    "/reservation/flavors/{flavor_id}/visibility",
    description=(
        "Return whether a Nova flavor is visible to the current project "
    ),
    responses={
        200: {"model": FlavorVisibilityResponse},
        401: {"model": schemas.UnauthorizedMessage},
        500: {"model": schemas.InternalServerErrorMessage},
    },
    response_model=FlavorVisibilityResponse,
    status_code=status.HTTP_200_OK,
    response_description="OK",
)
async def get_flavor_visibility(
    flavor_id: str = Path(..., description="Nova flavor ID to check"),
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header(
        "",
        alias=constants.INBOUND_HEADER,
        regex=constants.INBOUND_HEADER_REGEX,
    ),
) -> FlavorVisibilityResponse:
    session = await generate_session(profile=profile)
    visible = await _is_flavor_visible(
        profile=profile,
        session=session,
        global_request_id=x_openstack_request_id,
        flavor_id=flavor_id,
    )
    return FlavorVisibilityResponse(flavor_id=flavor_id, visible=visible)


# ---------------------------------------------------------------------------
# Calendar internals
# ---------------------------------------------------------------------------


def _build_lease_rows(
    leases: List[Dict[str, Any]],
    window_start: datetime,
    window_end: datetime,
) -> List[schemas.CalendarLeaseRow]:
    """Filter ``leases`` by intersection with ``[window_start, window_end)``
    and shape each survivor into a :class:`CalendarLeaseRow`.

    A lease is included iff ``lease.start < window_end`` AND
    ``lease.end > window_start``.
    """
    rows: List[schemas.CalendarLeaseRow] = []
    for lease in leases:
        if not isinstance(lease, dict):
            continue
        start_str = lease.get("start_date")
        end_str = lease.get("end_date")
        if not start_str or not end_str:
            continue
        try:
            lease_start = _parse_iso(str(start_str), ["lease", "start_date"])
            lease_end = _parse_iso(str(end_str), ["lease", "end_date"])
        except HTTPException:
            # Skip malformed lease entries rather than failing the whole route;
            # the console renders what we can and logs the rest.
            LOG.warning(
                "Skipping lease {} with unparseable dates: start={!r} end={!r}",
                lease.get("id"),
                start_str,
                end_str,
            )
            continue

        if not (lease_start < window_end and lease_end > window_start):
            continue

        reservations = lease.get("reservations") or []
        dominant = _dominant_type(reservations) or "physical:host"
        # ``ResourceType`` validates the value; if Blazar returns anything
        # unexpected, fall back to the default to keep the row visible.
        try:
            dominant_enum = schemas.ResourceType(dominant)
        except ValueError:
            dominant_enum = schemas.ResourceType.physical_host

        rows.append(
            schemas.CalendarLeaseRow(
                lease_id=str(lease.get("id", "")),
                name=str(lease.get("name", "")),
                start=str(start_str),
                end=str(end_str),
                status=str(lease.get("status", "")),
                dominant_type=dominant_enum,
            )
        )
    return rows


async def _build_host_rows(
    *,
    session: Session,
    region: str,
    global_request_id: Optional[str],
    window_start: datetime,
    window_end: datetime,
) -> List[schemas.CalendarHostRow]:
    hosts = await blazar.list_hosts(
        session=session,
        region=region,
        global_request_id=global_request_id,
    )
    if not hosts:
        return []

    tasks = [
        blazar.list_host_allocations(
            session=session,
            region=region,
            global_request_id=global_request_id,
            host_id=str(host.get("id")),
        )
        for host in hosts
        if isinstance(host, dict) and host.get("id")
    ]
    allocations_per_host = await asyncio.gather(*tasks, return_exceptions=False)

    rows: List[schemas.CalendarHostRow] = []
    for host, allocations in zip(hosts, allocations_per_host):
        if not isinstance(host, dict):
            continue
        host_id = str(host.get("id", ""))
        hypervisor_hostname = str(host.get("hypervisor_hostname", host.get("name", "")))

        windowed = _filter_allocations(allocations, window_start, window_end)
        rows.append(
            schemas.CalendarHostRow(
                host_id=host_id,
                hypervisor_hostname=hypervisor_hostname,
                allocations=windowed,
            )
        )
    return rows


def _filter_allocations(
    allocations: List[Dict[str, Any]],
    window_start: datetime,
    window_end: datetime,
) -> List[schemas.CalendarAllocation]:
    """Filter raw Blazar allocations by intersection with the calendar window.

    Blazar's allocation entries nest reservation rows under ``reservations``;
    each reservation carries its own ``start_date`` / ``end_date`` and an
    owning ``lease_id``. We flatten them into per-row ``CalendarAllocation``
    entries keeping only those that intersect the window.
    """
    flattened: List[schemas.CalendarAllocation] = []
    for entry in allocations or []:
        if not isinstance(entry, dict):
            continue
        for reservation in entry.get("reservations") or []:
            if not isinstance(reservation, dict):
                continue
            start_str = reservation.get("start_date")
            end_str = reservation.get("end_date")
            lease_id = reservation.get("lease_id") or entry.get("lease_id")
            if not start_str or not end_str:
                continue
            try:
                alloc_start = _parse_iso(str(start_str), ["allocation", "start_date"])
                alloc_end = _parse_iso(str(end_str), ["allocation", "end_date"])
            except HTTPException:
                continue
            if not (alloc_start < window_end and alloc_end > window_start):
                continue
            flattened.append(
                schemas.CalendarAllocation(
                    lease_id=str(lease_id or ""),
                    start=str(start_str),
                    end=str(end_str),
                )
            )
    return flattened
