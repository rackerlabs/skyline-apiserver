# flake8: noqa

from . import base

list_rules = (
    base.Rule(
        name="context_is_admin",
        check_str=("role:admin"),
        description="Decides what is required for the 'is_admin:True' check to succeed.",
    ),
    base.Rule(
        name="admin_or_owner",
        check_str=("is_admin:True or project_id:%(project_id)s"),
        description="Default rule for most non-Admin APIs.",
    ),
    base.Rule(
        name="admin_api",
        check_str=("is_admin:True"),
        description="Default rule for most Admin APIs.",
    ),
    base.Rule(
        name="system_admin_api",
        check_str=("role:admin and system_scope:all"),
        description="Default rule for System Admin APIs.",
    ),
    base.Rule(
        name="system_reader_api",
        check_str=("role:reader and system_scope:all"),
        description="Default rule for System level read only APIs.",
    ),
    base.Rule(
        name="project_admin_api",
        check_str=("role:admin and project_id:%(project_id)s"),
        description="Default rule for Project level admin APIs.",
    ),
    base.Rule(
        name="project_member_api",
        check_str=("role:member and project_id:%(project_id)s"),
        description="Default rule for Project level non admin APIs.",
    ),
    base.Rule(
        name="project_reader_api",
        check_str=("role:reader and project_id:%(project_id)s"),
        description="Default rule for Project level read only APIs.",
    ),
    base.Rule(
        name="system_admin_or_owner",
        check_str=("rule:system_admin_api or rule:project_member_api"),
        description="Default rule for System admin+owner APIs.",
    ),
    base.Rule(
        name="system_or_project_reader",
        check_str=("rule:system_reader_api or rule:project_reader_api"),
        description="Default rule for System+Project read only APIs.",
    ),
    base.APIRule(
        name="os_compute_api:os-admin-actions:reset_state",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Reset the state of a given server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (os-resetState)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-admin-actions:inject_network_info",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Inject network information into the server",
        scope_types=["system", "project"],
        operations=[
            {"method": "POST", "path": "/servers/{server_id}/action (injectNetworkInfo)"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-admin-password",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Change the administrative password for a server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (changePassword)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-aggregates:set_metadata",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Create or replace metadata for an aggregate",
        scope_types=["system"],
        operations=[
            {"method": "POST", "path": "/os-aggregates/{aggregate_id}/action (set_metadata)"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-aggregates:add_host",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Add a host to an aggregate",
        scope_types=["system"],
        operations=[
            {"method": "POST", "path": "/os-aggregates/{aggregate_id}/action (add_host)"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-aggregates:create",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Create an aggregate",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/os-aggregates"}],
    ),
    base.APIRule(
        name="os_compute_api:os-aggregates:remove_host",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Remove a host from an aggregate",
        scope_types=["system"],
        operations=[
            {"method": "POST", "path": "/os-aggregates/{aggregate_id}/action (remove_host)"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-aggregates:update",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Update name and/or availability zone for an aggregate",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/os-aggregates/{aggregate_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-aggregates:index",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="List all aggregates",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-aggregates"}],
    ),
    base.APIRule(
        name="os_compute_api:os-aggregates:delete",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Delete an aggregate",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/os-aggregates/{aggregate_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-aggregates:show",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="Show details for an aggregate",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-aggregates/{aggregate_id}"}],
    ),
    base.APIRule(
        name="compute:aggregates:images",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Request image caching for an aggregate",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/os-aggregates/{aggregate_id}/images"}],
    ),
    base.APIRule(
        name="os_compute_api:os-assisted-volume-snapshots:create",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Create an assisted volume snapshot",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/os-assisted-volume-snapshots"}],
    ),
    base.APIRule(
        name="os_compute_api:os-assisted-volume-snapshots:delete",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Delete an assisted volume snapshot",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/os-assisted-volume-snapshots/{snapshot_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-attach-interfaces:list",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List port interfaces attached to a server",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers/{server_id}/os-interface"}],
    ),
    base.APIRule(
        name="os_compute_api:os-attach-interfaces:show",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show details of a port interface attached to a server",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers/{server_id}/os-interface/{port_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-attach-interfaces:create",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Attach an interface to a server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/os-interface"}],
    ),
    base.APIRule(
        name="os_compute_api:os-attach-interfaces:delete",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Detach an interface from a server",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/servers/{server_id}/os-interface/{port_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-availability-zone:list",
        check_str=("@"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List availability zone information without host information",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-availability-zone"}],
    ),
    base.APIRule(
        name="os_compute_api:os-availability-zone:detail",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="List detailed availability zone information with host information",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-availability-zone/detail"}],
    ),
    base.APIRule(
        name="os_compute_api:os-baremetal-nodes:list",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="List and show details of bare metal nodes.\n#\n#These APIs are proxy calls to the Ironic service and are deprecated.\n#",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-baremetal-nodes"}],
    ),
    base.APIRule(
        name="os_compute_api:os-baremetal-nodes:show",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin"),
        description="Show action details for a server.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-baremetal-nodes/{node_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-console-auth-tokens",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="Show console connection information for a given console authentication token",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-console-auth-tokens/{console_token}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-console-output",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Show console output for a server",
        scope_types=["system", "project"],
        operations=[
            {"method": "POST", "path": "/servers/{server_id}/action (os-getConsoleOutput)"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-create-backup",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a back up of a server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (createBackup)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-deferred-delete:restore",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Restore a soft deleted server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (restore)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-deferred-delete:force",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Force delete a server before deferred cleanup",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (forceDelete)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-evacuate",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Evacuate a server from a failed host to a new host",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (evacuate)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-extended-server-attributes",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin or role:reader"),
        description="Return extended attributes for server.\n#\n#This rule will control the visibility for a set of servers attributes:\n#\n#- ``OS-EXT-SRV-ATTR:host``\n#- ``OS-EXT-SRV-ATTR:instance_name``\n#- ``OS-EXT-SRV-ATTR:reservation_id`` (since microversion 2.3)\n#- ``OS-EXT-SRV-ATTR:launch_index`` (since microversion 2.3)\n#- ``OS-EXT-SRV-ATTR:hostname`` (since microversion 2.3)\n#- ``OS-EXT-SRV-ATTR:kernel_id`` (since microversion 2.3)\n#- ``OS-EXT-SRV-ATTR:ramdisk_id`` (since microversion 2.3)\n#- ``OS-EXT-SRV-ATTR:root_device_name`` (since microversion 2.3)\n#- ``OS-EXT-SRV-ATTR:user_data`` (since microversion 2.3)\n#\n#Microvision 2.75 added the above attributes in the ``PUT /servers/{server_id}``\n#and ``POST /servers/{server_id}/action (rebuild)`` API responses which are\n#also controlled by this policy rule, like the ``GET /servers*`` APIs.\n#",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/servers/{id}"},
            {"method": "GET", "path": "/servers/detail"},
            {"method": "PUT", "path": "/servers/{server_id}"},
            {"method": "POST", "path": "/servers/{server_id}/action (rebuild)"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:extensions",
        check_str=("@"),
        basic_check_str=("@"),
        description="List available extensions and show information for an extension by alias",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/extensions"},
            {"method": "GET", "path": "/extensions/{alias}"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-flavor-access:add_tenant_access",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Add flavor access to a tenant",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/flavors/{flavor_id}/action (addTenantAccess)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-flavor-access:remove_tenant_access",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Remove flavor access from a tenant",
        scope_types=["system"],
        operations=[
            {"method": "POST", "path": "/flavors/{flavor_id}/action (removeTenantAccess)"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-flavor-access",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="List flavor access information\n#\n#Allows access to the full list of tenants that have access\n#to a flavor via an os-flavor-access API.\n#",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/flavors/{flavor_id}/os-flavor-access"}],
    ),
    base.APIRule(
        name="os_compute_api:os-flavor-extra-specs:show",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show an extra spec for a flavor",
        scope_types=["system", "project"],
        operations=[
            {
                "method": "GET",
                "path": "/flavors/{flavor_id}/os-extra_specs/{flavor_extra_spec_key}",
            },
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-flavor-extra-specs:create",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Create extra specs for a flavor",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/flavors/{flavor_id}/os-extra_specs/"}],
    ),
    base.APIRule(
        name="os_compute_api:os-flavor-extra-specs:update",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Update an extra spec for a flavor",
        scope_types=["system"],
        operations=[
            {
                "method": "PUT",
                "path": "/flavors/{flavor_id}/os-extra_specs/{flavor_extra_spec_key}",
            },
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-flavor-extra-specs:delete",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Delete an extra spec for a flavor",
        scope_types=["system"],
        operations=[
            {
                "method": "DELETE",
                "path": "/flavors/{flavor_id}/os-extra_specs/{flavor_extra_spec_key}",
            },
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-flavor-extra-specs:index",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List extra specs for a flavor. Starting with microversion 2.47, the flavor used for a server is also returned in the response when showing server details, updating a server or rebuilding a server. Starting with microversion 2.61, extra specs may be returned in responses for the flavor resource.",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/flavors/{flavor_id}/os-extra_specs/"},
            {"method": "GET", "path": "/servers/detail"},
            {"method": "GET", "path": "/servers/{server_id}"},
            {"method": "PUT", "path": "/servers/{server_id}"},
            {"method": "POST", "path": "/servers/{server_id}/action (rebuild)"},
            {"method": "POST", "path": "/flavors"},
            {"method": "GET", "path": "/flavors/detail"},
            {"method": "GET", "path": "/flavors/{flavor_id}"},
            {"method": "PUT", "path": "/flavors/{flavor_id}"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-flavor-manage:create",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Create a flavor",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/flavors"}],
    ),
    base.APIRule(
        name="os_compute_api:os-flavor-manage:update",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Update a flavor",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/flavors/{flavor_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-flavor-manage:delete",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Delete a flavor",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/flavors/{flavor_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-floating-ip-pools",
        check_str=("@"),
        basic_check_str=("@"),
        description="List floating IP pools. This API is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-floating-ip-pools"}],
    ),
    base.APIRule(
        name="os_compute_api:os-floating-ips:add",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Associate floating IPs to server.  This API is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (addFloatingIp)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-floating-ips:remove",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Disassociate floating IPs to server.  This API is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (removeFloatingIp)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-floating-ips:list",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List floating IPs. This API is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-floating-ips"}],
    ),
    base.APIRule(
        name="os_compute_api:os-floating-ips:create",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create floating IPs. This API is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/os-floating-ips"}],
    ),
    base.APIRule(
        name="os_compute_api:os-floating-ips:show",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show floating IPs. This API is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-floating-ips/{floating_ip_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-floating-ips:delete",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete floating IPs. This API is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/os-floating-ips/{floating_ip_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-hosts:list",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="List physical hosts.\n#\n#This API is deprecated in favor of os-hypervisors and os-services.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-hosts"}],
    ),
    base.APIRule(
        name="os_compute_api:os-hosts:show",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="Show physical host.\n#\n#This API is deprecated in favor of os-hypervisors and os-services.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-hosts/{host_name}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-hosts:update",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Update physical host.\n#\n#This API is deprecated in favor of os-hypervisors and os-services.",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/os-hosts/{host_name}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-hosts:reboot",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Reboot physical host.\n#\n#This API is deprecated in favor of os-hypervisors and os-services.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-hosts/{host_name}/reboot"}],
    ),
    base.APIRule(
        name="os_compute_api:os-hosts:shutdown",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Shutdown physical host.\n#\n#This API is deprecated in favor of os-hypervisors and os-services.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-hosts/{host_name}/shutdown"}],
    ),
    base.APIRule(
        name="os_compute_api:os-hosts:start",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Start physical host.\n#\n#This API is deprecated in favor of os-hypervisors and os-services.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-hosts/{host_name}/startup"}],
    ),
    base.APIRule(
        name="os_compute_api:os-hypervisors:list",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="List all hypervisors.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-hypervisors"}],
    ),
    base.APIRule(
        name="os_compute_api:os-hypervisors:list-detail",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="List all hypervisors with details",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-hypervisors/details"}],
    ),
    base.APIRule(
        name="os_compute_api:os-hypervisors:statistics",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="Show summary statistics for all hypervisors over all compute nodes.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-hypervisors/statistics"}],
    ),
    base.APIRule(
        name="os_compute_api:os-hypervisors:show",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="Show details for a hypervisor.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-hypervisors/{hypervisor_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-hypervisors:uptime",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="Show the uptime of a hypervisor.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-hypervisors/{hypervisor_id}/uptime"}],
    ),
    base.APIRule(
        name="os_compute_api:os-hypervisors:search",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="Search hypervisor by hypervisor_hostname pattern.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/os-hypervisors/{hypervisor_hostname_pattern}/search"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-hypervisors:servers",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="List all servers on hypervisors that can match the provided hypervisor_hostname pattern.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/os-hypervisors/{hypervisor_hostname_pattern}/servers"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-instance-actions:events:details",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="Add \"details\" key in action events for a server.\n#\n#This check is performed only after the check\n#os_compute_api:os-instance-actions:show passes. Beginning with Microversion\n#2.84, new field 'details' is exposed via API which can have more details about\n#event failure. That field is controlled by this policy which is system reader\n#by default. Making the 'details' field visible to the non-admin user helps to\n#understand the nature of the problem (i.e. if the action can be retried),\n#but in the other hand it might leak information about the deployment\n#(e.g. the type of the hypervisor).\n#",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/servers/{server_id}/os-instance-actions/{request_id}"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-instance-actions:events",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader or role:admin and project_id:%(project_id)s"),
        description="Add events details in action details for a server.\n#This check is performed only after the check\n#os_compute_api:os-instance-actions:show passes. Beginning with Microversion\n#2.51, events details are always included; traceback information is provided\n#per event if policy enforcement passes. Beginning with Microversion 2.62,\n#each event includes a hashed host identifier and, if policy enforcement\n#passes, the name of the host.",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/servers/{server_id}/os-instance-actions/{request_id}"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-instance-actions:list",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List actions for a server.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers/{server_id}/os-instance-actions"}],
    ),
    base.APIRule(
        name="os_compute_api:os-instance-actions:show",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show action details for a server.",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/servers/{server_id}/os-instance-actions/{request_id}"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-instance-usage-audit-log:list",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="List all usage audits.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-instance_usage_audit_log"}],
    ),
    base.APIRule(
        name="os_compute_api:os-instance-usage-audit-log:show",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="List all usage audits occurred before a specified time for all servers on all compute hosts where usage auditing is configured",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-instance_usage_audit_log/{before_timestamp}"}],
    ),
    base.APIRule(
        name="os_compute_api:ips:show",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show IP addresses details for a network label of a  server",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers/{server_id}/ips/{network_label}"}],
    ),
    base.APIRule(
        name="os_compute_api:ips:index",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List IP addresses that are assigned to a server",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers/{server_id}/ips"}],
    ),
    base.APIRule(
        name="os_compute_api:os-keypairs:index",
        check_str=("(rule:system_reader_api) or user_id:%(user_id)s"),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="List all keypairs",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-keypairs"}],
    ),
    base.APIRule(
        name="os_compute_api:os-keypairs:create",
        check_str=("(rule:system_admin_api) or user_id:%(user_id)s"),
        basic_check_str=("role:admin or user_id:%(user_id)s"),
        description="Create a keypair",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/os-keypairs"}],
    ),
    base.APIRule(
        name="os_compute_api:os-keypairs:delete",
        check_str=("(rule:system_admin_api) or user_id:%(user_id)s"),
        basic_check_str=("role:admin or user_id:%(user_id)s"),
        description="Delete a keypair",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/os-keypairs/{keypair_name}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-keypairs:show",
        check_str=("(rule:system_reader_api) or user_id:%(user_id)s"),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="Show details of a keypair",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-keypairs/{keypair_name}"}],
    ),
    base.APIRule(
        name="os_compute_api:limits",
        check_str=("@"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show rate and absolute limits for the current user project",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/limits"}],
    ),
    base.APIRule(
        name="os_compute_api:limits:other_project",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="Show rate and absolute limits of other project.\n#\n#This policy only checks if the user has access to the requested\n#project limits. And this check is performed only after the check\n#os_compute_api:limits passes",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/limits"}],
    ),
    base.APIRule(
        name="os_compute_api:os-lock-server:lock",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Lock a server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (lock)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-lock-server:unlock",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Unlock a server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (unlock)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-lock-server:unlock:unlock_override",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin or role:admin and project_id:%(project_id)s"),
        description="Unlock a server, regardless who locked the server.\n#\n#This check is performed only after the check\n#os_compute_api:os-lock-server:unlock passes",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (unlock)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-migrate-server:migrate",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin or role:admin and project_id:%(project_id)s"),
        description="Cold migrate a server to a host",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (migrate)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-migrate-server:migrate_live",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin or role:admin and project_id:%(project_id)s"),
        description="Live migrate a server to a new host without a reboot",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (os-migrateLive)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-migrations:index",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="List migrations",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-migrations"}],
    ),
    base.APIRule(
        name="os_compute_api:os-multinic:add",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Add a fixed IP address to a server.\n#\n#This API is proxy calls to the Network service. This is\n#deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (addFixedIp)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-multinic:remove",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Remove a fixed IP address from a server.\n#\n#This API is proxy calls to the Network service. This is\n#deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (removeFixedIp)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-networks:list",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List networks for the project.\n#\n#This API is proxy calls to the Network service. This is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-networks"}],
    ),
    base.APIRule(
        name="os_compute_api:os-networks:show",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show network details.\n#\n#This API is proxy calls to the Network service. This is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-networks/{network_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-pause-server:pause",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Pause a server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (pause)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-pause-server:unpause",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Unpause a paused server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (unpause)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-quota-class-sets:show",
        check_str=("rule:system_reader_api"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List quotas for specific quota classs",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-quota-class-sets/{quota_class}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-quota-class-sets:update",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Update quotas for specific quota class",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/os-quota-class-sets/{quota_class}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-quota-sets:update",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Update the quotas",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/os-quota-sets/{tenant_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-quota-sets:defaults",
        check_str=("@"),
        basic_check_str=("@"),
        description="List default quotas",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-quota-sets/{tenant_id}/defaults"}],
    ),
    base.APIRule(
        name="os_compute_api:os-quota-sets:show",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show a quota",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-quota-sets/{tenant_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-quota-sets:delete",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Revert quotas to defaults",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/os-quota-sets/{tenant_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-quota-sets:detail",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show the detail of quota",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-quota-sets/{tenant_id}/detail"}],
    ),
    base.APIRule(
        name="os_compute_api:os-remote-consoles",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Generate a URL to access remove server console.\n#\n#This policy is for ``POST /remote-consoles`` API and below Server actions APIs\n#are deprecated:\n#\n#- ``os-getRDPConsole``\n#- ``os-getSerialConsole``\n#- ``os-getSPICEConsole``\n#- ``os-getVNCConsole``.",
        scope_types=["system", "project"],
        operations=[
            {"method": "POST", "path": "/servers/{server_id}/action (os-getRDPConsole)"},
            {"method": "POST", "path": "/servers/{server_id}/action (os-getSerialConsole)"},
            {"method": "POST", "path": "/servers/{server_id}/action (os-getSPICEConsole)"},
            {"method": "POST", "path": "/servers/{server_id}/action (os-getVNCConsole)"},
            {"method": "POST", "path": "/servers/{server_id}/remote-consoles"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-rescue",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Rescue a server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (rescue)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-unrescue",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Unrescue a server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (unrescue)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-security-groups:get",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List security groups. This API is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-security-groups"}],
    ),
    base.APIRule(
        name="os_compute_api:os-security-groups:show",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show security group. This API is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-security-groups/{security_group_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-security-groups:create",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create security group. This API is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/os-security-groups"}],
    ),
    base.APIRule(
        name="os_compute_api:os-security-groups:update",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update security group. This API is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/os-security-groups/{security_group_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-security-groups:delete",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete security group. This API is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/os-security-groups/{security_group_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-security-groups:rule:create",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create security group Rule. This API is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/os-security-group-rules"}],
    ),
    base.APIRule(
        name="os_compute_api:os-security-groups:rule:delete",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete security group Rule. This API is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/os-security-group-rules/{security_group_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-security-groups:list",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List security groups of server.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers/{server_id}/os-security-groups"}],
    ),
    base.APIRule(
        name="os_compute_api:os-security-groups:add",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Add security groups to server.",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (addSecurityGroup)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-security-groups:remove",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Remove security groups from server.",
        scope_types=["system", "project"],
        operations=[
            {"method": "POST", "path": "/servers/{server_id}/action (removeSecurityGroup)"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-server-diagnostics",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin or role:reader or role:admin and project_id:%(project_id)s"),
        description="Show the usage data for a server",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers/{server_id}/diagnostics"}],
    ),
    base.APIRule(
        name="os_compute_api:os-server-external-events:create",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Create one or more external events",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/os-server-external-events"}],
    ),
    base.APIRule(
        name="os_compute_api:os-server-groups:create",
        check_str=("rule:project_member_api"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a new server group",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/os-server-groups"}],
    ),
    base.APIRule(
        name="os_compute_api:os-server-groups:delete",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete a server group",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/os-server-groups/{server_group_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-server-groups:index",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List all server groups",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-server-groups"}],
    ),
    base.APIRule(
        name="os_compute_api:os-server-groups:index:all_projects",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="List all server groups for all projects",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-server-groups"}],
    ),
    base.APIRule(
        name="os_compute_api:os-server-groups:show",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show details of a server group",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-server-groups/{server_group_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:server-metadata:index",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List all metadata of a server",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers/{server_id}/metadata"}],
    ),
    base.APIRule(
        name="os_compute_api:server-metadata:show",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show metadata for a server",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers/{server_id}/metadata/{key}"}],
    ),
    base.APIRule(
        name="os_compute_api:server-metadata:create",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create metadata for a server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/metadata"}],
    ),
    base.APIRule(
        name="os_compute_api:server-metadata:update_all",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Replace metadata for a server",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/servers/{server_id}/metadata"}],
    ),
    base.APIRule(
        name="os_compute_api:server-metadata:update",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update metadata from a server",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/servers/{server_id}/metadata/{key}"}],
    ),
    base.APIRule(
        name="os_compute_api:server-metadata:delete",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete metadata from a server",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/servers/{server_id}/metadata/{key}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-server-password:show",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show the encrypted administrative password of a server",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers/{server_id}/os-server-password"}],
    ),
    base.APIRule(
        name="os_compute_api:os-server-password:clear",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Clear the encrypted administrative password of a server",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/servers/{server_id}/os-server-password"}],
    ),
    base.APIRule(
        name="os_compute_api:os-server-tags:delete_all",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete all the server tags",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/servers/{server_id}/tags"}],
    ),
    base.APIRule(
        name="os_compute_api:os-server-tags:index",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List all tags for given server",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers/{server_id}/tags"}],
    ),
    base.APIRule(
        name="os_compute_api:os-server-tags:update_all",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Replace all tags on specified server with the new set of tags.",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/servers/{server_id}/tags"}],
    ),
    base.APIRule(
        name="os_compute_api:os-server-tags:delete",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete a single tag from the specified server",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/servers/{server_id}/tags/{tag}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-server-tags:update",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Add a single tag to the server if server has no specified tag",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/servers/{server_id}/tags/{tag}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-server-tags:show",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Check tag existence on the server.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers/{server_id}/tags/{tag}"}],
    ),
    base.APIRule(
        name="compute:server:topology:index",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=("role:admin or role:reader"),
        description="Show the NUMA topology data for a server",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers/{server_id}/topology"}],
    ),
    base.APIRule(
        name="compute:server:topology:host:index",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="Show the NUMA topology data for a server with host NUMA ID and CPU pinning information",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/servers/{server_id}/topology"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:index",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List all servers",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:detail",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List all servers with detailed information",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers/detail"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:index:get_all_tenants",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="List all servers for all projects",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/servers"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:detail:get_all_tenants",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="List all servers with detailed information for  all projects",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/servers/detail"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:allow_all_filters",
        check_str=("rule:system_reader_api"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Allow all filters when listing servers",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/servers"},
            {"method": "GET", "path": "/servers/detail"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:servers:show",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show a server",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers/{server_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:show:host_status",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin or role:reader or role:admin and project_id:%(project_id)s"),
        description="\n#Show a server with additional host status information.\n#\n#This means host_status will be shown irrespective of status value. If showing\n#only host_status UNKNOWN is desired, use the\n#``os_compute_api:servers:show:host_status:unknown-only`` policy rule.\n#\n#Microvision 2.75 added the ``host_status`` attribute in the\n#``PUT /servers/{server_id}`` and ``POST /servers/{server_id}/action (rebuild)``\n#API responses which are also controlled by this policy rule, like the\n#``GET /servers*`` APIs.\n#",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/servers/{server_id}"},
            {"method": "GET", "path": "/servers/detail"},
            {"method": "PUT", "path": "/servers/{server_id}"},
            {"method": "POST", "path": "/servers/{server_id}/action (rebuild)"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:servers:show:host_status:unknown-only",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="\n#Show a server with additional host status information, only if host status is\n#UNKNOWN.\n#\n#This policy rule will only be enforced when the\n#``os_compute_api:servers:show:host_status`` policy rule does not pass for the\n#request. An example policy configuration could be where the\n#``os_compute_api:servers:show:host_status`` rule is set to allow admin-only and\n#the ``os_compute_api:servers:show:host_status:unknown-only`` rule is set to\n#allow everyone.\n#",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/servers/{server_id}"},
            {"method": "GET", "path": "/servers/detail"},
            {"method": "PUT", "path": "/servers/{server_id}"},
            {"method": "POST", "path": "/servers/{server_id}/action (rebuild)"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:servers:create",
        check_str=("rule:project_member_api"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a server",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/servers"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:create:forced_host",
        check_str=("rule:project_admin_api"),
        basic_check_str=("role:admin or role:admin and project_id:%(project_id)s"),
        description="\n#Create a server on the specified host and/or node.\n#\n#In this case, the server is forced to launch on the specified\n#host and/or node by bypassing the scheduler filters unlike the\n#``compute:servers:create:requested_destination`` rule.\n#",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers"}],
    ),
    base.APIRule(
        name="compute:servers:create:requested_destination",
        check_str=("rule:project_admin_api"),
        basic_check_str=("role:admin or role:admin and project_id:%(project_id)s"),
        description="\n#Create a server on the requested compute service host and/or\n#hypervisor_hostname.\n#\n#In this case, the requested host and/or hypervisor_hostname is\n#validated by the scheduler filters unlike the\n#``os_compute_api:servers:create:forced_host`` rule.\n#",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:create:attach_volume",
        check_str=("rule:project_member_api"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a server with the requested volume attached to it",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/servers"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:create:attach_network",
        check_str=("rule:project_member_api"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a server with the requested network attached  to it",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/servers"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:create:trusted_certs",
        check_str=("rule:project_member_api"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create a server with trusted image certificate IDs",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/servers"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:create:zero_disk_flavor",
        check_str=("rule:project_admin_api"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="\n#This rule controls the compute API validation behavior of creating a server\n#with a flavor that has 0 disk, indicating the server should be volume-backed.\n#\n#For a flavor with disk=0, the root disk will be set to exactly the size of the\n#image used to deploy the instance. However, in this case the filter_scheduler\n#cannot select the compute host based on the virtual image size. Therefore, 0\n#should only be used for volume booted instances or for testing purposes.\n#\n#WARNING: It is a potential security exposure to enable this policy rule\n#if users can upload their own images since repeated attempts to\n#create a disk=0 flavor instance with a large image can exhaust\n#the local disk of the compute (or shared storage cluster). See bug\n#https://bugs.launchpad.net/nova/+bug/1739646 for details.\n#",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers"}],
    ),
    base.APIRule(
        name="network:attach_external_network",
        check_str=("rule:project_admin_api"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Attach an unshared external network to a server",
        scope_types=["system", "project"],
        operations=[
            {"method": "POST", "path": "/servers"},
            {"method": "POST", "path": "/servers/{server_id}/os-interface"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:servers:delete",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete a server",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/servers/{server_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:update",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a server",
        scope_types=["system", "project"],
        operations=[{"method": "PUT", "path": "/servers/{server_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:confirm_resize",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Confirm a server resize",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (confirmResize)"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:revert_resize",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Revert a server resize",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (revertResize)"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:reboot",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Reboot a server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (reboot)"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:resize",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Resize a server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (resize)"}],
    ),
    base.APIRule(
        name="compute:servers:resize:cross_cell",
        check_str=("!"),
        basic_check_str=("!"),
        description="Resize a server across cells. By default, this is disabled for all users and recommended to be tested in a deployment for admin users before opening it up to non-admin users. Resizing within a cell is the default preferred behavior even if this is enabled. ",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (resize)"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:rebuild",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Rebuild a server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (rebuild)"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:rebuild:trusted_certs",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Rebuild a server with trusted image certificate IDs",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (rebuild)"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:create_image",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create an image from a server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (createImage)"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:create_image:allow_volume_backed",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create an image from a volume backed server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (createImage)"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:start",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Start a server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (os-start)"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:stop",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Stop a server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (os-stop)"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:trigger_crash_dump",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Trigger crash dump in a server",
        scope_types=["system", "project"],
        operations=[
            {"method": "POST", "path": "/servers/{server_id}/action (trigger_crash_dump)"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:servers:migrations:show",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="Show details for an in-progress live migration for a given server",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers/{server_id}/migrations/{migration_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:servers:migrations:force_complete",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Force an in-progress live migration for a given server to complete",
        scope_types=["system", "project"],
        operations=[
            {
                "method": "POST",
                "path": "/servers/{server_id}/migrations/{migration_id}/action (force_complete)",
            },
        ],
    ),
    base.APIRule(
        name="os_compute_api:servers:migrations:delete",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Delete(Abort) an in-progress live migration",
        scope_types=["system", "project"],
        operations=[
            {"method": "DELETE", "path": "/servers/{server_id}/migrations/{migration_id}"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:servers:migrations:index",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="Lists in-progress live migrations for a given server",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers/{server_id}/migrations"}],
    ),
    base.APIRule(
        name="os_compute_api:os-services:list",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="List all running Compute services in a region.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-services"}],
    ),
    base.APIRule(
        name="os_compute_api:os-services:update",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Update a Compute service.",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/os-services/{service_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-services:delete",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Delete a Compute service.",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/os-services/{service_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-shelve:shelve",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Shelve server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (shelve)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-shelve:unshelve",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Unshelve (restore) shelved server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (unshelve)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-shelve:shelve_offload",
        check_str=("rule:system_admin_api"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Shelf-offload (remove) server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (shelveOffload)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-simple-tenant-usage:show",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show usage statistics for a specific tenant",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-simple-tenant-usage/{tenant_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-simple-tenant-usage:list",
        check_str=("rule:system_reader_api"),
        basic_check_str=("role:admin or role:reader"),
        description="List per tenant usage statistics for all tenants",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/os-simple-tenant-usage"}],
    ),
    base.APIRule(
        name="os_compute_api:os-suspend-server:resume",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Resume suspended server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (resume)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-suspend-server:suspend",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Suspend server",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/action (suspend)"}],
    ),
    base.APIRule(
        name="os_compute_api:os-tenant-networks:list",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List project networks.\n#\n#This API is proxy calls to the Network service. This is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-tenant-networks"}],
    ),
    base.APIRule(
        name="os_compute_api:os-tenant-networks:show",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show project network details.\n#\n#This API is proxy calls to the Network service. This is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-tenant-networks/{network_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-volumes:list",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List volumes.\n#\n#This API is a proxy call to the Volume service. It is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-volumes"}],
    ),
    base.APIRule(
        name="os_compute_api:os-volumes:create",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create volume.\n#\n#This API is a proxy call to the Volume service. It is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/os-volumes"}],
    ),
    base.APIRule(
        name="os_compute_api:os-volumes:detail",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List volumes detail.\n#\n#This API is a proxy call to the Volume service. It is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-volumes/detail"}],
    ),
    base.APIRule(
        name="os_compute_api:os-volumes:show",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show volume.\n#\n#This API is a proxy call to the Volume service. It is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-volumes/{volume_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-volumes:delete",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete volume.\n#\n#This API is a proxy call to the Volume service. It is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/os-volumes/{volume_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-volumes:snapshots:list",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List snapshots.\n#\n#This API is a proxy call to the Volume service. It is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-snapshots"}],
    ),
    base.APIRule(
        name="os_compute_api:os-volumes:snapshots:create",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Create snapshots.\n#\n#This API is a proxy call to the Volume service. It is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/os-snapshots"}],
    ),
    base.APIRule(
        name="os_compute_api:os-volumes:snapshots:detail",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List snapshots details.\n#\n#This API is a proxy call to the Volume service. It is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-snapshots/detail"}],
    ),
    base.APIRule(
        name="os_compute_api:os-volumes:snapshots:show",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show snapshot.\n#\n#This API is a proxy call to the Volume service. It is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/os-snapshots/{snapshot_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-volumes:snapshots:delete",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Delete snapshot.\n#\n#This API is a proxy call to the Volume service. It is deprecated.",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/os-snapshots/{snapshot_id}"}],
    ),
    base.APIRule(
        name="os_compute_api:os-volumes-attachments:index",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="List volume attachments for an instance",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/servers/{server_id}/os-volume_attachments"}],
    ),
    base.APIRule(
        name="os_compute_api:os-volumes-attachments:create",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Attach a volume to an instance",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/servers/{server_id}/os-volume_attachments"}],
    ),
    base.APIRule(
        name="os_compute_api:os-volumes-attachments:show",
        check_str=("rule:system_or_project_reader"),
        basic_check_str=(
            "role:admin or role:reader or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s or role:reader and project_id:%(project_id)s"
        ),
        description="Show details of a volume attachment",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/servers/{server_id}/os-volume_attachments/{volume_id}"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-volumes-attachments:update",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Update a volume attachment.\n#New 'update' policy about 'swap + update' request (which is possible\n#only >2.85) only <swap policy> is checked. We expect <swap policy> to be\n#always superset of this policy permission.\n#",
        scope_types=["system", "project"],
        operations=[
            {"method": "PUT", "path": "/servers/{server_id}/os-volume_attachments/{volume_id}"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-volumes-attachments:swap",
        check_str=("rule:system_admin_api"),
        basic_check_str=("role:admin"),
        description="Update a volume attachment with a different volumeId",
        scope_types=["system"],
        operations=[
            {"method": "PUT", "path": "/servers/{server_id}/os-volume_attachments/{volume_id}"},
        ],
    ),
    base.APIRule(
        name="os_compute_api:os-volumes-attachments:delete",
        check_str=("rule:system_admin_or_owner"),
        basic_check_str=(
            "role:admin or role:admin and project_id:%(project_id)s or role:member and project_id:%(project_id)s"
        ),
        description="Detach a volume from an instance",
        scope_types=["system", "project"],
        operations=[
            {
                "method": "DELETE",
                "path": "/servers/{server_id}/os-volume_attachments/{volume_id}",
            },
        ],
    ),
)

__all__ = ("list_rules",)
