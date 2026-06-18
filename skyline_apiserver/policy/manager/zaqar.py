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
        name="zaqar_project_reader",
        check_str=f"({PROJECT_READER})",
        description="Project readers and members can inspect Zaqar messaging resources.",
    ),
    base.Rule(
        name="zaqar_project_member",
        check_str=f"({PROJECT_MEMBER})",
        description="Project members can manage Zaqar messaging resources.",
    ),

    # Queues
    base.APIRule(
        name="messaging:queues:get",
        check_str=f"rule:zaqar_project_reader or ({SYSTEM_READER}) or ({SYSTEM_ADMIN})",
        description="List queues and show queue details.",
        scope_types=["project", "system"],
        operations=[
            {"method": "GET", "path": "/v2/queues"},
            {"method": "GET", "path": "/v2/queues/{queue_name}"},
            {"method": "GET", "path": "/v2/queues/{queue_name}/stats"},
            {"method": "GET", "path": "/v2/queues/{queue_name}/metadata"},
        ],
    ),
    base.APIRule(
        name="messaging:queues:create",
        check_str=f"rule:zaqar_project_member or ({SYSTEM_ADMIN})",
        description="Create a queue.",
        scope_types=["project", "system"],
        operations=[{"method": "PUT", "path": "/v2/queues/{queue_name}"}],
    ),
    base.APIRule(
        name="messaging:queues:update",
        check_str=f"rule:zaqar_project_member or ({SYSTEM_ADMIN})",
        description="Update queue metadata.",
        scope_types=["project", "system"],
        operations=[{"method": "PUT", "path": "/v2/queues/{queue_name}/metadata"}],
    ),
    base.APIRule(
        name="messaging:queues:delete",
        check_str=f"rule:zaqar_project_member or ({SYSTEM_ADMIN})",
        description="Delete a queue.",
        scope_types=["project", "system"],
        operations=[{"method": "DELETE", "path": "/v2/queues/{queue_name}"}],
    ),

    # Messages
    base.APIRule(
        name="messaging:messages:get",
        check_str=f"rule:zaqar_project_reader or ({SYSTEM_READER}) or ({SYSTEM_ADMIN})",
        description="List messages in a queue.",
        scope_types=["project", "system"],
        operations=[
            {"method": "GET", "path": "/v2/queues/{queue_name}/messages"},
            {"method": "GET", "path": "/v2/queues/{queue_name}/messages/{message_id}"},
        ],
    ),
    base.APIRule(
        name="messaging:messages:create",
        check_str=f"rule:zaqar_project_member or ({SYSTEM_ADMIN})",
        description="Post messages to a queue.",
        scope_types=["project", "system"],
        operations=[{"method": "POST", "path": "/v2/queues/{queue_name}/messages"}],
    ),

    # Claims
    base.APIRule(
        name="messaging:claims:create",
        check_str=f"rule:zaqar_project_member or ({SYSTEM_ADMIN})",
        description="Claim messages from a queue.",
        scope_types=["project", "system"],
        operations=[{"method": "POST", "path": "/v2/queues/{queue_name}/claims"}],
    ),
    base.APIRule(
        name="messaging:claims:get",
        check_str=f"rule:zaqar_project_reader or ({SYSTEM_READER}) or ({SYSTEM_ADMIN})",
        description="Query a claim.",
        scope_types=["project", "system"],
        operations=[
            {"method": "GET", "path": "/v2/queues/{queue_name}/claims/{claim_id}"},
        ],
    ),
    base.APIRule(
        name="messaging:claims:update",
        check_str=f"rule:zaqar_project_member or ({SYSTEM_ADMIN})",
        description="Renew a claim.",
        scope_types=["project", "system"],
        operations=[
            {"method": "PATCH", "path": "/v2/queues/{queue_name}/claims/{claim_id}"},
        ],
    ),
    base.APIRule(
        name="messaging:claims:delete",
        check_str=f"rule:zaqar_project_member or ({SYSTEM_ADMIN})",
        description="Release a claim.",
        scope_types=["project", "system"],
        operations=[
            {"method": "DELETE", "path": "/v2/queues/{queue_name}/claims/{claim_id}"},
        ],
    ),

    # Subscriptions
    base.APIRule(
        name="messaging:subscriptions:get",
        check_str=f"rule:zaqar_project_reader or ({SYSTEM_READER}) or ({SYSTEM_ADMIN})",
        description="List and show subscriptions.",
        scope_types=["project", "system"],
        operations=[
            {"method": "GET", "path": "/v2/queues/{queue_name}/subscriptions"},
            {"method": "GET", "path": "/v2/queues/{queue_name}/subscriptions/{sub_id}"},
        ],
    ),
    base.APIRule(
        name="messaging:subscriptions:create",
        check_str=f"rule:zaqar_project_member or ({SYSTEM_ADMIN})",
        description="Create a subscription.",
        scope_types=["project", "system"],
        operations=[
            {"method": "POST", "path": "/v2/queues/{queue_name}/subscriptions"},
        ],
    ),
    base.APIRule(
        name="messaging:subscriptions:update",
        check_str=f"rule:zaqar_project_member or ({SYSTEM_ADMIN})",
        description="Update a subscription.",
        scope_types=["project", "system"],
        operations=[
            {"method": "PATCH", "path": "/v2/queues/{queue_name}/subscriptions/{sub_id}"},
        ],
    ),
    base.APIRule(
        name="messaging:subscriptions:delete",
        check_str=f"rule:zaqar_project_member or ({SYSTEM_ADMIN})",
        description="Delete a subscription.",
        scope_types=["project", "system"],
        operations=[
            {"method": "DELETE", "path": "/v2/queues/{queue_name}/subscriptions/{sub_id}"},
        ],
    ),
)

__all__ = ("list_rules",)
