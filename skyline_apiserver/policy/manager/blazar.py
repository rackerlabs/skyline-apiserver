# Copyright 2026 OpenStack Skyline Authors
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

# flake8: noqa
# fmt: off

from . import base

PROJECT_READER = "role:reader or role:member or role:_member_"
PROJECT_MEMBER = "role:member or role:_member_"
SYSTEM_READER = "role:reader and system_scope:all"
SYSTEM_ADMIN = "role:admin and system_scope:all"

list_rules = (
    base.Rule(
        name="blazar_project_reader",
        check_str=f"({PROJECT_READER})",
        description="Project readers and members can inspect Blazar reservation resources.",
    ),
    base.Rule(
        name="blazar_project_member",
        check_str=f"({PROJECT_MEMBER})",
        description="Project members can manage Blazar reservations.",
    ),
    base.APIRule(
        name="osreservations:leases:get",
        check_str=f"rule:blazar_project_reader or ({SYSTEM_READER}) or ({SYSTEM_ADMIN})",
        description="List leases and show lease details.",
        scope_types=["project", "system"],
        operations=[
            {"method": "GET", "path": "/v1/leases"},
            {"method": "GET", "path": "/v1/leases/{lease_id}"},
        ],
    ),
    base.APIRule(
        name="osreservations:leases:create",
        check_str=f"rule:blazar_project_member or ({SYSTEM_ADMIN})",
        description="Create a lease.",
        scope_types=["project", "system"],
        operations=[{"method": "POST", "path": "/v1/leases"}],
    ),
    base.APIRule(
        name="osreservations:leases:update",
        check_str=f"rule:blazar_project_member or ({SYSTEM_ADMIN})",
        description="Update a lease.",
        scope_types=["project", "system"],
        operations=[{"method": "PUT", "path": "/v1/leases/{lease_id}"}],
    ),
    base.APIRule(
        name="osreservations:leases:delete",
        check_str=f"rule:blazar_project_member or ({SYSTEM_ADMIN})",
        description="Delete a lease.",
        scope_types=["project", "system"],
        operations=[{"method": "DELETE", "path": "/v1/leases/{lease_id}"}],
    ),
    base.APIRule(
        name="osreservations:hosts:get",
        check_str=f"rule:blazar_project_reader or ({SYSTEM_READER}) or ({SYSTEM_ADMIN})",
        description="List reservable hosts and show host details.",
        scope_types=["project", "system"],
        operations=[
            {"method": "GET", "path": "/v1/os-hosts"},
            {"method": "GET", "path": "/v1/os-hosts/{host_id}"},
        ],
    ),
    base.APIRule(
        name="osreservations:floatingips:get",
        check_str=f"rule:blazar_project_reader or ({SYSTEM_READER}) or ({SYSTEM_ADMIN})",
        description="List reservable floating IPs and show floating IP details.",
        scope_types=["project", "system"],
        operations=[
            {"method": "GET", "path": "/v1/floatingips"},
            {"method": "GET", "path": "/v1/floatingips/{floatingip_id}"},
        ],
    ),
)

__all__ = ("list_rules",)
