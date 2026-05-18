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

"""Pydantic schemas for the Blazar reservation routes.

These models are used by the Skyline-internal validation/aggregation routes at
``skyline_apiserver/api/v1/reservation.py``. They mirror the wire format of
Blazar's ``/v1/leases`` API for the parts that flow through this layer, and
add Skyline-internal aggregation shapes for the calendar route.

Skyline never invents new reservation types. The reservation models below are
a discriminated union over the Blazar ``resource_type`` field, with one model
per supported type:

* ``physical:host``     -> :class:`HostReservation`
* ``flavor:instance``   -> :class:`FlavorReservation`
* ``virtual:floatingip``-> :class:`FloatingIpReservation`

Validation that requires cross-field or cross-service checks (date ordering,
flavor visibility, floating IP membership, before_end action compatibility) is
performed by the route handler, not by these models.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class ResourceType(str, Enum):
    """Blazar reservation resource types supported by Skyline."""

    physical_host = "physical:host"
    flavor_instance = "flavor:instance"
    virtual_floatingip = "virtual:floatingip"

    def __str__(self) -> str:
        return self.value


class LeaseEventType(str, Enum):
    """Lifecycle event types Blazar emits per lease."""

    start_lease = "start_lease"
    end_lease = "end_lease"
    before_end = "before_end"

    def __str__(self) -> str:
        return self.value


class LeaseEventStatus(str, Enum):
    """Status values Blazar reports for lease events."""

    UNPROCESSED = "UNPROCESSED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ERROR = "ERROR"

    def __str__(self) -> str:
        return self.value


class BeforeEndAction(str, Enum):
    """Actions Blazar can run when the ``before_end`` event fires."""

    default = "default"
    email = "email"
    snapshot = "snapshot"

    def __str__(self) -> str:
        return self.value


# ---------------------------------------------------------------------------
# Reservation type-specific models
# ---------------------------------------------------------------------------


class _ReservationBase(BaseModel):
    """Fields shared by every reservation entry, regardless of resource type."""

    id: Optional[str] = Field(None, description="Reservation ID assigned by Blazar")
    status: Optional[str] = Field(None, description="Reservation status reported by Blazar")


class HostReservation(_ReservationBase):
    """Compute host reservation (``resource_type == 'physical:host'``).

    Accepts ``min``/``max`` host counts and Blazar predicate expressions
    composed by the console form. The server-side route enforces
    ``1 <= min <= max`` before forwarding to Blazar.
    """

    resource_type: str = Field(
        "physical:host",
        const=True,
        description="Blazar resource type discriminator",
    )
    min: int = Field(..., ge=1, description="Minimum host count to allocate")
    max: int = Field(..., ge=1, description="Maximum host count to allocate")
    hypervisor_properties: str = Field(
        "",
        description=(
            "Blazar hypervisor predicate expression. Empty string means "
            "'any host'."
        ),
    )
    resource_properties: str = Field(
        "",
        description="Blazar resource predicate expression. Empty string means 'any host'.",
    )
    before_end: Optional[BeforeEndAction] = Field(
        None,
        description="Per-reservation before_end action, when Blazar supports it.",
    )
    # Populated by Blazar after creation; passed through unchanged on read.
    resource_id: Optional[str] = Field(None, description="Blazar-assigned resource id")
    computehost_allocations: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Allocation entries Blazar reports for this reservation.",
    )


class FlavorReservation(_ReservationBase):
    """Flavor-based instance reservation (``resource_type == 'flavor:instance'``).

    Flavor visibility is checked by the route handler against the Nova client;
    the schema only enforces presence and value ranges.
    """

    resource_type: str = Field(
        "flavor:instance",
        const=True,
        description="Blazar resource type discriminator",
    )
    flavor_id: str = Field(..., description="Nova flavor ID to reserve capacity for")
    amount: int = Field(..., ge=1, description="Number of instances to reserve")
    # Populated by Blazar after creation.
    reservation_class_id: Optional[str] = Field(
        None,
        description="Placement reservation class id assigned by Blazar.",
    )


class FloatingIpReservation(_ReservationBase):
    """Floating IP reservation (``resource_type == 'virtual:floatingip'``).

    Membership of ``required_floatingips`` in the Blazar-registered FIP set
    for the chosen network is enforced by the route handler.
    """

    resource_type: str = Field(
        "virtual:floatingip",
        const=True,
        description="Blazar resource type discriminator",
    )
    network_id: str = Field(..., description="Neutron network id to draw FIPs from")
    amount: int = Field(..., ge=1, description="Number of floating IPs to reserve")
    required_floatingips: Optional[List[str]] = Field(
        None,
        description=(
            "Specific floating IP addresses that must be included in the "
            "reservation. Each address must already be registered with Blazar "
            "for the chosen network."
        ),
    )
    # Populated by Blazar after the lease starts.
    assigned_floatingips: Optional[List[str]] = Field(
        None,
        description="Floating IP addresses assigned by Blazar once the lease is active.",
    )


# A reservation entry submitted on a lease can be any of the three types.
# Pydantic 1.x picks the first matching variant; resource_type acts as the
# discriminator because each variant declares it as a literal const.
Reservation = Union[HostReservation, FlavorReservation, FloatingIpReservation]


# ---------------------------------------------------------------------------
# Lease event model
# ---------------------------------------------------------------------------


class LeaseEvent(BaseModel):
    """A Blazar lease lifecycle event.

    Both inbound (when the console submits a ``before_end`` event time) and
    outbound (when the apiserver returns lease detail) use this shape.
    """

    id: Optional[str] = Field(None, description="Event ID assigned by Blazar")
    lease_id: Optional[str] = Field(None, description="Owning lease ID")
    event_type: LeaseEventType = Field(..., description="Lease event type")
    time: str = Field(..., description="Scheduled event time as an ISO 8601 string")
    status: Optional[LeaseEventStatus] = Field(
        None,
        description="Blazar-reported event status; absent on inbound payloads.",
    )


# ---------------------------------------------------------------------------
# Lease create / update payloads
# ---------------------------------------------------------------------------


class LeaseCreate(BaseModel):
    """Body of ``POST /api/v1/reservation/leases`` from the console.

    The route validates date ordering, forwards ``start_date == 'now'``
    literally, and rejects payloads that mix ``physical:host`` with other
    reservation types.
    """

    name: str = Field(..., min_length=1, description="Lease name")
    start_date: str = Field(
        ...,
        description=(
            "Lease start time. Either an ISO 8601 timestamp or the literal "
            "string 'now', which Blazar interprets as the current server time."
        ),
    )
    end_date: str = Field(..., description="Lease end time as an ISO 8601 string")
    reservations: List[Reservation] = Field(
        ...,
        description=(
            "One or more reservations to create with the lease. At least one "
            "reservation is required, and cross-type exclusivity rules apply."
        ),
    )
    events: Optional[List[LeaseEvent]] = Field(
        None,
        description="Optional lease lifecycle events (typically before_end).",
    )
    before_end_notification_emails: Optional[str] = Field(
        None,
        description=(
            "Comma-separated email recipients for the 'email' before_end "
            "action. Required when before_end_action == 'email'."
        ),
    )


class LeaseUpdate(BaseModel):
    """Body of ``PUT /api/v1/reservation/leases/{lease_id}`` from the console.

    Every field is optional so the console can submit partial updates.
    The route enforces ``end_date > now`` and the same cross-field checks
    as :class:`LeaseCreate` for any fields that are present.
    """

    name: Optional[str] = Field(None, description="New lease name")
    start_date: Optional[str] = Field(None, description="New lease start time")
    end_date: Optional[str] = Field(None, description="New lease end time")
    reservations: Optional[List[Reservation]] = Field(
        None,
        description=(
            "Reservations to add, modify, or replace. Existing reservations "
            "must include their Blazar-assigned ``id``."
        ),
    )
    events: Optional[List[LeaseEvent]] = Field(
        None,
        description="Lease events to add or modify.",
    )
    before_end_notification_emails: Optional[str] = Field(
        None,
        description="New comma-separated email recipients for before_end notifications.",
    )


# ---------------------------------------------------------------------------
# Calendar aggregation models
# ---------------------------------------------------------------------------


class CalendarLeaseRow(BaseModel):
    """One row of the calendar's lease lane."""

    lease_id: str = Field(..., description="Blazar lease ID")
    name: str = Field(..., description="Lease name")
    start: str = Field(..., description="Lease start time as an ISO 8601 string")
    end: str = Field(..., description="Lease end time as an ISO 8601 string")
    status: str = Field(..., description="Blazar-reported lease status")
    dominant_type: ResourceType = Field(
        ...,
        description=(
            "The reservation type that dominates this lease, used to color "
            "the lease bar."
        ),
    )


class CalendarAllocation(BaseModel):
    """A single allocation span on a host row."""

    lease_id: str = Field(..., description="Owning lease ID")
    start: str = Field(..., description="Allocation start as an ISO 8601 string")
    end: str = Field(..., description="Allocation end as an ISO 8601 string")


class CalendarHostRow(BaseModel):
    """One row of the calendar's host lane (admin-only)."""

    host_id: str = Field(..., description="Blazar host ID")
    hypervisor_hostname: str = Field(..., description="Underlying hypervisor hostname")
    allocations: List[CalendarAllocation] = Field(
        default_factory=list,
        description="Allocation spans Blazar reports for this host.",
    )


# ``CalendarRow`` is the union shape used by the calendar response. Naming it
# this way matches the task list and lets callers refer to either lane via a
# single import.
CalendarRow = Union[CalendarLeaseRow, CalendarHostRow]


class CalendarResponse(BaseModel):
    """Body of ``GET /api/v1/reservation/calendar``.

    ``host_rows`` is ``None`` when the user is not an admin, or when the
    host-allocation fan-out timed out. In the timeout case ``partial`` is set
    to ``True`` so the console can render a warning while keeping previously
    rendered lease bars.
    """

    lease_rows: List[CalendarLeaseRow] = Field(
        default_factory=list,
        description="Lease bars whose [start, end) intersect the requested window.",
    )
    host_rows: Optional[List[CalendarHostRow]] = Field(
        None,
        description=(
            "Host availability rows, populated only for admins. ``None`` when "
            "the host fan-out was skipped or timed out."
        ),
    )
    partial: bool = Field(
        False,
        description=(
            "True when the host fan-out timed out and the response is missing "
            "host_rows that would otherwise have been included."
        ),
    )
