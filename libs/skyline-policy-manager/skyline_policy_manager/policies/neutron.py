# flake8: noqa

from . import base

list_rules = (
    base.Rule(
        name="context_is_admin",
        check_str=("role:admin"),
        description="Rule for cloud admin access",
    ),
    base.Rule(
        name="owner",
        check_str=("tenant_id:%(tenant_id)s"),
        description="Rule for resource owner access",
    ),
    base.Rule(
        name="admin_or_owner",
        check_str=("rule:context_is_admin or rule:owner"),
        description="Rule for admin or owner access",
    ),
    base.Rule(
        name="context_is_advsvc",
        check_str=("role:advsvc"),
        description="Rule for advsvc role access",
    ),
    base.Rule(
        name="admin_or_network_owner",
        check_str=("rule:context_is_admin or tenant_id:%(network:tenant_id)s"),
        description="Rule for admin or network owner access",
    ),
    base.Rule(
        name="admin_owner_or_network_owner",
        check_str=("rule:owner or rule:admin_or_network_owner"),
        description="Rule for resource owner, admin or network owner access",
    ),
    base.Rule(
        name="network_owner",
        check_str=("tenant_id:%(network:tenant_id)s"),
        description="Rule for network owner access",
    ),
    base.Rule(
        name="admin_only",
        check_str=("rule:context_is_admin"),
        description="Rule for admin-only access",
    ),
    base.Rule(
        name="regular_user",
        check_str=(""),
        description="Rule for regular user access",
    ),
    base.Rule(
        name="shared",
        check_str=("field:networks:shared=True"),
        description="Rule of shared network",
    ),
    base.Rule(
        name="default",
        check_str=("rule:admin_or_owner"),
        description="Default access rule",
    ),
    base.Rule(
        name="admin_or_ext_parent_owner",
        check_str=("rule:context_is_admin or tenant_id:%(ext_parent:tenant_id)s"),
        description="Rule for common parent owner check",
    ),
    base.Rule(
        name="ext_parent_owner",
        check_str=("tenant_id:%(ext_parent:tenant_id)s"),
        description="Rule for common parent owner check",
    ),
    base.Rule(
        name="sg_owner",
        check_str=("tenant_id:%(security_group:tenant_id)s"),
        description="Rule for security group owner access",
    ),
    base.Rule(
        name="shared_address_groups",
        check_str=("field:address_groups:shared=True"),
        description="Definition of a shared address group",
    ),
    base.Rule(
        name="shared_address_scopes",
        check_str=("field:address_scopes:shared=True"),
        description="Definition of a shared address scope",
    ),
    base.Rule(
        name="get_flavor_service_profile",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s)"
        ),
        description="Get a flavor associated with a given service profiles. There is no corresponding GET operations in API currently. This rule is currently referred only in the DELETE of flavor_service_profile.",
    ),
    base.Rule(
        name="external",
        check_str=("field:networks:router:external=True"),
        description="Definition of an external network",
    ),
    base.Rule(
        name="network_device",
        check_str=("field:port:device_owner=~^network:"),
        description="Definition of port with network device_owner",
    ),
    base.Rule(
        name="admin_or_data_plane_int",
        check_str=("rule:context_is_admin or role:data_plane_integrator"),
        description="Rule for data plane integration",
    ),
    base.Rule(
        name="restrict_wildcard",
        check_str=("(not field:rbac_policy:target_tenant=*) or rule:admin_only"),
        description="Definition of a wildcard target_tenant",
    ),
    base.Rule(
        name="admin_or_sg_owner",
        check_str=("rule:context_is_admin or tenant_id:%(security_group:tenant_id)s"),
        description="Rule for admin or security group owner access",
    ),
    base.Rule(
        name="admin_owner_or_sg_owner",
        check_str=("rule:owner or rule:admin_or_sg_owner"),
        description="Rule for resource owner, admin or security group owner access",
    ),
    base.Rule(
        name="shared_subnetpools",
        check_str=("field:subnetpools:shared=True"),
        description="Definition of a shared subnetpool",
    ),
    base.APIRule(
        name="get_address_group",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s) or rule:shared_address_groups"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get an address group",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/address-groups"},
            {"method": "GET", "path": "/address-groups/{id}"},
        ],
    ),
    base.APIRule(
        name="create_address_scope",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create an address scope",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/address-scopes"}],
    ),
    base.APIRule(
        name="create_address_scope:shared",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create a shared address scope",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/address-scopes"}],
    ),
    base.APIRule(
        name="get_address_scope",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s) or rule:shared_address_scopes"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get an address scope",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/address-scopes"},
            {"method": "GET", "path": "/address-scopes/{id}"},
        ],
    ),
    base.APIRule(
        name="update_address_scope",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update an address scope",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/address-scopes/{id}"}],
    ),
    base.APIRule(
        name="update_address_scope:shared",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update ``shared`` attribute of an address scope",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/address-scopes/{id}"}],
    ),
    base.APIRule(
        name="delete_address_scope",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete an address scope",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/address-scopes/{id}"}],
    ),
    base.APIRule(
        name="get_agent",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get an agent",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/agents"},
            {"method": "GET", "path": "/agents/{id}"},
        ],
    ),
    base.APIRule(
        name="update_agent",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update an agent",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/agents/{id}"}],
    ),
    base.APIRule(
        name="delete_agent",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete an agent",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/agents/{id}"}],
    ),
    base.APIRule(
        name="create_dhcp-network",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Add a network to a DHCP agent",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/agents/{agent_id}/dhcp-networks"}],
    ),
    base.APIRule(
        name="get_dhcp-networks",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List networks on a DHCP agent",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/agents/{agent_id}/dhcp-networks"}],
    ),
    base.APIRule(
        name="delete_dhcp-network",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Remove a network from a DHCP agent",
        scope_types=["system"],
        operations=[
            {"method": "DELETE", "path": "/agents/{agent_id}/dhcp-networks/{network_id}"},
        ],
    ),
    base.APIRule(
        name="create_l3-router",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Add a router to an L3 agent",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/agents/{agent_id}/l3-routers"}],
    ),
    base.APIRule(
        name="get_l3-routers",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List routers on an L3 agent",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/agents/{agent_id}/l3-routers"}],
    ),
    base.APIRule(
        name="delete_l3-router",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Remove a router from an L3 agent",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/agents/{agent_id}/l3-routers/{router_id}"}],
    ),
    base.APIRule(
        name="get_dhcp-agents",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List DHCP agents hosting a network",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/networks/{network_id}/dhcp-agents"}],
    ),
    base.APIRule(
        name="get_l3-agents",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List L3 agents hosting a router",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/routers/{router_id}/l3-agents"}],
    ),
    base.APIRule(
        name="get_auto_allocated_topology",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a project's auto-allocated topology",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/auto-allocated-topology/{project_id}"}],
    ),
    base.APIRule(
        name="delete_auto_allocated_topology",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete a project's auto-allocated topology",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/auto-allocated-topology/{project_id}"}],
    ),
    base.APIRule(
        name="get_availability_zone",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("@"),
        description="List availability zones",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/availability_zones"}],
    ),
    base.APIRule(
        name="create_flavor",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create a flavor",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/flavors"}],
    ),
    base.APIRule(
        name="get_flavor",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a flavor",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/flavors"},
            {"method": "GET", "path": "/flavors/{id}"},
        ],
    ),
    base.APIRule(
        name="update_flavor",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update a flavor",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/flavors/{id}"}],
    ),
    base.APIRule(
        name="delete_flavor",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete a flavor",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/flavors/{id}"}],
    ),
    base.APIRule(
        name="create_service_profile",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create a service profile",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/service_profiles"}],
    ),
    base.APIRule(
        name="get_service_profile",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get a service profile",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/service_profiles"},
            {"method": "GET", "path": "/service_profiles/{id}"},
        ],
    ),
    base.APIRule(
        name="update_service_profile",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update a service profile",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/service_profiles/{id}"}],
    ),
    base.APIRule(
        name="delete_service_profile",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete a service profile",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/service_profiles/{id}"}],
    ),
    base.APIRule(
        name="create_flavor_service_profile",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Associate a flavor with a service profile",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/flavors/{flavor_id}/service_profiles"}],
    ),
    base.APIRule(
        name="delete_flavor_service_profile",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Disassociate a flavor with a service profile",
        scope_types=["system"],
        operations=[
            {"method": "DELETE", "path": "/flavors/{flavor_id}/service_profiles/{profile_id}"},
        ],
    ),
    base.APIRule(
        name="create_floatingip",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a floating IP",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/floatingips"}],
    ),
    base.APIRule(
        name="create_floatingip:floating_ip_address",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a floating IP with a specific IP address",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/floatingips"}],
    ),
    base.APIRule(
        name="get_floatingip",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a floating IP",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/floatingips"},
            {"method": "GET", "path": "/floatingips/{id}"},
        ],
    ),
    base.APIRule(
        name="update_floatingip",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a floating IP",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/floatingips/{id}"}],
    ),
    base.APIRule(
        name="delete_floatingip",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete a floating IP",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/floatingips/{id}"}],
    ),
    base.APIRule(
        name="get_floatingip_pool",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get floating IP pools",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/floatingip_pools"}],
    ),
    base.APIRule(
        name="create_floatingip_port_forwarding",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s) or rule:ext_parent_owner"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a floating IP port forwarding",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/floatingips/{floatingip_id}/port_forwardings"}],
    ),
    base.APIRule(
        name="get_floatingip_port_forwarding",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s) or rule:ext_parent_owner"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a floating IP port forwarding",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/floatingips/{floatingip_id}/port_forwardings"},
            {
                "method": "GET",
                "path": "/floatingips/{floatingip_id}/port_forwardings/{port_forwarding_id}",
            },
        ],
    ),
    base.APIRule(
        name="update_floatingip_port_forwarding",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s) or rule:ext_parent_owner"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a floating IP port forwarding",
        scope_types=["system", "project"],
        operations=[
            {
                "method": "PUT",
                "path": "/floatingips/{floatingip_id}/port_forwardings/{port_forwarding_id}",
            },
        ],
    ),
    base.APIRule(
        name="delete_floatingip_port_forwarding",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s) or rule:ext_parent_owner"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete a floating IP port forwarding",
        scope_types=["system", "project"],
        operations=[
            {
                "method": "DELETE",
                "path": "/floatingips/{floatingip_id}/port_forwardings/{port_forwarding_id}",
            },
        ],
    ),
    base.APIRule(
        name="create_router_conntrack_helper",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s) or rule:ext_parent_owner"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a router conntrack helper",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/routers/{router_id}/conntrack_helpers"}],
    ),
    base.APIRule(
        name="get_router_conntrack_helper",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s) or rule:ext_parent_owner"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a router conntrack helper",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/routers/{router_id}/conntrack_helpers"},
            {
                "method": "GET",
                "path": "/routers/{router_id}/conntrack_helpers/{conntrack_helper_id}",
            },
        ],
    ),
    base.APIRule(
        name="update_router_conntrack_helper",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s) or rule:ext_parent_owner"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a router conntrack helper",
        scope_types=["system", "project"],
        operations=[
            {
                "method": "PUT",
                "path": "/routers/{router_id}/conntrack_helpers/{conntrack_helper_id}",
            },
        ],
    ),
    base.APIRule(
        name="delete_router_conntrack_helper",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s) or rule:ext_parent_owner"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete a router conntrack helper",
        scope_types=["system", "project"],
        operations=[
            {
                "method": "DELETE",
                "path": "/routers/{router_id}/conntrack_helpers/{conntrack_helper_id}",
            },
        ],
    ),
    base.APIRule(
        name="get_loggable_resource",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get loggable resources",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/log/loggable-resources"}],
    ),
    base.APIRule(
        name="create_log",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create a network log",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/log/logs"}],
    ),
    base.APIRule(
        name="get_log",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get a network log",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/log/logs"},
            {"method": "GET", "path": "/log/logs/{id}"},
        ],
    ),
    base.APIRule(
        name="update_log",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update a network log",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/log/logs/{id}"}],
    ),
    base.APIRule(
        name="delete_log",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete a network log",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/log/logs/{id}"}],
    ),
    base.APIRule(
        name="create_metering_label",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create a metering label",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/metering/metering-labels"}],
    ),
    base.APIRule(
        name="get_metering_label",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get a metering label",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/metering/metering-labels"},
            {"method": "GET", "path": "/metering/metering-labels/{id}"},
        ],
    ),
    base.APIRule(
        name="delete_metering_label",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete a metering label",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/metering/metering-labels/{id}"}],
    ),
    base.APIRule(
        name="create_metering_label_rule",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create a metering label rule",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/metering/metering-label-rules"}],
    ),
    base.APIRule(
        name="get_metering_label_rule",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get a metering label rule",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/metering/metering-label-rules"},
            {"method": "GET", "path": "/metering/metering-label-rules/{id}"},
        ],
    ),
    base.APIRule(
        name="delete_metering_label_rule",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete a metering label rule",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/metering/metering-label-rules/{id}"}],
    ),
    base.APIRule(
        name="create_network",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a network",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/networks"}],
    ),
    base.APIRule(
        name="create_network:shared",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create a shared network",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/networks"}],
    ),
    base.APIRule(
        name="create_network:router:external",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create an external network",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/networks"}],
    ),
    base.APIRule(
        name="create_network:is_default",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Specify ``is_default`` attribute when creating a network",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/networks"}],
    ),
    base.APIRule(
        name="create_network:port_security_enabled",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Specify ``port_security_enabled`` attribute when creating a network",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/networks"}],
    ),
    base.APIRule(
        name="create_network:segments",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Specify ``segments`` attribute when creating a network",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/networks"}],
    ),
    base.APIRule(
        name="create_network:provider:network_type",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Specify ``provider:network_type`` when creating a network",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/networks"}],
    ),
    base.APIRule(
        name="create_network:provider:physical_network",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Specify ``provider:physical_network`` when creating a network",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/networks"}],
    ),
    base.APIRule(
        name="create_network:provider:segmentation_id",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Specify ``provider:segmentation_id`` when creating a network",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/networks"}],
    ),
    base.APIRule(
        name="get_network",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s) or rule:shared or rule:external or rule:context_is_advsvc"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a network",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/networks"},
            {"method": "GET", "path": "/networks/{id}"},
        ],
    ),
    base.APIRule(
        name="get_network:router:external",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s)"
        ),
        basic_check_str=("@"),
        description="Get ``router:external`` attribute of a network",
        scope_types=["project"],
        operations=[
            {"method": "GET", "path": "/networks"},
            {"method": "GET", "path": "/networks/{id}"},
        ],
    ),
    base.APIRule(
        name="get_network:segments",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get ``segments`` attribute of a network",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/networks"},
            {"method": "GET", "path": "/networks/{id}"},
        ],
    ),
    base.APIRule(
        name="get_network:provider:network_type",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get ``provider:network_type`` attribute of a network",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/networks"},
            {"method": "GET", "path": "/networks/{id}"},
        ],
    ),
    base.APIRule(
        name="get_network:provider:physical_network",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get ``provider:physical_network`` attribute of a network",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/networks"},
            {"method": "GET", "path": "/networks/{id}"},
        ],
    ),
    base.APIRule(
        name="get_network:provider:segmentation_id",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get ``provider:segmentation_id`` attribute of a network",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/networks"},
            {"method": "GET", "path": "/networks/{id}"},
        ],
    ),
    base.APIRule(
        name="update_network",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a network",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/networks/{id}"}],
    ),
    base.APIRule(
        name="update_network:segments",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update ``segments`` attribute of a network",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/networks/{id}"}],
    ),
    base.APIRule(
        name="update_network:shared",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update ``shared`` attribute of a network",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/networks/{id}"}],
    ),
    base.APIRule(
        name="update_network:provider:network_type",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update ``provider:network_type`` attribute of a network",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/networks/{id}"}],
    ),
    base.APIRule(
        name="update_network:provider:physical_network",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update ``provider:physical_network`` attribute of a network",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/networks/{id}"}],
    ),
    base.APIRule(
        name="update_network:provider:segmentation_id",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update ``provider:segmentation_id`` attribute of a network",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/networks/{id}"}],
    ),
    base.APIRule(
        name="update_network:router:external",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update ``router:external`` attribute of a network",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/networks/{id}"}],
    ),
    base.APIRule(
        name="update_network:is_default",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update ``is_default`` attribute of a network",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/networks/{id}"}],
    ),
    base.APIRule(
        name="update_network:port_security_enabled",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update ``port_security_enabled`` attribute of a network",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/networks/{id}"}],
    ),
    base.APIRule(
        name="delete_network",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete a network",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/networks/{id}"}],
    ),
    base.APIRule(
        name="get_network_ip_availability",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get network IP availability",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/network-ip-availabilities"},
            {"method": "GET", "path": "/network-ip-availabilities/{network_id}"},
        ],
    ),
    base.APIRule(
        name="create_network_segment_range",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create a network segment range",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/network_segment_ranges"}],
    ),
    base.APIRule(
        name="get_network_segment_range",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get a network segment range",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/network_segment_ranges"},
            {"method": "GET", "path": "/network_segment_ranges/{id}"},
        ],
    ),
    base.APIRule(
        name="update_network_segment_range",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update a network segment range",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/network_segment_ranges/{id}"}],
    ),
    base.APIRule(
        name="delete_network_segment_range",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete a network segment range",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/network_segment_ranges/{id}"}],
    ),
    base.APIRule(
        name="create_port",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a port",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/ports"}],
    ),
    base.APIRule(
        name="create_port:device_owner",
        check_str=(
            "not rule:network_device or role:admin and system_scope:all or role:admin and project_id:%(project_id)s or rule:context_is_advsvc or rule:network_owner"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Specify ``device_owner`` attribute when creting a port",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/ports"}],
    ),
    base.APIRule(
        name="create_port:mac_address",
        check_str=(
            "rule:context_is_advsvc or rule:network_owner or role:admin and system_scope:all or role:admin and project_id:%(project_id)s"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Specify ``mac_address`` attribute when creating a port",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/ports"}],
    ),
    base.APIRule(
        name="create_port:fixed_ips",
        check_str=(
            "rule:context_is_advsvc or rule:network_owner or role:admin and system_scope:all or role:admin and project_id:%(project_id)s or rule:shared"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Specify ``fixed_ips`` information when creating a port",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/ports"}],
    ),
    base.APIRule(
        name="create_port:fixed_ips:ip_address",
        check_str=(
            "rule:context_is_advsvc or rule:network_owner or role:admin and system_scope:all or role:admin and project_id:%(project_id)s"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Specify IP address in ``fixed_ips`` when creating a port",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/ports"}],
    ),
    base.APIRule(
        name="create_port:fixed_ips:subnet_id",
        check_str=(
            "rule:context_is_advsvc or rule:network_owner or role:admin and system_scope:all or role:admin and project_id:%(project_id)s or rule:shared"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Specify subnet ID in ``fixed_ips`` when creating a port",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/ports"}],
    ),
    base.APIRule(
        name="create_port:port_security_enabled",
        check_str=(
            "rule:context_is_advsvc or rule:network_owner or role:admin and system_scope:all or role:admin and project_id:%(project_id)s"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Specify ``port_security_enabled`` attribute when creating a port",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/ports"}],
    ),
    base.APIRule(
        name="create_port:binding:host_id",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Specify ``binding:host_id`` attribute when creating a port",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/ports"}],
    ),
    base.APIRule(
        name="create_port:binding:profile",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Specify ``binding:profile`` attribute when creating a port",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/ports"}],
    ),
    base.APIRule(
        name="create_port:binding:vnic_type",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Specify ``binding:vnic_type`` attribute when creating a port",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/ports"}],
    ),
    base.APIRule(
        name="create_port:allowed_address_pairs",
        check_str=(
            "role:admin and system_scope:all or role:admin and project_id:%(project_id)s or rule:network_owner"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Specify ``allowed_address_pairs`` attribute when creating a port",
        scope_types=["project", "system"],
        operations=[{"method": "POST", "path": "/ports"}],
    ),
    base.APIRule(
        name="create_port:allowed_address_pairs:mac_address",
        check_str=(
            "role:admin and system_scope:all or role:admin and project_id:%(project_id)s or rule:network_owner"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Specify ``mac_address` of `allowed_address_pairs`` attribute when creating a port",
        scope_types=["project", "system"],
        operations=[{"method": "POST", "path": "/ports"}],
    ),
    base.APIRule(
        name="create_port:allowed_address_pairs:ip_address",
        check_str=(
            "role:admin and system_scope:all or role:admin and project_id:%(project_id)s or rule:network_owner"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Specify ``ip_address`` of ``allowed_address_pairs`` attribute when creating a port",
        scope_types=["project", "system"],
        operations=[{"method": "POST", "path": "/ports"}],
    ),
    base.APIRule(
        name="get_port",
        check_str=(
            "rule:context_is_advsvc or (role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a port",
        scope_types=["project", "system"],
        operations=[
            {"method": "GET", "path": "/ports"},
            {"method": "GET", "path": "/ports/{id}"},
        ],
    ),
    base.APIRule(
        name="get_port:binding:vif_type",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get ``binding:vif_type`` attribute of a port",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/ports"},
            {"method": "GET", "path": "/ports/{id}"},
        ],
    ),
    base.APIRule(
        name="get_port:binding:vif_details",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get ``binding:vif_details`` attribute of a port",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/ports"},
            {"method": "GET", "path": "/ports/{id}"},
        ],
    ),
    base.APIRule(
        name="get_port:binding:host_id",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get ``binding:host_id`` attribute of a port",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/ports"},
            {"method": "GET", "path": "/ports/{id}"},
        ],
    ),
    base.APIRule(
        name="get_port:binding:profile",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get ``binding:profile`` attribute of a port",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/ports"},
            {"method": "GET", "path": "/ports/{id}"},
        ],
    ),
    base.APIRule(
        name="get_port:resource_request",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get ``resource_request`` attribute of a port",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/ports"},
            {"method": "GET", "path": "/ports/{id}"},
        ],
    ),
    base.APIRule(
        name="update_port",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s) or rule:context_is_advsvc"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a port",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/ports/{id}"}],
    ),
    base.APIRule(
        name="update_port:device_owner",
        check_str=(
            "not rule:network_device or rule:context_is_advsvc or rule:network_owner or role:admin and system_scope:all or role:admin and project_id:%(project_id)s"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update ``device_owner`` attribute of a port",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/ports/{id}"}],
    ),
    base.APIRule(
        name="update_port:mac_address",
        check_str=("role:admin and system_scope:all or rule:context_is_advsvc"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update ``mac_address`` attribute of a port",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/ports/{id}"}],
    ),
    base.APIRule(
        name="update_port:fixed_ips",
        check_str=(
            "rule:context_is_advsvc or rule:network_owner or role:admin and system_scope:all or role:admin and project_id:%(project_id)s"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Specify ``fixed_ips`` information when updating a port",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/ports/{id}"}],
    ),
    base.APIRule(
        name="update_port:fixed_ips:ip_address",
        check_str=(
            "rule:context_is_advsvc or rule:network_owner or role:admin and system_scope:all or role:admin and project_id:%(project_id)s"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Specify IP address in ``fixed_ips`` information when updating a port",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/ports/{id}"}],
    ),
    base.APIRule(
        name="update_port:fixed_ips:subnet_id",
        check_str=(
            "rule:context_is_advsvc or rule:network_owner or role:admin and system_scope:all or role:admin and project_id:%(project_id)s or rule:shared"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Specify subnet ID in ``fixed_ips`` information when updating a port",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/ports/{id}"}],
    ),
    base.APIRule(
        name="update_port:port_security_enabled",
        check_str=(
            "rule:context_is_advsvc or rule:network_owner or role:admin and system_scope:all or role:admin and project_id:%(project_id)s"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update ``port_security_enabled`` attribute of a port",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/ports/{id}"}],
    ),
    base.APIRule(
        name="update_port:binding:host_id",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update ``binding:host_id`` attribute of a port",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/ports/{id}"}],
    ),
    base.APIRule(
        name="update_port:binding:profile",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update ``binding:profile`` attribute of a port",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/ports/{id}"}],
    ),
    base.APIRule(
        name="update_port:binding:vnic_type",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s) or rule:context_is_advsvc"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update ``binding:vnic_type`` attribute of a port",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/ports/{id}"}],
    ),
    base.APIRule(
        name="update_port:allowed_address_pairs",
        check_str=(
            "role:admin and system_scope:all or role:admin and project_id:%(project_id)s or rule:network_owner"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update ``allowed_address_pairs`` attribute of a port",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/ports/{id}"}],
    ),
    base.APIRule(
        name="update_port:allowed_address_pairs:mac_address",
        check_str=(
            "role:admin and system_scope:all or role:admin and project_id:%(project_id)s or rule:network_owner"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update ``mac_address`` of ``allowed_address_pairs`` attribute of a port",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/ports/{id}"}],
    ),
    base.APIRule(
        name="update_port:allowed_address_pairs:ip_address",
        check_str=(
            "role:admin and system_scope:all or role:admin and project_id:%(project_id)s or rule:network_owner"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update ``ip_address`` of ``allowed_address_pairs`` attribute of a port",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/ports/{id}"}],
    ),
    base.APIRule(
        name="update_port:data_plane_status",
        check_str=("role:admin and system_scope:all or role:data_plane_integrator"),
        basic_check_str=("role:admin"),
        description="Update ``data_plane_status`` attribute of a port",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/ports/{id}"}],
    ),
    base.APIRule(
        name="delete_port",
        check_str=(
            "rule:context_is_advsvc or (role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete a port",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/ports/{id}"}],
    ),
    base.APIRule(
        name="get_policy",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s)"
        ),
        basic_check_str=("@"),
        description="Get QoS policies",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/qos/policies"},
            {"method": "GET", "path": "/qos/policies/{id}"},
        ],
    ),
    base.APIRule(
        name="create_policy",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create a QoS policy",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/qos/policies"}],
    ),
    base.APIRule(
        name="update_policy",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update a QoS policy",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/qos/policies/{id}"}],
    ),
    base.APIRule(
        name="delete_policy",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete a QoS policy",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/qos/policies/{id}"}],
    ),
    base.APIRule(
        name="get_rule_type",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get available QoS rule types",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/qos/rule-types"},
            {"method": "GET", "path": "/qos/rule-types/{rule_type}"},
        ],
    ),
    base.APIRule(
        name="get_policy_bandwidth_limit_rule",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a QoS bandwidth limit rule",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/qos/policies/{policy_id}/bandwidth_limit_rules"},
            {
                "method": "GET",
                "path": "/qos/policies/{policy_id}/bandwidth_limit_rules/{rule_id}",
            },
        ],
    ),
    base.APIRule(
        name="create_policy_bandwidth_limit_rule",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create a QoS bandwidth limit rule",
        scope_types=["system"],
        operations=[
            {"method": "POST", "path": "/qos/policies/{policy_id}/bandwidth_limit_rules"},
        ],
    ),
    base.APIRule(
        name="update_policy_bandwidth_limit_rule",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update a QoS bandwidth limit rule",
        scope_types=["system"],
        operations=[
            {
                "method": "PUT",
                "path": "/qos/policies/{policy_id}/bandwidth_limit_rules/{rule_id}",
            },
        ],
    ),
    base.APIRule(
        name="delete_policy_bandwidth_limit_rule",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete a QoS bandwidth limit rule",
        scope_types=["system"],
        operations=[
            {
                "method": "DELETE",
                "path": "/qos/policies/{policy_id}/bandwidth_limit_rules/{rule_id}",
            },
        ],
    ),
    base.APIRule(
        name="get_policy_dscp_marking_rule",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a QoS DSCP marking rule",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/qos/policies/{policy_id}/dscp_marking_rules"},
            {"method": "GET", "path": "/qos/policies/{policy_id}/dscp_marking_rules/{rule_id}"},
        ],
    ),
    base.APIRule(
        name="create_policy_dscp_marking_rule",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create a QoS DSCP marking rule",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/qos/policies/{policy_id}/dscp_marking_rules"}],
    ),
    base.APIRule(
        name="update_policy_dscp_marking_rule",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update a QoS DSCP marking rule",
        scope_types=["system"],
        operations=[
            {"method": "PUT", "path": "/qos/policies/{policy_id}/dscp_marking_rules/{rule_id}"},
        ],
    ),
    base.APIRule(
        name="delete_policy_dscp_marking_rule",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete a QoS DSCP marking rule",
        scope_types=["system"],
        operations=[
            {
                "method": "DELETE",
                "path": "/qos/policies/{policy_id}/dscp_marking_rules/{rule_id}",
            },
        ],
    ),
    base.APIRule(
        name="get_policy_minimum_bandwidth_rule",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a QoS minimum bandwidth rule",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/qos/policies/{policy_id}/minimum_bandwidth_rules"},
            {
                "method": "GET",
                "path": "/qos/policies/{policy_id}/minimum_bandwidth_rules/{rule_id}",
            },
        ],
    ),
    base.APIRule(
        name="create_policy_minimum_bandwidth_rule",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create a QoS minimum bandwidth rule",
        scope_types=["system"],
        operations=[
            {"method": "POST", "path": "/qos/policies/{policy_id}/minimum_bandwidth_rules"},
        ],
    ),
    base.APIRule(
        name="update_policy_minimum_bandwidth_rule",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update a QoS minimum bandwidth rule",
        scope_types=["system"],
        operations=[
            {
                "method": "PUT",
                "path": "/qos/policies/{policy_id}/minimum_bandwidth_rules/{rule_id}",
            },
        ],
    ),
    base.APIRule(
        name="delete_policy_minimum_bandwidth_rule",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete a QoS minimum bandwidth rule",
        scope_types=["system"],
        operations=[
            {
                "method": "DELETE",
                "path": "/qos/policies/{policy_id}/minimum_bandwidth_rules/{rule_id}",
            },
        ],
    ),
    base.APIRule(
        name="get_alias_bandwidth_limit_rule",
        check_str=("rule:get_policy_bandwidth_limit_rule"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a QoS bandwidth limit rule through alias",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/qos/alias_bandwidth_limit_rules/{rule_id}/"}],
    ),
    base.APIRule(
        name="update_alias_bandwidth_limit_rule",
        check_str=("rule:update_policy_bandwidth_limit_rule"),
        basic_check_str=("role:admin"),
        description="Update a QoS bandwidth limit rule through alias",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/qos/alias_bandwidth_limit_rules/{rule_id}/"}],
    ),
    base.APIRule(
        name="delete_alias_bandwidth_limit_rule",
        check_str=("rule:delete_policy_bandwidth_limit_rule"),
        basic_check_str=("role:admin"),
        description="Delete a QoS bandwidth limit rule through alias",
        scope_types=["project"],
        operations=[{"method": "DELETE", "path": "/qos/alias_bandwidth_limit_rules/{rule_id}/"}],
    ),
    base.APIRule(
        name="get_alias_dscp_marking_rule",
        check_str=("rule:get_policy_dscp_marking_rule"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a QoS DSCP marking rule through alias",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/qos/alias_dscp_marking_rules/{rule_id}/"}],
    ),
    base.APIRule(
        name="update_alias_dscp_marking_rule",
        check_str=("rule:update_policy_dscp_marking_rule"),
        basic_check_str=("role:admin"),
        description="Update a QoS DSCP marking rule through alias",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/qos/alias_dscp_marking_rules/{rule_id}/"}],
    ),
    base.APIRule(
        name="delete_alias_dscp_marking_rule",
        check_str=("rule:delete_policy_dscp_marking_rule"),
        basic_check_str=("role:admin"),
        description="Delete a QoS DSCP marking rule through alias",
        scope_types=["project"],
        operations=[{"method": "DELETE", "path": "/qos/alias_dscp_marking_rules/{rule_id}/"}],
    ),
    base.APIRule(
        name="get_alias_minimum_bandwidth_rule",
        check_str=("rule:get_policy_minimum_bandwidth_rule"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a QoS minimum bandwidth rule through alias",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/qos/alias_minimum_bandwidth_rules/{rule_id}/"}],
    ),
    base.APIRule(
        name="update_alias_minimum_bandwidth_rule",
        check_str=("rule:update_policy_minimum_bandwidth_rule"),
        basic_check_str=("role:admin"),
        description="Update a QoS minimum bandwidth rule through alias",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/qos/alias_minimum_bandwidth_rules/{rule_id}/"}],
    ),
    base.APIRule(
        name="delete_alias_minimum_bandwidth_rule",
        check_str=("rule:delete_policy_minimum_bandwidth_rule"),
        basic_check_str=("role:admin"),
        description="Delete a QoS minimum bandwidth rule through alias",
        scope_types=["project"],
        operations=[
            {"method": "DELETE", "path": "/qos/alias_minimum_bandwidth_rules/{rule_id}/"},
        ],
    ),
    base.APIRule(
        name="get_quota",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get a resource quota",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/quota"},
            {"method": "GET", "path": "/quota/{id}"},
        ],
    ),
    base.APIRule(
        name="update_quota",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update a resource quota",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/quota/{id}"}],
    ),
    base.APIRule(
        name="delete_quota",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete a resource quota",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/quota/{id}"}],
    ),
    base.APIRule(
        name="create_rbac_policy",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=("role:admin"),
        description="Create an RBAC policy",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/rbac-policies"}],
    ),
    base.APIRule(
        name="create_rbac_policy:target_tenant",
        check_str=("role:admin and system_scope:all or rule:restrict_wildcard"),
        basic_check_str=("role:admin"),
        description="Specify ``target_tenant`` when creating an RBAC policy",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/rbac-policies"}],
    ),
    base.APIRule(
        name="update_rbac_policy",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=("role:admin"),
        description="Update an RBAC policy",
        scope_types=["project", "system"],
        operations=[{"method": "PUT", "path": "/rbac-policies/{id}"}],
    ),
    base.APIRule(
        name="update_rbac_policy:target_tenant",
        check_str=("role:admin and system_scope:all or rule:restrict_wildcard"),
        basic_check_str=("role:admin"),
        description="Update ``target_tenant`` attribute of an RBAC policy",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/rbac-policies/{id}"}],
    ),
    base.APIRule(
        name="get_rbac_policy",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get an RBAC policy",
        scope_types=["project", "system"],
        operations=[
            {"method": "GET", "path": "/rbac-policies"},
            {"method": "GET", "path": "/rbac-policies/{id}"},
        ],
    ),
    base.APIRule(
        name="delete_rbac_policy",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=("role:admin"),
        description="Delete an RBAC policy",
        scope_types=["project", "system"],
        operations=[{"method": "DELETE", "path": "/rbac-policies/{id}"}],
    ),
    base.APIRule(
        name="create_router",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a router",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/routers"}],
    ),
    base.APIRule(
        name="create_router:distributed",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Specify ``distributed`` attribute when creating a router",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/routers"}],
    ),
    base.APIRule(
        name="create_router:ha",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Specify ``ha`` attribute when creating a router",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/routers"}],
    ),
    base.APIRule(
        name="create_router:external_gateway_info",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Specify ``external_gateway_info`` information when creating a router",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/routers"}],
    ),
    base.APIRule(
        name="create_router:external_gateway_info:network_id",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Specify ``network_id`` in ``external_gateway_info`` information when creating a router",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/routers"}],
    ),
    base.APIRule(
        name="create_router:external_gateway_info:enable_snat",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Specify ``enable_snat`` in ``external_gateway_info`` information when creating a router",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/routers"}],
    ),
    base.APIRule(
        name="create_router:external_gateway_info:external_fixed_ips",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Specify ``external_fixed_ips`` in ``external_gateway_info`` information when creating a router",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/routers"}],
    ),
    base.APIRule(
        name="get_router",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a router",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/routers"},
            {"method": "GET", "path": "/routers/{id}"},
        ],
    ),
    base.APIRule(
        name="get_router:distributed",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get ``distributed`` attribute of a router",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/routers"},
            {"method": "GET", "path": "/routers/{id}"},
        ],
    ),
    base.APIRule(
        name="get_router:ha",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get ``ha`` attribute of a router",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/routers"},
            {"method": "GET", "path": "/routers/{id}"},
        ],
    ),
    base.APIRule(
        name="update_router",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a router",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/routers/{id}"}],
    ),
    base.APIRule(
        name="update_router:distributed",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update ``distributed`` attribute of a router",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/routers/{id}"}],
    ),
    base.APIRule(
        name="update_router:ha",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update ``ha`` attribute of a router",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/routers/{id}"}],
    ),
    base.APIRule(
        name="update_router:external_gateway_info",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update ``external_gateway_info`` information of a router",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/routers/{id}"}],
    ),
    base.APIRule(
        name="update_router:external_gateway_info:network_id",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update ``network_id`` attribute of ``external_gateway_info`` information of a router",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/routers/{id}"}],
    ),
    base.APIRule(
        name="update_router:external_gateway_info:enable_snat",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update ``enable_snat`` attribute of ``external_gateway_info`` information of a router",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/routers/{id}"}],
    ),
    base.APIRule(
        name="update_router:external_gateway_info:external_fixed_ips",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update ``external_fixed_ips`` attribute of ``external_gateway_info`` information of a router",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/routers/{id}"}],
    ),
    base.APIRule(
        name="delete_router",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete a router",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/routers/{id}"}],
    ),
    base.APIRule(
        name="add_router_interface",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Add an interface to a router",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/routers/{id}/add_router_interface"}],
    ),
    base.APIRule(
        name="remove_router_interface",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Remove an interface from a router",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/routers/{id}/remove_router_interface"}],
    ),
    base.APIRule(
        name="create_security_group",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a security group",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/security-groups"}],
    ),
    base.APIRule(
        name="get_security_group",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a security group",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/security-groups"},
            {"method": "GET", "path": "/security-groups/{id}"},
        ],
    ),
    base.APIRule(
        name="update_security_group",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a security group",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/security-groups/{id}"}],
    ),
    base.APIRule(
        name="delete_security_group",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete a security group",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/security-groups/{id}"}],
    ),
    base.APIRule(
        name="create_security_group_rule",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a security group rule",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/security-group-rules"}],
    ),
    base.APIRule(
        name="get_security_group_rule",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s) or rule:sg_owner"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a security group rule",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/security-group-rules"},
            {"method": "GET", "path": "/security-group-rules/{id}"},
        ],
    ),
    base.APIRule(
        name="delete_security_group_rule",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete a security group rule",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/security-group-rules/{id}"}],
    ),
    base.APIRule(
        name="create_segment",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create a segment",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/segments"}],
    ),
    base.APIRule(
        name="get_segment",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get a segment",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/segments"},
            {"method": "GET", "path": "/segments/{id}"},
        ],
    ),
    base.APIRule(
        name="update_segment",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update a segment",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/segments/{id}"}],
    ),
    base.APIRule(
        name="delete_segment",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete a segment",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/segments/{id}"}],
    ),
    base.APIRule(
        name="get_service_provider",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get service providers",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/service-providers"}],
    ),
    base.APIRule(
        name="create_subnet",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s) or rule:network_owner"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a subnet",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/subnets"}],
    ),
    base.APIRule(
        name="create_subnet:segment_id",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Specify ``segment_id`` attribute when creating a subnet",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/subnets"}],
    ),
    base.APIRule(
        name="create_subnet:service_types",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Specify ``service_types`` attribute when creating a subnet",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/subnets"}],
    ),
    base.APIRule(
        name="get_subnet",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s) or rule:shared"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a subnet",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/subnets"},
            {"method": "GET", "path": "/subnets/{id}"},
        ],
    ),
    base.APIRule(
        name="get_subnet:segment_id",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get ``segment_id`` attribute of a subnet",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/subnets"},
            {"method": "GET", "path": "/subnets/{id}"},
        ],
    ),
    base.APIRule(
        name="update_subnet",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s) or rule:network_owner"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a subnet",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/subnets/{id}"}],
    ),
    base.APIRule(
        name="update_subnet:segment_id",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update ``segment_id`` attribute of a subnet",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/subnets/{id}"}],
    ),
    base.APIRule(
        name="update_subnet:service_types",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update ``service_types`` attribute of a subnet",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/subnets/{id}"}],
    ),
    base.APIRule(
        name="delete_subnet",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s) or rule:network_owner"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete a subnet",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/subnets/{id}"}],
    ),
    base.APIRule(
        name="create_subnetpool",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a subnetpool",
        scope_types=["project", "system"],
        operations=[{"method": "POST", "path": "/subnetpools"}],
    ),
    base.APIRule(
        name="create_subnetpool:shared",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create a shared subnetpool",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/subnetpools"}],
    ),
    base.APIRule(
        name="create_subnetpool:is_default",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Specify ``is_default`` attribute when creating a subnetpool",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/subnetpools"}],
    ),
    base.APIRule(
        name="get_subnetpool",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s) or rule:shared_subnetpools"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a subnetpool",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/subnetpools"},
            {"method": "GET", "path": "/subnetpools/{id}"},
        ],
    ),
    base.APIRule(
        name="update_subnetpool",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a subnetpool",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/subnetpools/{id}"}],
    ),
    base.APIRule(
        name="update_subnetpool:is_default",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update ``is_default`` attribute of a subnetpool",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/subnetpools/{id}"}],
    ),
    base.APIRule(
        name="delete_subnetpool",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete a subnetpool",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/subnetpools/{id}"}],
    ),
    base.APIRule(
        name="onboard_network_subnets",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Onboard existing subnet into a subnetpool",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/subnetpools/{id}/onboard_network_subnets"}],
    ),
    base.APIRule(
        name="add_prefixes",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Add prefixes to a subnetpool",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/subnetpools/{id}/add_prefixes"}],
    ),
    base.APIRule(
        name="remove_prefixes",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Remove unallocated prefixes from a subnetpool",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/subnetpools/{id}/remove_prefixes"}],
    ),
    base.APIRule(
        name="create_trunk",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a trunk",
        scope_types=["project", "system"],
        operations=[{"method": "POST", "path": "/trunks"}],
    ),
    base.APIRule(
        name="get_trunk",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get a trunk",
        scope_types=["project", "system"],
        operations=[
            {"method": "GET", "path": "/trunks"},
            {"method": "GET", "path": "/trunks/{id}"},
        ],
    ),
    base.APIRule(
        name="update_trunk",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a trunk",
        scope_types=["project", "system"],
        operations=[{"method": "PUT", "path": "/trunks/{id}"}],
    ),
    base.APIRule(
        name="delete_trunk",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete a trunk",
        scope_types=["project", "system"],
        operations=[{"method": "DELETE", "path": "/trunks/{id}"}],
    ),
    base.APIRule(
        name="get_subports",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List subports attached to a trunk",
        scope_types=["project", "system"],
        operations=[{"method": "GET", "path": "/trunks/{id}/get_subports"}],
    ),
    base.APIRule(
        name="add_subports",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Add subports to a trunk",
        scope_types=["project", "system"],
        operations=[{"method": "PUT", "path": "/trunks/{id}/add_subports"}],
    ),
    base.APIRule(
        name="remove_subports",
        check_str=(
            "(role:admin and system_scope:all) or (role:member and project_id:%(project_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete subports from a trunk",
        scope_types=["project", "system"],
        operations=[{"method": "PUT", "path": "/trunks/{id}/remove_subports"}],
    ),
    base.APIRule(
        name="create_endpoint_group",
        check_str=("rule:regular_user"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a VPN endpoint group",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/vpn/endpoint-groups"}],
    ),
    base.APIRule(
        name="update_endpoint_group",
        check_str=("rule:admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a VPN endpoint group",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/vpn/endpoint-groups/{id}"}],
    ),
    base.APIRule(
        name="delete_endpoint_group",
        check_str=("rule:admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete a VPN endpoint group",
        scope_types=["project"],
        operations=[{"method": "DELETE", "path": "/vpn/endpoint-groups/{id}"}],
    ),
    base.APIRule(
        name="get_endpoint_group",
        check_str=("rule:admin_or_owner"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get VPN endpoint groups",
        scope_types=["project"],
        operations=[
            {"method": "GET", "path": "/vpn/endpoint-groups"},
            {"method": "GET", "path": "/vpn/endpoint-groups/{id}"},
        ],
    ),
    base.APIRule(
        name="create_ikepolicy",
        check_str=("rule:regular_user"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create an IKE policy",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/vpn/ikepolicies"}],
    ),
    base.APIRule(
        name="update_ikepolicy",
        check_str=("rule:admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update an IKE policy",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/vpn/ikepolicies/{id}"}],
    ),
    base.APIRule(
        name="delete_ikepolicy",
        check_str=("rule:admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete an IKE policy",
        scope_types=["project"],
        operations=[{"method": "DELETE", "path": "/vpn/ikepolicies/{id}"}],
    ),
    base.APIRule(
        name="get_ikepolicy",
        check_str=("rule:admin_or_owner"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get IKE policyies",
        scope_types=["project"],
        operations=[
            {"method": "GET", "path": "/vpn/ikepolicies"},
            {"method": "GET", "path": "/vpn/ikepolicies/{id}"},
        ],
    ),
    base.APIRule(
        name="create_ipsecpolicy",
        check_str=("rule:regular_user"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create an IPsec policy",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/vpn/ipsecpolicies"}],
    ),
    base.APIRule(
        name="update_ipsecpolicy",
        check_str=("rule:admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update an IPsec policy",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/vpn/ipsecpolicies/{id}"}],
    ),
    base.APIRule(
        name="delete_ipsecpolicy",
        check_str=("rule:admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete an IPsec policy",
        scope_types=["project"],
        operations=[{"method": "DELETE", "path": "/vpn/ipsecpolicies/{id}"}],
    ),
    base.APIRule(
        name="get_ipsecpolicy",
        check_str=("rule:admin_or_owner"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get IPsec policies",
        scope_types=["project"],
        operations=[
            {"method": "GET", "path": "/vpn/ipsecpolicies"},
            {"method": "GET", "path": "/vpn/ipsecpolicies/{id}"},
        ],
    ),
    base.APIRule(
        name="create_ipsec_site_connection",
        check_str=("rule:regular_user"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create an IPsec site connection",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/vpn/ipsec-site-connections"}],
    ),
    base.APIRule(
        name="update_ipsec_site_connection",
        check_str=("rule:admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update an IPsec site connection",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/vpn/ipsec-site-connections/{id}"}],
    ),
    base.APIRule(
        name="delete_ipsec_site_connection",
        check_str=("rule:admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete an IPsec site connection",
        scope_types=["project"],
        operations=[{"method": "DELETE", "path": "/vpn/ipsec-site-connections/{id}"}],
    ),
    base.APIRule(
        name="get_ipsec_site_connection",
        check_str=("rule:admin_or_owner"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get IPsec site connections",
        scope_types=["project"],
        operations=[
            {"method": "GET", "path": "/vpn/ipsec-site-connections"},
            {"method": "GET", "path": "/vpn/ipsec-site-connections/{id}"},
        ],
    ),
    base.APIRule(
        name="create_vpnservice",
        check_str=("rule:regular_user"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a VPN service",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/vpn/vpnservices"}],
    ),
    base.APIRule(
        name="update_vpnservice",
        check_str=("rule:admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a VPN service",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/vpn/vpnservices/{id}"}],
    ),
    base.APIRule(
        name="delete_vpnservice",
        check_str=("rule:admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete a VPN service",
        scope_types=["project"],
        operations=[{"method": "DELETE", "path": "/vpn/vpnservices/{id}"}],
    ),
    base.APIRule(
        name="get_vpnservice",
        check_str=("rule:admin_or_owner"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Get VPN services",
        scope_types=["project"],
        operations=[
            {"method": "GET", "path": "/vpn/vpnservices"},
            {"method": "GET", "path": "/vpn/vpnservices/{id}"},
        ],
    ),
)

__all__ = ("list_rules",)
