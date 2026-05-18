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

"""Skyline_Apiserver client for OpenStack Blazar (reservation service).

This module is a thin HTTP wrapper that:

- resolves the ``reservation`` endpoint from the user's Keystone session via
  ``utils.get_endpoint``;
- issues authenticated requests through ``keystoneauth1.session.Session.request``
  with ``X-OpenStack-Request-ID`` propagation;
- centralizes exception mapping in ``_handle_blazar_error`` so that
  ``Unauthorized`` -> 401, ``ConnectFailure`` -> 503 with body
  ``Blazar service unreachable``, ``asyncio.TimeoutError`` -> 504, and any
  Blazar HTTP error is echoed with its original status code and message;
- emits structured request/response logs through the shared ``LOG`` instance.

Higher-level routes under ``api/v1/reservation.py`` consume these helpers and
add server-side validation, aggregation, and admin-role enforcement.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

from fastapi import HTTPException
from fastapi import status as http_status
from keystoneauth1.exceptions.connection import (
    ConnectFailure,
    ConnectionError as KsaConnectionError,
)
from keystoneauth1.exceptions.http import HttpError, Unauthorized
from keystoneauth1.session import Session
from starlette.concurrency import run_in_threadpool

from skyline_apiserver.client import utils
from skyline_apiserver.log import LOG
from skyline_apiserver.types import constants

# Blazar registers itself in the Keystone catalog under the ``reservation``
# service type. Skyline maps that to the friendly name ``blazar`` for nginx
# and console wiring (see ``config/openstack.py::service_mapping``).
_BLAZAR_SERVICE_TYPE = "reservation"


# ---------------------------------------------------------------------------
# Error mapping
# ---------------------------------------------------------------------------


def _extract_blazar_detail(exc: HttpError) -> str:
    """Extract a human-readable error message from a Blazar ``HttpError``.

    Blazar may return error bodies in any of the following shapes::

        {"error": {"code": int, "message": str}}
        {"error_message": "..."}
        {"detail": "..."}
        {"faultstring": "..."}

    or a plain text body. This helper inspects each shape in order and falls
    back to the raw response text or the exception message.
    """
    response = getattr(exc, "response", None)
    if response is not None:
        try:
            payload = response.json()
        except Exception:
            payload = None
        if isinstance(payload, dict):
            err = payload.get("error")
            if isinstance(err, dict):
                msg = err.get("message")
                if msg:
                    return str(msg)
            if isinstance(err, str) and err:
                return err
            for key in ("error_message", "detail", "faultstring", "message"):
                value = payload.get(key)
                if value:
                    return str(value)
        text = getattr(response, "text", None)
        if text:
            return str(text)
    return str(exc) or "Blazar request failed"


def _handle_blazar_error(
    exc: BaseException,
    *,
    method: str,
    url: str,
) -> HTTPException:
    """Translate exceptions raised during a Blazar request into ``HTTPException``.

    The mapping is centralized so that every public function in this module
    surfaces consistent statuses to Skyline_Console:

    +-------------------------------------+--------+---------------------------------+
    | Exception                           | Status | Body                            |
    +=====================================+========+=================================+
    | ``Unauthorized``                    | 401    | ``Blazar: <message>``           |
    +-------------------------------------+--------+---------------------------------+
    | ``ConnectFailure`` / connection err | 503    | ``Blazar service unreachable``  |
    +-------------------------------------+--------+---------------------------------+
    | ``asyncio.TimeoutError``            | 504    | ``Blazar request timed out``    |
    +-------------------------------------+--------+---------------------------------+
    | ``HttpError`` (4xx/5xx from Blazar) | echoed | Blazar's ``message``/``detail`` |
    +-------------------------------------+--------+---------------------------------+
    | anything else                       | 500    | ``str(exc)``                    |
    +-------------------------------------+--------+---------------------------------+
    """
    LOG.warning("Blazar request failed: {} {}: {!r}", method, url, exc)

    if isinstance(exc, Unauthorized):
        return HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail=f"Blazar: {exc}",
        )
    if isinstance(exc, (ConnectFailure, KsaConnectionError)):
        return HTTPException(
            status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blazar service unreachable",
        )
    if isinstance(exc, asyncio.TimeoutError):
        return HTTPException(
            status_code=http_status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Blazar request timed out",
        )
    if isinstance(exc, HttpError):
        echoed = exc.http_status or http_status.HTTP_500_INTERNAL_SERVER_ERROR
        return HTTPException(status_code=echoed, detail=_extract_blazar_detail(exc))
    return HTTPException(
        status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(exc),
    )


# ---------------------------------------------------------------------------
# Core HTTP helper
# ---------------------------------------------------------------------------


async def _request(
    session: Session,
    region: str,
    global_request_id: Optional[str],
    method: str,
    path: str,
    *,
    json: Any = None,
    params: Optional[Dict[str, Any]] = None,
) -> Any:
    """Issue an authenticated HTTP request to ``blazar-api``.

    The reservation endpoint is resolved through ``utils.get_endpoint`` so the
    caller never needs to know the catalog URL. The inbound
    ``X-OpenStack-Request-ID`` header is propagated for correlation, and any
    raised exception is mapped through ``_handle_blazar_error``.

    :param method: HTTP method, e.g. ``"GET"``, ``"POST"``.
    :param path: Path to append to the resolved endpoint, e.g. ``"/leases"``.
    :param json: Optional JSON-serializable request body.
    :param params: Optional querystring parameters.
    :returns: Parsed JSON body, or ``None`` for ``204`` / empty responses.
    """
    base_endpoint = await utils.get_endpoint(
        region=region,
        service=_BLAZAR_SERVICE_TYPE,
        session=session,
    )
    url = base_endpoint.rstrip("/") + path

    headers: Dict[str, str] = {}
    if global_request_id:
        headers[constants.INBOUND_HEADER] = global_request_id

    LOG.debug("Blazar request: {} {}", method, url)
    try:
        response = await run_in_threadpool(
            session.request,
            url,
            method,
            json=json,
            params=params,
            headers=headers,
            # Disable keystoneauth's automatic connect retries so transient
            # failures surface immediately as a 503 rather than being silently
            # retried.
            connect_retries=0,
        )
    except Exception as exc:
        raise _handle_blazar_error(exc, method=method, url=url) from exc

    LOG.info("Blazar response: {} {} -> {}", method, url, response.status_code)

    if response.status_code == 204 or not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.text


def _unwrap(payload: Any, key: str) -> Any:
    """Return ``payload[key]`` when ``payload`` is the standard Blazar wrapper.

    Blazar wraps single-resource responses as ``{"lease": {...}}`` and
    collections as ``{"leases": [...]}``. Callers typically only care about the
    inner value, so this helper unwraps the wrapper when present and returns
    the payload unchanged otherwise (handles minor server-side variations
    without breaking call sites).
    """
    if isinstance(payload, dict) and key in payload:
        return payload[key]
    return payload


# ---------------------------------------------------------------------------
# Lease operations (/v1/leases)
# ---------------------------------------------------------------------------


async def list_leases(
    session: Session,
    region: str,
    global_request_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """List leases visible to the authenticated user (``GET /v1/leases``)."""
    payload = await _request(session, region, global_request_id, "GET", "/leases")
    return _unwrap(payload, "leases") or []


async def get_lease(
    session: Session,
    region: str,
    global_request_id: Optional[str],
    lease_id: str,
) -> Dict[str, Any]:
    """Fetch a single lease by id (``GET /v1/leases/{lease_id}``)."""
    payload = await _request(
        session, region, global_request_id, "GET", f"/leases/{lease_id}",
    )
    return _unwrap(payload, "lease")


async def create_lease(
    session: Session,
    region: str,
    global_request_id: Optional[str],
    body: Dict[str, Any],
) -> Dict[str, Any]:
    """Create a lease (``POST /v1/leases``).

    The ``body`` is forwarded verbatim to Blazar.
    """
    payload = await _request(
        session, region, global_request_id, "POST", "/leases", json=body,
    )
    return _unwrap(payload, "lease")


async def update_lease(
    session: Session,
    region: str,
    global_request_id: Optional[str],
    lease_id: str,
    body: Dict[str, Any],
) -> Dict[str, Any]:
    """Update an existing lease (``PUT /v1/leases/{lease_id}``)."""
    payload = await _request(
        session, region, global_request_id, "PUT", f"/leases/{lease_id}", json=body,
    )
    return _unwrap(payload, "lease")


async def delete_lease(
    session: Session,
    region: str,
    global_request_id: Optional[str],
    lease_id: str,
) -> None:
    """Delete a lease (``DELETE /v1/leases/{lease_id}``)."""
    await _request(
        session, region, global_request_id, "DELETE", f"/leases/{lease_id}",
    )


# ---------------------------------------------------------------------------
# Host operations (/v1/os-hosts), admin-only at the route layer
# ---------------------------------------------------------------------------


async def list_hosts(
    session: Session,
    region: str,
    global_request_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """List Blazar-registered hypervisor hosts (``GET /v1/os-hosts``)."""
    payload = await _request(session, region, global_request_id, "GET", "/os-hosts")
    return _unwrap(payload, "hosts") or []


async def get_host(
    session: Session,
    region: str,
    global_request_id: Optional[str],
    host_id: str,
) -> Dict[str, Any]:
    """Fetch a single host (``GET /v1/os-hosts/{host_id}``)."""
    payload = await _request(
        session, region, global_request_id, "GET", f"/os-hosts/{host_id}",
    )
    return _unwrap(payload, "host")


async def create_host(
    session: Session,
    region: str,
    global_request_id: Optional[str],
    body: Dict[str, Any],
) -> Dict[str, Any]:
    """Register a new host with Blazar (``POST /v1/os-hosts``)."""
    payload = await _request(
        session, region, global_request_id, "POST", "/os-hosts", json=body,
    )
    return _unwrap(payload, "host")


async def update_host(
    session: Session,
    region: str,
    global_request_id: Optional[str],
    host_id: str,
    body: Dict[str, Any],
) -> Dict[str, Any]:
    """Update a registered host (``PUT /v1/os-hosts/{host_id}``)."""
    payload = await _request(
        session,
        region,
        global_request_id,
        "PUT",
        f"/os-hosts/{host_id}",
        json=body,
    )
    return _unwrap(payload, "host")


async def delete_host(
    session: Session,
    region: str,
    global_request_id: Optional[str],
    host_id: str,
) -> None:
    """Unregister a host (``DELETE /v1/os-hosts/{host_id}``)."""
    await _request(
        session, region, global_request_id, "DELETE", f"/os-hosts/{host_id}",
    )


async def list_host_allocations(
    session: Session,
    region: str,
    global_request_id: Optional[str],
    host_id: str,
) -> List[Dict[str, Any]]:
    """List allocations for a single host (``GET /v1/os-hosts/{host_id}/allocations``)."""
    payload = await _request(
        session,
        region,
        global_request_id,
        "GET",
        f"/os-hosts/{host_id}/allocations",
    )
    return _unwrap(payload, "allocations") or []


async def list_all_allocations(
    session: Session,
    region: str,
    global_request_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """List allocations across all hosts (``GET /v1/os-hosts/allocations``)."""
    payload = await _request(
        session, region, global_request_id, "GET", "/os-hosts/allocations",
    )
    return _unwrap(payload, "allocations") or []


# ---------------------------------------------------------------------------
# Floating IP operations (/v1/floatingips)
# ---------------------------------------------------------------------------


async def list_floatingips(
    session: Session,
    region: str,
    global_request_id: Optional[str] = None,
    network_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """List Blazar-registered floating IPs (``GET /v1/floatingips``).

    When ``network_id`` is provided, the returned list is filtered to floating
    IPs in that Neutron network. Filtering is performed client-side because
    the Blazar API does not advertise a stable querystring filter for it.
    """
    payload = await _request(
        session, region, global_request_id, "GET", "/floatingips",
    )
    floatingips = _unwrap(payload, "floatingips") or []
    if network_id is not None:
        floatingips = [
            fip for fip in floatingips
            if isinstance(fip, dict) and fip.get("network_id") == network_id
        ]
    return floatingips


async def get_floatingip(
    session: Session,
    region: str,
    global_request_id: Optional[str],
    floatingip_id: str,
) -> Dict[str, Any]:
    """Fetch a single floating IP (``GET /v1/floatingips/{id}``)."""
    payload = await _request(
        session,
        region,
        global_request_id,
        "GET",
        f"/floatingips/{floatingip_id}",
    )
    return _unwrap(payload, "floatingip")


async def create_floatingip(
    session: Session,
    region: str,
    global_request_id: Optional[str],
    body: Dict[str, Any],
) -> Dict[str, Any]:
    """Register a floating IP with Blazar (``POST /v1/floatingips``)."""
    payload = await _request(
        session, region, global_request_id, "POST", "/floatingips", json=body,
    )
    return _unwrap(payload, "floatingip")


async def delete_floatingip(
    session: Session,
    region: str,
    global_request_id: Optional[str],
    floatingip_id: str,
) -> None:
    """Unregister a floating IP (``DELETE /v1/floatingips/{id}``)."""
    await _request(
        session,
        region,
        global_request_id,
        "DELETE",
        f"/floatingips/{floatingip_id}",
    )
