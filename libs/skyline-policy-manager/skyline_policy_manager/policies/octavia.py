# flake8: noqa

from . import base

list_rules = (
    base.Rule(
        name="system-admin",
        check_str=("role:admin and system_scope:all"),
        description="No description",
    ),
    base.Rule(
        name="system-reader",
        check_str=("role:reader and system_scope:all"),
        description="No description",
    ),
    base.Rule(
        name="project-member",
        check_str=("role:member and project_id:%(project_id)s"),
        description="No description",
    ),
    base.Rule(
        name="project-reader",
        check_str=("role:reader and project_id:%(project_id)s"),
        description="No description",
    ),
    base.Rule(
        name="context_is_admin",
        check_str=("role:load-balancer_admin or rule:system-admin"),
        description="No description",
    ),
    base.Rule(
        name="load-balancer:owner",
        check_str=("project_id:%(project_id)s"),
        description="No description",
    ),
    base.Rule(
        name="load-balancer:observer_and_owner",
        check_str=("role:load-balancer_observer and rule:project-reader"),
        description="No description",
    ),
    base.Rule(
        name="load-balancer:global_observer",
        check_str=("role:load-balancer_global_observer or rule:system-reader"),
        description="No description",
    ),
    base.Rule(
        name="load-balancer:member_and_owner",
        check_str=("role:load-balancer_member and rule:project-member"),
        description="No description",
    ),
    base.Rule(
        name="load-balancer:admin",
        check_str=("is_admin:True or role:load-balancer_admin or rule:system-admin"),
        description="No description",
    ),
    base.Rule(
        name="load-balancer:read",
        check_str=(
            "rule:load-balancer:observer_and_owner or rule:load-balancer:global_observer or rule:load-balancer:member_and_owner or rule:load-balancer:admin"
        ),
        description="No description",
    ),
    base.Rule(
        name="load-balancer:read-global",
        check_str=("rule:load-balancer:global_observer or rule:load-balancer:admin"),
        description="No description",
    ),
    base.Rule(
        name="load-balancer:write",
        check_str=("rule:load-balancer:member_and_owner or rule:load-balancer:admin"),
        description="No description",
    ),
    base.Rule(
        name="load-balancer:read-quota",
        check_str=(
            "rule:load-balancer:observer_and_owner or rule:load-balancer:global_observer or rule:load-balancer:member_and_owner or role:load-balancer_quota_admin or rule:load-balancer:admin"
        ),
        description="No description",
    ),
    base.Rule(
        name="load-balancer:read-quota-global",
        check_str=(
            "rule:load-balancer:global_observer or role:load-balancer_quota_admin or rule:load-balancer:admin"
        ),
        description="No description",
    ),
    base.Rule(
        name="load-balancer:write-quota",
        check_str=("role:load-balancer_quota_admin or rule:load-balancer:admin"),
        description="No description",
    ),
    base.APIRule(
        name="os_load-balancer_api:flavor:get_all",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List Flavors",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2.0/lbaas/flavors"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:flavor:post",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin"),
        description="Create a Flavor",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/v2.0/lbaas/flavors"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:flavor:put",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin"),
        description="Update a Flavor",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/v2.0/lbaas/flavors/{flavor_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:flavor:get_one",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show Flavor details",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2.0/lbaas/flavors/{flavor_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:flavor:delete",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin"),
        description="Remove a Flavor",
        scope_types=["project"],
        operations=[{"method": "DELETE", "path": "/v2.0/lbaas/flavors/{flavor_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:flavor-profile:get_all",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin or role:reader"),
        description="List Flavor Profiles",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2.0/lbaas/flavorprofiles"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:flavor-profile:post",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin"),
        description="Create a Flavor Profile",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/v2.0/lbaas/flavorprofiles"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:flavor-profile:put",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin"),
        description="Update a Flavor Profile",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/v2.0/lbaas/flavorprofiles/{flavor_profile_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:flavor-profile:get_one",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin or role:reader"),
        description="Show Flavor Profile details",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2.0/lbaas/flavorprofiles/{flavor_profile_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:flavor-profile:delete",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin"),
        description="Remove a Flavor Profile",
        scope_types=["project"],
        operations=[
            {"method": "DELETE", "path": "/v2.0/lbaas/flavorprofiles/{flavor_profile_id}"},
        ],
    ),
    base.APIRule(
        name="os_load-balancer_api:availability-zone:get_all",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List Availability Zones",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2.0/lbaas/availabilityzones"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:availability-zone:post",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin"),
        description="Create an Availability Zone",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/v2.0/lbaas/availabilityzones"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:availability-zone:put",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin"),
        description="Update an Availability Zone",
        scope_types=["project"],
        operations=[
            {"method": "PUT", "path": "/v2.0/lbaas/availabilityzones/{availability_zone_id}"},
        ],
    ),
    base.APIRule(
        name="os_load-balancer_api:availability-zone:get_one",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show Availability Zone details",
        scope_types=["project"],
        operations=[
            {"method": "GET", "path": "/v2.0/lbaas/availabilityzones/{availability_zone_id}"},
        ],
    ),
    base.APIRule(
        name="os_load-balancer_api:availability-zone:delete",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin"),
        description="Remove an Availability Zone",
        scope_types=["project"],
        operations=[
            {"method": "DELETE", "path": "/v2.0/lbaas/availabilityzones/{availability_zone_id}"},
        ],
    ),
    base.APIRule(
        name="os_load-balancer_api:availability-zone-profile:get_all",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin or role:reader"),
        description="List Availability Zones",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2.0/lbaas/availabilityzoneprofiles"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:availability-zone-profile:post",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin"),
        description="Create an Availability Zone",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/v2.0/lbaas/availabilityzoneprofiles"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:availability-zone-profile:put",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin"),
        description="Update an Availability Zone",
        scope_types=["project"],
        operations=[
            {
                "method": "PUT",
                "path": "/v2.0/lbaas/availabilityzoneprofiles/{availability_zone_profile_id}",
            },
        ],
    ),
    base.APIRule(
        name="os_load-balancer_api:availability-zone-profile:get_one",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin or role:reader"),
        description="Show Availability Zone details",
        scope_types=["project"],
        operations=[
            {
                "method": "GET",
                "path": "/v2.0/lbaas/availabilityzoneprofiles/{availability_zone_profile_id}",
            },
        ],
    ),
    base.APIRule(
        name="os_load-balancer_api:availability-zone-profile:delete",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin"),
        description="Remove an Availability Zone",
        scope_types=["project"],
        operations=[
            {
                "method": "DELETE",
                "path": "/v2.0/lbaas/availabilityzoneprofiles/{availability_zone_profile_id}",
            },
        ],
    ),
    base.APIRule(
        name="os_load-balancer_api:healthmonitor:get_all",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List Health Monitors of a Pool",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/healthmonitors"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:healthmonitor:get_all-global",
        check_str=("rule:load-balancer:read-global"),
        basic_check_str=("role:admin or role:reader"),
        description="List Health Monitors including resources owned by others",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/healthmonitors"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:healthmonitor:post",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a Health Monitor",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/v2/lbaas/healthmonitors"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:healthmonitor:get_one",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show Health Monitor details",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/healthmonitors/{healthmonitor_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:healthmonitor:put",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a Health Monitor",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/v2/lbaas/healthmonitors/{healthmonitor_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:healthmonitor:delete",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Remove a Health Monitor",
        scope_types=["project"],
        operations=[{"method": "DELETE", "path": "/v2/lbaas/healthmonitors/{healthmonitor_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:l7policy:get_all",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List L7 Policys",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/l7policies"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:l7policy:get_all-global",
        check_str=("rule:load-balancer:read-global"),
        basic_check_str=("role:admin or role:reader"),
        description="List L7 Policys including resources owned by others",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/l7policies"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:l7policy:post",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a L7 Policy",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/v2/lbaas/l7policies"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:l7policy:get_one",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show L7 Policy details",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/l7policies/{l7policy_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:l7policy:put",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a L7 Policy",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/v2/lbaas/l7policies/{l7policy_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:l7policy:delete",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Remove a L7 Policy",
        scope_types=["project"],
        operations=[{"method": "DELETE", "path": "/v2/lbaas/l7policies/{l7policy_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:l7rule:get_all",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List L7 Rules",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/l7policies/{l7policy_id}/rules"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:l7rule:post",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a L7 Rule",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/v2/lbaas/l7policies/{l7policy_id}/rules"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:l7rule:get_one",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show L7 Rule details",
        scope_types=["project"],
        operations=[
            {"method": "GET", "path": "/v2/lbaas/l7policies/{l7policy_id}/rules/{l7rule_id}"},
        ],
    ),
    base.APIRule(
        name="os_load-balancer_api:l7rule:put",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a L7 Rule",
        scope_types=["project"],
        operations=[
            {"method": "PUT", "path": "/v2/lbaas/l7policies/{l7policy_id}/rules/{l7rule_id}"},
        ],
    ),
    base.APIRule(
        name="os_load-balancer_api:l7rule:delete",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Remove a L7 Rule",
        scope_types=["project"],
        operations=[
            {"method": "DELETE", "path": "/v2/lbaas/l7policies/{l7policy_id}/rules/{l7rule_id}"},
        ],
    ),
    base.APIRule(
        name="os_load-balancer_api:listener:get_all",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List Listeners",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/listeners"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:listener:get_all-global",
        check_str=("rule:load-balancer:read-global"),
        basic_check_str=("role:admin or role:reader"),
        description="List Listeners including resources owned by others",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/listeners"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:listener:post",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a Listener",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/v2/lbaas/listeners"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:listener:get_one",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show Listener details",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/listeners/{listener_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:listener:put",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a Listener",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/v2/lbaas/listeners/{listener_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:listener:delete",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Remove a Listener",
        scope_types=["project"],
        operations=[{"method": "DELETE", "path": "/v2/lbaas/listeners/{listener_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:listener:get_stats",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show Listener statistics",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/listeners/{listener_id}/stats"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:loadbalancer:get_all",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List Load Balancers",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/loadbalancers"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:loadbalancer:get_all-global",
        check_str=("rule:load-balancer:read-global"),
        basic_check_str=("role:admin or role:reader"),
        description="List Load Balancers including resources owned by others",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/loadbalancers"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:loadbalancer:post",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a Load Balancer",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/v2/lbaas/loadbalancers"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:loadbalancer:get_one",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show Load Balancer details",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/loadbalancers/{loadbalancer_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:loadbalancer:put",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a Load Balancer",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/v2/lbaas/loadbalancers/{loadbalancer_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:loadbalancer:delete",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Remove a Load Balancer",
        scope_types=["project"],
        operations=[{"method": "DELETE", "path": "/v2/lbaas/loadbalancers/{loadbalancer_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:loadbalancer:get_stats",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show Load Balancer statistics",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/loadbalancers/{loadbalancer_id}/stats"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:loadbalancer:get_status",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show Load Balancer status",
        scope_types=["project"],
        operations=[
            {"method": "GET", "path": "/v2/lbaas/loadbalancers/{loadbalancer_id}/status"},
        ],
    ),
    base.APIRule(
        name="os_load-balancer_api:loadbalancer:put_failover",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin"),
        description="Failover a Load Balancer",
        scope_types=["project"],
        operations=[
            {"method": "PUT", "path": "/v2/lbaas/loadbalancers/{loadbalancer_id}/failover"},
        ],
    ),
    base.APIRule(
        name="os_load-balancer_api:member:get_all",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List Members of a Pool",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/pools/{pool_id}/members"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:member:post",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a Member",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/v2/lbaas/pools/{pool_id}/members"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:member:get_one",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show Member details",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/pools/{pool_id}/members/{member_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:member:put",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a Member",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/v2/lbaas/pools/{pool_id}/members/{member_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:member:delete",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Remove a Member",
        scope_types=["project"],
        operations=[
            {"method": "DELETE", "path": "/v2/lbaas/pools/{pool_id}/members/{member_id}"},
        ],
    ),
    base.APIRule(
        name="os_load-balancer_api:pool:get_all",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List Pools",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/pools"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:pool:get_all-global",
        check_str=("rule:load-balancer:read-global"),
        basic_check_str=("role:admin or role:reader"),
        description="List Pools including resources owned by others",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/pools"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:pool:post",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a Pool",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/v2/lbaas/pools"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:pool:get_one",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show Pool details",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/pools/{pool_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:pool:put",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a Pool",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/v2/lbaas/pools/{pool_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:pool:delete",
        check_str=("rule:load-balancer:write"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Remove a Pool",
        scope_types=["project"],
        operations=[{"method": "DELETE", "path": "/v2/lbaas/pools/{pool_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:provider:get_all",
        check_str=("rule:load-balancer:read"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List enabled providers",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/providers"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:quota:get_all",
        check_str=("rule:load-balancer:read-quota"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List Quotas",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/quotas"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:quota:get_all-global",
        check_str=("rule:load-balancer:read-quota-global"),
        basic_check_str=("role:admin or role:reader"),
        description="List Quotas including resources owned by others",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/quotas"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:quota:get_one",
        check_str=("rule:load-balancer:read-quota"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show Quota details",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/quotas/{project_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:quota:put",
        check_str=("rule:load-balancer:write-quota"),
        basic_check_str=("role:admin"),
        description="Update a Quota",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/v2/lbaas/quotas/{project_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:quota:delete",
        check_str=("rule:load-balancer:write-quota"),
        basic_check_str=("role:admin"),
        description="Reset a Quota",
        scope_types=["project"],
        operations=[{"method": "DELETE", "path": "/v2/lbaas/quotas/{project_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:quota:get_defaults",
        check_str=("rule:load-balancer:read-quota"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show Default Quota for a Project",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/lbaas/quotas/{project_id}/default"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:amphora:get_all",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin or role:reader"),
        description="List Amphorae",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/octavia/amphorae"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:amphora:get_one",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin or role:reader"),
        description="Show Amphora details",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/octavia/amphorae/{amphora_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:amphora:delete",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin"),
        description="Delete an Amphora",
        scope_types=["project"],
        operations=[{"method": "DELETE", "path": "/v2/octavia/amphorae/{amphora_id}"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:amphora:put_config",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin"),
        description="Update Amphora Agent Configuration",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/v2/octavia/amphorae/{amphora_id}/config"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:amphora:put_failover",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin"),
        description="Failover Amphora",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/v2/octavia/amphorae/{amphora_id}/failover"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:amphora:get_stats",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin or role:reader"),
        description="Show Amphora statistics",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v2/octavia/amphorae/{amphora_id}/stats"}],
    ),
    base.APIRule(
        name="os_load-balancer_api:provider-flavor:get_all",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin or role:reader"),
        description="List the provider flavor capabilities.",
        scope_types=["project"],
        operations=[
            {"method": "GET", "path": "/v2/lbaas/providers/{provider}/flavor_capabilities"},
        ],
    ),
    base.APIRule(
        name="os_load-balancer_api:provider-availability-zone:get_all",
        check_str=("rule:load-balancer:admin"),
        basic_check_str=("role:admin or role:reader"),
        description="List the provider availability zone capabilities.",
        scope_types=["project"],
        operations=[
            {
                "method": "GET",
                "path": "/v2/lbaas/providers/{provider}/availability_zone_capabilities",
            },
        ],
    ),
)

__all__ = ("list_rules",)
