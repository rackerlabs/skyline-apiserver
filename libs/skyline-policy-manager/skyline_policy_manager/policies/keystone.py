# flake8: noqa

from . import base

list_rules = (
    base.Rule(
        name="admin_required",
        check_str=("role:admin or is_admin:1"),
        description="No description",
    ),
    base.Rule(
        name="service_role",
        check_str=("role:service"),
        description="No description",
    ),
    base.Rule(
        name="service_or_admin",
        check_str=("rule:admin_required or rule:service_role"),
        description="No description",
    ),
    base.Rule(
        name="owner",
        check_str=("user_id:%(user_id)s"),
        description="No description",
    ),
    base.Rule(
        name="admin_or_owner",
        check_str=("rule:admin_required or rule:owner"),
        description="No description",
    ),
    base.Rule(
        name="token_subject",
        check_str=("user_id:%(target.token.user_id)s"),
        description="No description",
    ),
    base.Rule(
        name="admin_or_token_subject",
        check_str=("rule:admin_required or rule:token_subject"),
        description="No description",
    ),
    base.Rule(
        name="service_admin_or_token_subject",
        check_str=("rule:service_or_admin or rule:token_subject"),
        description="No description",
    ),
    base.APIRule(
        name="identity:get_access_rule",
        check_str=("(role:reader and system_scope:all) or user_id:%(target.user.id)s"),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="Show access rule details.",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/v3/users/{user_id}/access_rules/{access_rule_id}"},
            {"method": "HEAD", "path": "/v3/users/{user_id}/access_rules/{access_rule_id}"},
        ],
    ),
    base.APIRule(
        name="identity:list_access_rules",
        check_str=("(role:reader and system_scope:all) or user_id:%(target.user.id)s"),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="List access rules for a user.",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/v3/users/{user_id}/access_rules"},
            {"method": "HEAD", "path": "/v3/users/{user_id}/access_rules"},
        ],
    ),
    base.APIRule(
        name="identity:delete_access_rule",
        check_str=("(role:admin and system_scope:all) or user_id:%(target.user.id)s"),
        basic_check_str=("role:admin or user_id:%(user_id)s"),
        description="Delete an access_rule.",
        scope_types=["system", "project"],
        operations=[
            {"method": "DELETE", "path": "/v3/users/{user_id}/access_rules/{access_rule_id}"},
        ],
    ),
    base.APIRule(
        name="identity:authorize_request_token",
        check_str=("rule:admin_required"),
        basic_check_str=("!"),
        description="Authorize OAUTH1 request token.",
        scope_types=["project"],
        operations=[{"method": "PUT", "path": "/v3/OS-OAUTH1/authorize/{request_token_id}"}],
    ),
    base.APIRule(
        name="identity:get_access_token",
        check_str=("rule:admin_required"),
        basic_check_str=("!"),
        description="Get OAUTH1 access token for user by access token ID.",
        scope_types=["project"],
        operations=[
            {
                "method": "GET",
                "path": "/v3/users/{user_id}/OS-OAUTH1/access_tokens/{access_token_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:get_access_token_role",
        check_str=("rule:admin_required"),
        basic_check_str=("!"),
        description="Get role for user OAUTH1 access token.",
        scope_types=["project"],
        operations=[
            {
                "method": "GET",
                "path": "/v3/users/{user_id}/OS-OAUTH1/access_tokens/{access_token_id}/roles/{role_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:list_access_tokens",
        check_str=("rule:admin_required"),
        basic_check_str=("!"),
        description="List OAUTH1 access tokens for user.",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v3/users/{user_id}/OS-OAUTH1/access_tokens"}],
    ),
    base.APIRule(
        name="identity:list_access_token_roles",
        check_str=("rule:admin_required"),
        basic_check_str=("!"),
        description="List OAUTH1 access token roles.",
        scope_types=["project"],
        operations=[
            {
                "method": "GET",
                "path": "/v3/users/{user_id}/OS-OAUTH1/access_tokens/{access_token_id}/roles",
            },
        ],
    ),
    base.APIRule(
        name="identity:delete_access_token",
        check_str=("rule:admin_required"),
        basic_check_str=("!"),
        description="Delete OAUTH1 access token.",
        scope_types=["project"],
        operations=[
            {
                "method": "DELETE",
                "path": "/v3/users/{user_id}/OS-OAUTH1/access_tokens/{access_token_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:get_application_credential",
        check_str=("(role:reader and system_scope:all) or rule:owner"),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="Show application credential details.",
        scope_types=["system", "project"],
        operations=[
            {
                "method": "GET",
                "path": "/v3/users/{user_id}/application_credentials/{application_credential_id}",
            },
            {
                "method": "HEAD",
                "path": "/v3/users/{user_id}/application_credentials/{application_credential_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:list_application_credentials",
        check_str=("(role:reader and system_scope:all) or rule:owner"),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="List application credentials for a user.",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/v3/users/{user_id}/application_credentials"},
            {"method": "HEAD", "path": "/v3/users/{user_id}/application_credentials"},
        ],
    ),
    base.APIRule(
        name="identity:create_application_credential",
        check_str=("user_id:%(user_id)s"),
        basic_check_str=("role:admin or user_id:%(user_id)s"),
        description="Create an application credential.",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/v3/users/{user_id}/application_credentials"}],
    ),
    base.APIRule(
        name="identity:delete_application_credential",
        check_str=("(role:admin and system_scope:all) or rule:owner"),
        basic_check_str=("role:admin or user_id:%(user_id)s"),
        description="Delete an application credential.",
        scope_types=["system", "project"],
        operations=[
            {
                "method": "DELETE",
                "path": "/v3/users/{user_id}/application_credentials/{application_credential_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:get_auth_catalog",
        check_str=(""),
        basic_check_str=("@"),
        description="Get service catalog.",
        scope_types=["project"],
        operations=[
            {"method": "GET", "path": "/v3/auth/catalog"},
            {"method": "HEAD", "path": "/v3/auth/catalog"},
        ],
    ),
    base.APIRule(
        name="identity:get_auth_projects",
        check_str=(""),
        basic_check_str=("@"),
        description="List all projects a user has access to via role assignments.",
        scope_types=["project"],
        operations=[
            {"method": "GET", "path": "/v3/auth/projects"},
            {"method": "HEAD", "path": "/v3/auth/projects"},
        ],
    ),
    base.APIRule(
        name="identity:get_auth_domains",
        check_str=(""),
        basic_check_str=("@"),
        description="List all domains a user has access to via role assignments.",
        scope_types=["project"],
        operations=[
            {"method": "GET", "path": "/v3/auth/domains"},
            {"method": "HEAD", "path": "/v3/auth/domains"},
        ],
    ),
    base.APIRule(
        name="identity:get_auth_system",
        check_str=(""),
        basic_check_str=("@"),
        description="List systems a user has access to via role assignments.",
        scope_types=["project"],
        operations=[
            {"method": "GET", "path": "/v3/auth/system"},
            {"method": "HEAD", "path": "/v3/auth/system"},
        ],
    ),
    base.APIRule(
        name="identity:get_consumer",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("!"),
        description="Show OAUTH1 consumer details.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/v3/OS-OAUTH1/consumers/{consumer_id}"}],
    ),
    base.APIRule(
        name="identity:list_consumers",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("!"),
        description="List OAUTH1 consumers.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/v3/OS-OAUTH1/consumers"}],
    ),
    base.APIRule(
        name="identity:create_consumer",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("!"),
        description="Create OAUTH1 consumer.",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/v3/OS-OAUTH1/consumers"}],
    ),
    base.APIRule(
        name="identity:update_consumer",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("!"),
        description="Update OAUTH1 consumer.",
        scope_types=["system"],
        operations=[{"method": "PATCH", "path": "/v3/OS-OAUTH1/consumers/{consumer_id}"}],
    ),
    base.APIRule(
        name="identity:delete_consumer",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("!"),
        description="Delete OAUTH1 consumer.",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/v3/OS-OAUTH1/consumers/{consumer_id}"}],
    ),
    base.APIRule(
        name="identity:get_credential",
        check_str=("(role:reader and system_scope:all) or user_id:%(target.credential.user_id)s"),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="Show credentials details.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/v3/credentials/{credential_id}"}],
    ),
    base.APIRule(
        name="identity:list_credentials",
        check_str=("(role:reader and system_scope:all) or user_id:%(target.credential.user_id)s"),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="List credentials.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/v3/credentials"}],
    ),
    base.APIRule(
        name="identity:create_credential",
        check_str=("(role:admin and system_scope:all) or user_id:%(target.credential.user_id)s"),
        basic_check_str=("role:admin or user_id:%(user_id)s"),
        description="Create credential.",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/v3/credentials"}],
    ),
    base.APIRule(
        name="identity:update_credential",
        check_str=("(role:admin and system_scope:all) or user_id:%(target.credential.user_id)s"),
        basic_check_str=("role:admin or user_id:%(user_id)s"),
        description="Update credential.",
        scope_types=["system", "project"],
        operations=[{"method": "PATCH", "path": "/v3/credentials/{credential_id}"}],
    ),
    base.APIRule(
        name="identity:delete_credential",
        check_str=("(role:admin and system_scope:all) or user_id:%(target.credential.user_id)s"),
        basic_check_str=("role:admin or user_id:%(user_id)s"),
        description="Delete credential.",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/v3/credentials/{credential_id}"}],
    ),
    base.APIRule(
        name="identity:get_domain",
        check_str=(
            "(role:reader and system_scope:all) or token.domain.id:%(target.domain.id)s or token.project.domain.id:%(target.domain.id)s"
        ),
        basic_check_str=(
            "role:admin or role:reader or user_id:%(user_id)s or project_id:%(project_id)s"
        ),
        description="Show domain details.",
        scope_types=["system", "domain", "project"],
        operations=[{"method": "GET", "path": "/v3/domains/{domain_id}"}],
    ),
    base.APIRule(
        name="identity:list_domains",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List domains.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/v3/domains"}],
    ),
    base.APIRule(
        name="identity:create_domain",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create domain.",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/v3/domains"}],
    ),
    base.APIRule(
        name="identity:update_domain",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update domain.",
        scope_types=["system"],
        operations=[{"method": "PATCH", "path": "/v3/domains/{domain_id}"}],
    ),
    base.APIRule(
        name="identity:delete_domain",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete domain.",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/v3/domains/{domain_id}"}],
    ),
    base.APIRule(
        name="identity:create_domain_config",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create domain configuration.",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/v3/domains/{domain_id}/config"}],
    ),
    base.APIRule(
        name="identity:get_domain_config",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get the entire domain configuration for a domain, an option group within a domain, or a specific configuration option within a group for a domain.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/domains/{domain_id}/config"},
            {"method": "HEAD", "path": "/v3/domains/{domain_id}/config"},
            {"method": "GET", "path": "/v3/domains/{domain_id}/config/{group}"},
            {"method": "HEAD", "path": "/v3/domains/{domain_id}/config/{group}"},
            {"method": "GET", "path": "/v3/domains/{domain_id}/config/{group}/{option}"},
            {"method": "HEAD", "path": "/v3/domains/{domain_id}/config/{group}/{option}"},
        ],
    ),
    base.APIRule(
        name="identity:get_security_compliance_domain_config",
        check_str=(""),
        basic_check_str=("@"),
        description="Get security compliance domain configuration for either a domain or a specific option in a domain.",
        scope_types=["system", "domain", "project"],
        operations=[
            {"method": "GET", "path": "/v3/domains/{domain_id}/config/security_compliance"},
            {"method": "HEAD", "path": "/v3/domains/{domain_id}/config/security_compliance"},
            {
                "method": "GET",
                "path": "v3/domains/{domain_id}/config/security_compliance/{option}",
            },
            {
                "method": "HEAD",
                "path": "v3/domains/{domain_id}/config/security_compliance/{option}",
            },
        ],
    ),
    base.APIRule(
        name="identity:update_domain_config",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update domain configuration for either a domain, specific group or a specific option in a group.",
        scope_types=["system"],
        operations=[
            {"method": "PATCH", "path": "/v3/domains/{domain_id}/config"},
            {"method": "PATCH", "path": "/v3/domains/{domain_id}/config/{group}"},
            {"method": "PATCH", "path": "/v3/domains/{domain_id}/config/{group}/{option}"},
        ],
    ),
    base.APIRule(
        name="identity:delete_domain_config",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete domain configuration for either a domain, specific group or a specific option in a group.",
        scope_types=["system"],
        operations=[
            {"method": "DELETE", "path": "/v3/domains/{domain_id}/config"},
            {"method": "DELETE", "path": "/v3/domains/{domain_id}/config/{group}"},
            {"method": "DELETE", "path": "/v3/domains/{domain_id}/config/{group}/{option}"},
        ],
    ),
    base.APIRule(
        name="identity:get_domain_config_default",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get domain configuration default for either a domain, specific group or a specific option in a group.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/domains/config/default"},
            {"method": "HEAD", "path": "/v3/domains/config/default"},
            {"method": "GET", "path": "/v3/domains/config/{group}/default"},
            {"method": "HEAD", "path": "/v3/domains/config/{group}/default"},
            {"method": "GET", "path": "/v3/domains/config/{group}/{option}/default"},
            {"method": "HEAD", "path": "/v3/domains/config/{group}/{option}/default"},
        ],
    ),
    base.APIRule(
        name="identity:ec2_get_credential",
        check_str=("(role:reader and system_scope:all) or user_id:%(target.credential.user_id)s"),
        basic_check_str=("role:admin or user_id:%(user_id)s"),
        description="Show ec2 credential details.",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/v3/users/{user_id}/credentials/OS-EC2/{credential_id}"},
        ],
    ),
    base.APIRule(
        name="identity:ec2_list_credentials",
        check_str=("(role:reader and system_scope:all) or rule:owner"),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="List ec2 credentials.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/v3/users/{user_id}/credentials/OS-EC2"}],
    ),
    base.APIRule(
        name="identity:ec2_create_credential",
        check_str=("(role:admin and system_scope:all) or rule:owner"),
        basic_check_str=("role:admin or user_id:%(user_id)s"),
        description="Create ec2 credential.",
        scope_types=["system", "project"],
        operations=[{"method": "POST", "path": "/v3/users/{user_id}/credentials/OS-EC2"}],
    ),
    base.APIRule(
        name="identity:ec2_delete_credential",
        check_str=("(role:admin and system_scope:all) or user_id:%(target.credential.user_id)s"),
        basic_check_str=("role:admin or user_id:%(user_id)s"),
        description="Delete ec2 credential.",
        scope_types=["system", "project"],
        operations=[
            {
                "method": "DELETE",
                "path": "/v3/users/{user_id}/credentials/OS-EC2/{credential_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:get_endpoint",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Show endpoint details.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/v3/endpoints/{endpoint_id}"}],
    ),
    base.APIRule(
        name="identity:list_endpoints",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List endpoints.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/v3/endpoints"}],
    ),
    base.APIRule(
        name="identity:create_endpoint",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create endpoint.",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/v3/endpoints"}],
    ),
    base.APIRule(
        name="identity:update_endpoint",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update endpoint.",
        scope_types=["system"],
        operations=[{"method": "PATCH", "path": "/v3/endpoints/{endpoint_id}"}],
    ),
    base.APIRule(
        name="identity:delete_endpoint",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete endpoint.",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/v3/endpoints/{endpoint_id}"}],
    ),
    base.APIRule(
        name="identity:create_endpoint_group",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create endpoint group.",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/v3/OS-EP-FILTER/endpoint_groups"}],
    ),
    base.APIRule(
        name="identity:list_endpoint_groups",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin"),
        description="List endpoint groups.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/v3/OS-EP-FILTER/endpoint_groups"}],
    ),
    base.APIRule(
        name="identity:get_endpoint_group",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Get endpoint group.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}"},
            {"method": "HEAD", "path": "/v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}"},
        ],
    ),
    base.APIRule(
        name="identity:update_endpoint_group",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update endpoint group.",
        scope_types=["system"],
        operations=[
            {"method": "PATCH", "path": "/v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}"},
        ],
    ),
    base.APIRule(
        name="identity:delete_endpoint_group",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete endpoint group.",
        scope_types=["system"],
        operations=[
            {"method": "DELETE", "path": "/v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}"},
        ],
    ),
    base.APIRule(
        name="identity:list_projects_associated_with_endpoint_group",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin"),
        description="List all projects associated with a specific endpoint group.",
        scope_types=["system"],
        operations=[
            {
                "method": "GET",
                "path": "/v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}/projects",
            },
        ],
    ),
    base.APIRule(
        name="identity:list_endpoints_associated_with_endpoint_group",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin"),
        description="List all endpoints associated with an endpoint group.",
        scope_types=["system"],
        operations=[
            {
                "method": "GET",
                "path": "/v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}/endpoints",
            },
        ],
    ),
    base.APIRule(
        name="identity:get_endpoint_group_in_project",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Check if an endpoint group is associated with a project.",
        scope_types=["system"],
        operations=[
            {
                "method": "GET",
                "path": "/v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}/projects/{project_id}",
            },
            {
                "method": "HEAD",
                "path": "/v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}/projects/{project_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:list_endpoint_groups_for_project",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin"),
        description="List endpoint groups associated with a specific project.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/OS-EP-FILTER/projects/{project_id}/endpoint_groups"},
        ],
    ),
    base.APIRule(
        name="identity:add_endpoint_group_to_project",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Allow a project to access an endpoint group.",
        scope_types=["system"],
        operations=[
            {
                "method": "PUT",
                "path": "/v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}/projects/{project_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:remove_endpoint_group_from_project",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Remove endpoint group from project.",
        scope_types=["system"],
        operations=[
            {
                "method": "DELETE",
                "path": "/v3/OS-EP-FILTER/endpoint_groups/{endpoint_group_id}/projects/{project_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:check_grant",
        check_str=(
            "(role:reader and system_scope:all) or ((role:reader and domain_id:%(target.user.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:reader and domain_id:%(target.user.domain_id)s and domain_id:%(target.domain.id)s) or (role:reader and domain_id:%(target.group.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:reader and domain_id:%(target.group.domain_id)s and domain_id:%(target.domain.id)s)) and (domain_id:%(target.role.domain_id)s or None:%(target.role.domain_id)s)"
        ),
        basic_check_str=("role:admin or role:reader or project_id:%(project_id)s"),
        description="Check a role grant between a target and an actor. A target can be either a domain or a project. An actor can be either a user or a group. These terms also apply to the OS-INHERIT APIs, where grants on the target are inherited to all projects in the subtree, if applicable.",
        scope_types=["system", "domain"],
        operations=[
            {
                "method": "HEAD",
                "path": "/v3/projects/{project_id}/users/{user_id}/roles/{role_id}",
            },
            {
                "method": "GET",
                "path": "/v3/projects/{project_id}/users/{user_id}/roles/{role_id}",
            },
            {
                "method": "HEAD",
                "path": "/v3/projects/{project_id}/groups/{group_id}/roles/{role_id}",
            },
            {
                "method": "GET",
                "path": "/v3/projects/{project_id}/groups/{group_id}/roles/{role_id}",
            },
            {"method": "HEAD", "path": "/v3/domains/{domain_id}/users/{user_id}/roles/{role_id}"},
            {"method": "GET", "path": "/v3/domains/{domain_id}/users/{user_id}/roles/{role_id}"},
            {
                "method": "HEAD",
                "path": "/v3/domains/{domain_id}/groups/{group_id}/roles/{role_id}",
            },
            {
                "method": "GET",
                "path": "/v3/domains/{domain_id}/groups/{group_id}/roles/{role_id}",
            },
            {
                "method": "HEAD",
                "path": "/v3/OS-INHERIT/projects/{project_id}/users/{user_id}/roles/{role_id}/inherited_to_projects",
            },
            {
                "method": "GET",
                "path": "/v3/OS-INHERIT/projects/{project_id}/users/{user_id}/roles/{role_id}/inherited_to_projects",
            },
            {
                "method": "HEAD",
                "path": "/v3/OS-INHERIT/projects/{project_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects",
            },
            {
                "method": "GET",
                "path": "/v3/OS-INHERIT/projects/{project_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects",
            },
            {
                "method": "HEAD",
                "path": "/v3/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/{role_id}/inherited_to_projects",
            },
            {
                "method": "GET",
                "path": "/v3/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/{role_id}/inherited_to_projects",
            },
            {
                "method": "HEAD",
                "path": "/v3/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects",
            },
            {
                "method": "GET",
                "path": "/v3/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects",
            },
        ],
    ),
    base.APIRule(
        name="identity:list_grants",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and domain_id:%(target.user.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:reader and domain_id:%(target.user.domain_id)s and domain_id:%(target.domain.id)s) or (role:reader and domain_id:%(target.group.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:reader and domain_id:%(target.group.domain_id)s and domain_id:%(target.domain.id)s)"
        ),
        basic_check_str=("role:admin or role:reader or project_id:%(project_id)s"),
        description="List roles granted to an actor on a target. A target can be either a domain or a project. An actor can be either a user or a group. For the OS-INHERIT APIs, it is possible to list inherited role grants for actors on domains, where grants are inherited to all projects in the specified domain.",
        scope_types=["system", "domain"],
        operations=[
            {"method": "GET", "path": "/v3/projects/{project_id}/users/{user_id}/roles"},
            {"method": "HEAD", "path": "/v3/projects/{project_id}/users/{user_id}/roles"},
            {"method": "GET", "path": "/v3/projects/{project_id}/groups/{group_id}/roles"},
            {"method": "HEAD", "path": "/v3/projects/{project_id}/groups/{group_id}/roles"},
            {"method": "GET", "path": "/v3/domains/{domain_id}/users/{user_id}/roles"},
            {"method": "HEAD", "path": "/v3/domains/{domain_id}/users/{user_id}/roles"},
            {"method": "GET", "path": "/v3/domains/{domain_id}/groups/{group_id}/roles"},
            {"method": "HEAD", "path": "/v3/domains/{domain_id}/groups/{group_id}/roles"},
            {
                "method": "GET",
                "path": "/v3/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/inherited_to_projects",
            },
            {
                "method": "GET",
                "path": "/v3/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/inherited_to_projects",
            },
        ],
    ),
    base.APIRule(
        name="identity:create_grant",
        check_str=(
            "(role:admin and system_scope:all) or ((role:admin and domain_id:%(target.user.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:admin and domain_id:%(target.user.domain_id)s and domain_id:%(target.domain.id)s) or (role:admin and domain_id:%(target.group.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:admin and domain_id:%(target.group.domain_id)s and domain_id:%(target.domain.id)s)) and (domain_id:%(target.role.domain_id)s or None:%(target.role.domain_id)s)"
        ),
        basic_check_str=("role:admin or role:admin and project_id:%(project_id)s"),
        description="Create a role grant between a target and an actor. A target can be either a domain or a project. An actor can be either a user or a group. These terms also apply to the OS-INHERIT APIs, where grants on the target are inherited to all projects in the subtree, if applicable.",
        scope_types=["system", "domain"],
        operations=[
            {
                "method": "PUT",
                "path": "/v3/projects/{project_id}/users/{user_id}/roles/{role_id}",
            },
            {
                "method": "PUT",
                "path": "/v3/projects/{project_id}/groups/{group_id}/roles/{role_id}",
            },
            {"method": "PUT", "path": "/v3/domains/{domain_id}/users/{user_id}/roles/{role_id}"},
            {
                "method": "PUT",
                "path": "/v3/domains/{domain_id}/groups/{group_id}/roles/{role_id}",
            },
            {
                "method": "PUT",
                "path": "/v3/OS-INHERIT/projects/{project_id}/users/{user_id}/roles/{role_id}/inherited_to_projects",
            },
            {
                "method": "PUT",
                "path": "/v3/OS-INHERIT/projects/{project_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects",
            },
            {
                "method": "PUT",
                "path": "/v3/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/{role_id}/inherited_to_projects",
            },
            {
                "method": "PUT",
                "path": "/v3/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects",
            },
        ],
    ),
    base.APIRule(
        name="identity:revoke_grant",
        check_str=(
            "(role:admin and system_scope:all) or ((role:admin and domain_id:%(target.user.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:admin and domain_id:%(target.user.domain_id)s and domain_id:%(target.domain.id)s) or (role:admin and domain_id:%(target.group.domain_id)s and domain_id:%(target.project.domain_id)s) or (role:admin and domain_id:%(target.group.domain_id)s and domain_id:%(target.domain.id)s)) and (domain_id:%(target.role.domain_id)s or None:%(target.role.domain_id)s)"
        ),
        basic_check_str=("role:admin or role:admin and project_id:%(project_id)s"),
        description="Revoke a role grant between a target and an actor. A target can be either a domain or a project. An actor can be either a user or a group. These terms also apply to the OS-INHERIT APIs, where grants on the target are inherited to all projects in the subtree, if applicable. In that case, revoking the role grant in the target would remove the logical effect of inheriting it to the target's projects subtree.",
        scope_types=["system", "domain"],
        operations=[
            {
                "method": "DELETE",
                "path": "/v3/projects/{project_id}/users/{user_id}/roles/{role_id}",
            },
            {
                "method": "DELETE",
                "path": "/v3/projects/{project_id}/groups/{group_id}/roles/{role_id}",
            },
            {
                "method": "DELETE",
                "path": "/v3/domains/{domain_id}/users/{user_id}/roles/{role_id}",
            },
            {
                "method": "DELETE",
                "path": "/v3/domains/{domain_id}/groups/{group_id}/roles/{role_id}",
            },
            {
                "method": "DELETE",
                "path": "/v3/OS-INHERIT/projects/{project_id}/users/{user_id}/roles/{role_id}/inherited_to_projects",
            },
            {
                "method": "DELETE",
                "path": "/v3/OS-INHERIT/projects/{project_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects",
            },
            {
                "method": "DELETE",
                "path": "/v3/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/{role_id}/inherited_to_projects",
            },
            {
                "method": "DELETE",
                "path": "/v3/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects",
            },
        ],
    ),
    base.APIRule(
        name="identity:list_system_grants_for_user",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List all grants a specific user has on the system.",
        scope_types=["system"],
        operations=[
            {"method": "HEAD", "path": "/v3/system/users/{user_id}/roles"},
            {"method": "GET", "path": "/v3/system/users/{user_id}/roles"},
        ],
    ),
    base.APIRule(
        name="identity:check_system_grant_for_user",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Check if a user has a role on the system.",
        scope_types=["system"],
        operations=[
            {"method": "HEAD", "path": "/v3/system/users/{user_id}/roles/{role_id}"},
            {"method": "GET", "path": "/v3/system/users/{user_id}/roles/{role_id}"},
        ],
    ),
    base.APIRule(
        name="identity:create_system_grant_for_user",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Grant a user a role on the system.",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/v3/system/users/{user_id}/roles/{role_id}"}],
    ),
    base.APIRule(
        name="identity:revoke_system_grant_for_user",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Remove a role from a user on the system.",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/v3/system/users/{user_id}/roles/{role_id}"}],
    ),
    base.APIRule(
        name="identity:list_system_grants_for_group",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List all grants a specific group has on the system.",
        scope_types=["system"],
        operations=[
            {"method": "HEAD", "path": "/v3/system/groups/{group_id}/roles"},
            {"method": "GET", "path": "/v3/system/groups/{group_id}/roles"},
        ],
    ),
    base.APIRule(
        name="identity:check_system_grant_for_group",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Check if a group has a role on the system.",
        scope_types=["system"],
        operations=[
            {"method": "HEAD", "path": "/v3/system/groups/{group_id}/roles/{role_id}"},
            {"method": "GET", "path": "/v3/system/groups/{group_id}/roles/{role_id}"},
        ],
    ),
    base.APIRule(
        name="identity:create_system_grant_for_group",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Grant a group a role on the system.",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/v3/system/groups/{group_id}/roles/{role_id}"}],
    ),
    base.APIRule(
        name="identity:revoke_system_grant_for_group",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Remove a role from a group on the system.",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/v3/system/groups/{group_id}/roles/{role_id}"}],
    ),
    base.APIRule(
        name="identity:get_group",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and domain_id:%(target.group.domain_id)s)"
        ),
        basic_check_str=("role:admin or role:reader"),
        description="Show group details.",
        scope_types=["system", "domain"],
        operations=[
            {"method": "GET", "path": "/v3/groups/{group_id}"},
            {"method": "HEAD", "path": "/v3/groups/{group_id}"},
        ],
    ),
    base.APIRule(
        name="identity:list_groups",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and domain_id:%(target.group.domain_id)s)"
        ),
        basic_check_str=("role:admin or role:reader"),
        description="List groups.",
        scope_types=["system", "domain"],
        operations=[
            {"method": "GET", "path": "/v3/groups"},
            {"method": "HEAD", "path": "/v3/groups"},
        ],
    ),
    base.APIRule(
        name="identity:list_groups_for_user",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and domain_id:%(target.user.domain_id)s) or user_id:%(user_id)s"
        ),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="List groups to which a user belongs.",
        scope_types=["system", "domain", "project"],
        operations=[
            {"method": "GET", "path": "/v3/users/{user_id}/groups"},
            {"method": "HEAD", "path": "/v3/users/{user_id}/groups"},
        ],
    ),
    base.APIRule(
        name="identity:create_group",
        check_str=(
            "(role:admin and system_scope:all) or (role:admin and domain_id:%(target.group.domain_id)s)"
        ),
        basic_check_str=("role:admin"),
        description="Create group.",
        scope_types=["system", "domain"],
        operations=[{"method": "POST", "path": "/v3/groups"}],
    ),
    base.APIRule(
        name="identity:update_group",
        check_str=(
            "(role:admin and system_scope:all) or (role:admin and domain_id:%(target.group.domain_id)s)"
        ),
        basic_check_str=("role:admin"),
        description="Update group.",
        scope_types=["system", "domain"],
        operations=[{"method": "PATCH", "path": "/v3/groups/{group_id}"}],
    ),
    base.APIRule(
        name="identity:delete_group",
        check_str=(
            "(role:admin and system_scope:all) or (role:admin and domain_id:%(target.group.domain_id)s)"
        ),
        basic_check_str=("role:admin"),
        description="Delete group.",
        scope_types=["system", "domain"],
        operations=[{"method": "DELETE", "path": "/v3/groups/{group_id}"}],
    ),
    base.APIRule(
        name="identity:list_users_in_group",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and domain_id:%(target.group.domain_id)s)"
        ),
        basic_check_str=("role:admin or role:reader"),
        description="List members of a specific group.",
        scope_types=["system", "domain"],
        operations=[
            {"method": "GET", "path": "/v3/groups/{group_id}/users"},
            {"method": "HEAD", "path": "/v3/groups/{group_id}/users"},
        ],
    ),
    base.APIRule(
        name="identity:remove_user_from_group",
        check_str=(
            "(role:admin and system_scope:all) or (role:admin and domain_id:%(target.group.domain_id)s and domain_id:%(target.user.domain_id)s)"
        ),
        basic_check_str=("role:admin"),
        description="Remove user from group.",
        scope_types=["system", "domain"],
        operations=[{"method": "DELETE", "path": "/v3/groups/{group_id}/users/{user_id}"}],
    ),
    base.APIRule(
        name="identity:check_user_in_group",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and domain_id:%(target.group.domain_id)s and domain_id:%(target.user.domain_id)s)"
        ),
        basic_check_str=("role:admin or role:reader"),
        description="Check whether a user is a member of a group.",
        scope_types=["system", "domain"],
        operations=[
            {"method": "HEAD", "path": "/v3/groups/{group_id}/users/{user_id}"},
            {"method": "GET", "path": "/v3/groups/{group_id}/users/{user_id}"},
        ],
    ),
    base.APIRule(
        name="identity:add_user_to_group",
        check_str=(
            "(role:admin and system_scope:all) or (role:admin and domain_id:%(target.group.domain_id)s and domain_id:%(target.user.domain_id)s)"
        ),
        basic_check_str=("role:admin"),
        description="Add user to group.",
        scope_types=["system", "domain"],
        operations=[{"method": "PUT", "path": "/v3/groups/{group_id}/users/{user_id}"}],
    ),
    base.APIRule(
        name="identity:create_identity_provider",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create identity provider.",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/v3/OS-FEDERATION/identity_providers/{idp_id}"}],
    ),
    base.APIRule(
        name="identity:list_identity_providers",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List identity providers.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/OS-FEDERATION/identity_providers"},
            {"method": "HEAD", "path": "/v3/OS-FEDERATION/identity_providers"},
        ],
    ),
    base.APIRule(
        name="identity:get_identity_provider",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get identity provider.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/OS-FEDERATION/identity_providers/{idp_id}"},
            {"method": "HEAD", "path": "/v3/OS-FEDERATION/identity_providers/{idp_id}"},
        ],
    ),
    base.APIRule(
        name="identity:update_identity_provider",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update identity provider.",
        scope_types=["system"],
        operations=[{"method": "PATCH", "path": "/v3/OS-FEDERATION/identity_providers/{idp_id}"}],
    ),
    base.APIRule(
        name="identity:delete_identity_provider",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete identity provider.",
        scope_types=["system"],
        operations=[
            {"method": "DELETE", "path": "/v3/OS-FEDERATION/identity_providers/{idp_id}"},
        ],
    ),
    base.APIRule(
        name="identity:get_implied_role",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get information about an association between two roles. When a relationship exists between a prior role and an implied role and the prior role is assigned to a user, the user also assumes the implied role.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/roles/{prior_role_id}/implies/{implied_role_id}"},
        ],
    ),
    base.APIRule(
        name="identity:list_implied_roles",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List associations between two roles. When a relationship exists between a prior role and an implied role and the prior role is assigned to a user, the user also assumes the implied role. This will return all the implied roles that would be assumed by the user who gets the specified prior role.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/roles/{prior_role_id}/implies"},
            {"method": "HEAD", "path": "/v3/roles/{prior_role_id}/implies"},
        ],
    ),
    base.APIRule(
        name="identity:create_implied_role",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create an association between two roles. When a relationship exists between a prior role and an implied role and the prior role is assigned to a user, the user also assumes the implied role.",
        scope_types=["system"],
        operations=[
            {"method": "PUT", "path": "/v3/roles/{prior_role_id}/implies/{implied_role_id}"},
        ],
    ),
    base.APIRule(
        name="identity:delete_implied_role",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete the association between two roles. When a relationship exists between a prior role and an implied role and the prior role is assigned to a user, the user also assumes the implied role. Removing the association will cause that effect to be eliminated.",
        scope_types=["system"],
        operations=[
            {"method": "DELETE", "path": "/v3/roles/{prior_role_id}/implies/{implied_role_id}"},
        ],
    ),
    base.APIRule(
        name="identity:list_role_inference_rules",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List all associations between two roles in the system. When a relationship exists between a prior role and an implied role and the prior role is assigned to a user, the user also assumes the implied role.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/role_inferences"},
            {"method": "HEAD", "path": "/v3/role_inferences"},
        ],
    ),
    base.APIRule(
        name="identity:check_implied_role",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Check an association between two roles. When a relationship exists between a prior role and an implied role and the prior role is assigned to a user, the user also assumes the implied role.",
        scope_types=["system"],
        operations=[
            {"method": "HEAD", "path": "/v3/roles/{prior_role_id}/implies/{implied_role_id}"},
        ],
    ),
    base.APIRule(
        name="identity:get_limit_model",
        check_str=(""),
        basic_check_str=("@"),
        description="Get limit enforcement model.",
        scope_types=["system", "domain", "project"],
        operations=[
            {"method": "GET", "path": "/v3/limits/model"},
            {"method": "HEAD", "path": "/v3/limits/model"},
        ],
    ),
    base.APIRule(
        name="identity:get_limit",
        check_str=(
            "(role:reader and system_scope:all) or (domain_id:%(target.limit.domain.id)s or domain_id:%(target.limit.project.domain_id)s) or (project_id:%(target.limit.project_id)s and not None:%(target.limit.project_id)s)"
        ),
        basic_check_str=("@"),
        description="Show limit details.",
        scope_types=["system", "domain", "project"],
        operations=[
            {"method": "GET", "path": "/v3/limits/{limit_id}"},
            {"method": "HEAD", "path": "/v3/limits/{limit_id}"},
        ],
    ),
    base.APIRule(
        name="identity:list_limits",
        check_str=(""),
        basic_check_str=("@"),
        description="List limits.",
        scope_types=["system", "domain", "project"],
        operations=[
            {"method": "GET", "path": "/v3/limits"},
            {"method": "HEAD", "path": "/v3/limits"},
        ],
    ),
    base.APIRule(
        name="identity:create_limits",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create limits.",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/v3/limits"}],
    ),
    base.APIRule(
        name="identity:update_limit",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update limit.",
        scope_types=["system"],
        operations=[{"method": "PATCH", "path": "/v3/limits/{limit_id}"}],
    ),
    base.APIRule(
        name="identity:delete_limit",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete limit.",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/v3/limits/{limit_id}"}],
    ),
    base.APIRule(
        name="identity:create_mapping",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create a new federated mapping containing one or more sets of rules.",
        scope_types=["system"],
        operations=[{"method": "PUT", "path": "/v3/OS-FEDERATION/mappings/{mapping_id}"}],
    ),
    base.APIRule(
        name="identity:get_mapping",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get a federated mapping.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/OS-FEDERATION/mappings/{mapping_id}"},
            {"method": "HEAD", "path": "/v3/OS-FEDERATION/mappings/{mapping_id}"},
        ],
    ),
    base.APIRule(
        name="identity:list_mappings",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List federated mappings.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/OS-FEDERATION/mappings"},
            {"method": "HEAD", "path": "/v3/OS-FEDERATION/mappings"},
        ],
    ),
    base.APIRule(
        name="identity:delete_mapping",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete a federated mapping.",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/v3/OS-FEDERATION/mappings/{mapping_id}"}],
    ),
    base.APIRule(
        name="identity:update_mapping",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update a federated mapping.",
        scope_types=["system"],
        operations=[{"method": "PATCH", "path": "/v3/OS-FEDERATION/mappings/{mapping_id}"}],
    ),
    base.APIRule(
        name="identity:get_policy",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("!"),
        description="Show policy details.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/v3/policies/{policy_id}"}],
    ),
    base.APIRule(
        name="identity:list_policies",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("!"),
        description="List policies.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/v3/policies"}],
    ),
    base.APIRule(
        name="identity:create_policy",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("!"),
        description="Create policy.",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/v3/policies"}],
    ),
    base.APIRule(
        name="identity:update_policy",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("!"),
        description="Update policy.",
        scope_types=["system"],
        operations=[{"method": "PATCH", "path": "/v3/policies/{policy_id}"}],
    ),
    base.APIRule(
        name="identity:delete_policy",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("!"),
        description="Delete policy.",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/v3/policies/{policy_id}"}],
    ),
    base.APIRule(
        name="identity:create_policy_association_for_endpoint",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("!"),
        description="Associate a policy to a specific endpoint.",
        scope_types=["system"],
        operations=[
            {
                "method": "PUT",
                "path": "/v3/policies/{policy_id}/OS-ENDPOINT-POLICY/endpoints/{endpoint_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:check_policy_association_for_endpoint",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("!"),
        description="Check policy association for endpoint.",
        scope_types=["system"],
        operations=[
            {
                "method": "GET",
                "path": "/v3/policies/{policy_id}/OS-ENDPOINT-POLICY/endpoints/{endpoint_id}",
            },
            {
                "method": "HEAD",
                "path": "/v3/policies/{policy_id}/OS-ENDPOINT-POLICY/endpoints/{endpoint_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:delete_policy_association_for_endpoint",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("!"),
        description="Delete policy association for endpoint.",
        scope_types=["system"],
        operations=[
            {
                "method": "DELETE",
                "path": "/v3/policies/{policy_id}/OS-ENDPOINT-POLICY/endpoints/{endpoint_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:create_policy_association_for_service",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("!"),
        description="Associate a policy to a specific service.",
        scope_types=["system"],
        operations=[
            {
                "method": "PUT",
                "path": "/v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:check_policy_association_for_service",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("!"),
        description="Check policy association for service.",
        scope_types=["system"],
        operations=[
            {
                "method": "GET",
                "path": "/v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}",
            },
            {
                "method": "HEAD",
                "path": "/v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:delete_policy_association_for_service",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("!"),
        description="Delete policy association for service.",
        scope_types=["system"],
        operations=[
            {
                "method": "DELETE",
                "path": "/v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:create_policy_association_for_region_and_service",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("!"),
        description="Associate a policy to a specific region and service combination.",
        scope_types=["system"],
        operations=[
            {
                "method": "PUT",
                "path": "/v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}/regions/{region_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:check_policy_association_for_region_and_service",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("!"),
        description="Check policy association for region and service.",
        scope_types=["system"],
        operations=[
            {
                "method": "GET",
                "path": "/v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}/regions/{region_id}",
            },
            {
                "method": "HEAD",
                "path": "/v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}/regions/{region_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:delete_policy_association_for_region_and_service",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("!"),
        description="Delete policy association for region and service.",
        scope_types=["system"],
        operations=[
            {
                "method": "DELETE",
                "path": "/v3/policies/{policy_id}/OS-ENDPOINT-POLICY/services/{service_id}/regions/{region_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:get_policy_for_endpoint",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("!"),
        description="Get policy for endpoint.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/endpoints/{endpoint_id}/OS-ENDPOINT-POLICY/policy"},
            {"method": "HEAD", "path": "/v3/endpoints/{endpoint_id}/OS-ENDPOINT-POLICY/policy"},
        ],
    ),
    base.APIRule(
        name="identity:list_endpoints_for_policy",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("!"),
        description="List endpoints for policy.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/policies/{policy_id}/OS-ENDPOINT-POLICY/endpoints"},
        ],
    ),
    base.APIRule(
        name="identity:get_project",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and domain_id:%(target.project.domain_id)s) or project_id:%(target.project.id)s"
        ),
        basic_check_str=("role:admin or role:reader or project_id:%(project_id)s"),
        description="Show project details.",
        scope_types=["system", "domain", "project"],
        operations=[{"method": "GET", "path": "/v3/projects/{project_id}"}],
    ),
    base.APIRule(
        name="identity:list_projects",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and domain_id:%(target.domain_id)s)"
        ),
        basic_check_str=("role:admin or role:reader"),
        description="List projects.",
        scope_types=["system", "domain"],
        operations=[{"method": "GET", "path": "/v3/projects"}],
    ),
    base.APIRule(
        name="identity:list_user_projects",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and domain_id:%(target.user.domain_id)s) or user_id:%(target.user.id)s"
        ),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="List projects for user.",
        scope_types=["system", "domain", "project"],
        operations=[{"method": "GET", "path": "/v3/users/{user_id}/projects"}],
    ),
    base.APIRule(
        name="identity:create_project",
        check_str=(
            "(role:admin and system_scope:all) or (role:admin and domain_id:%(target.project.domain_id)s)"
        ),
        basic_check_str=("role:admin"),
        description="Create project.",
        scope_types=["system", "domain"],
        operations=[{"method": "POST", "path": "/v3/projects"}],
    ),
    base.APIRule(
        name="identity:update_project",
        check_str=(
            "(role:admin and system_scope:all) or (role:admin and domain_id:%(target.project.domain_id)s)"
        ),
        basic_check_str=("role:admin"),
        description="Update project.",
        scope_types=["system", "domain"],
        operations=[{"method": "PATCH", "path": "/v3/projects/{project_id}"}],
    ),
    base.APIRule(
        name="identity:delete_project",
        check_str=(
            "(role:admin and system_scope:all) or (role:admin and domain_id:%(target.project.domain_id)s)"
        ),
        basic_check_str=("role:admin"),
        description="Delete project.",
        scope_types=["system", "domain"],
        operations=[{"method": "DELETE", "path": "/v3/projects/{project_id}"}],
    ),
    base.APIRule(
        name="identity:list_project_tags",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and domain_id:%(target.project.domain_id)s) or project_id:%(target.project.id)s"
        ),
        basic_check_str=("role:admin or role:reader or project_id:%(project_id)s"),
        description="List tags for a project.",
        scope_types=["system", "domain", "project"],
        operations=[
            {"method": "GET", "path": "/v3/projects/{project_id}/tags"},
            {"method": "HEAD", "path": "/v3/projects/{project_id}/tags"},
        ],
    ),
    base.APIRule(
        name="identity:get_project_tag",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and domain_id:%(target.project.domain_id)s) or project_id:%(target.project.id)s"
        ),
        basic_check_str=("role:admin or role:reader or project_id:%(project_id)s"),
        description="Check if project contains a tag.",
        scope_types=["system", "domain", "project"],
        operations=[
            {"method": "GET", "path": "/v3/projects/{project_id}/tags/{value}"},
            {"method": "HEAD", "path": "/v3/projects/{project_id}/tags/{value}"},
        ],
    ),
    base.APIRule(
        name="identity:update_project_tags",
        check_str=(
            "(role:admin and system_scope:all) or (role:admin and domain_id:%(target.project.domain_id)s) or (role:admin and project_id:%(target.project.id)s)"
        ),
        basic_check_str=("role:admin"),
        description="Replace all tags on a project with the new set of tags.",
        scope_types=["system", "domain", "project"],
        operations=[{"method": "PUT", "path": "/v3/projects/{project_id}/tags"}],
    ),
    base.APIRule(
        name="identity:create_project_tag",
        check_str=(
            "(role:admin and system_scope:all) or (role:admin and domain_id:%(target.project.domain_id)s) or (role:admin and project_id:%(target.project.id)s)"
        ),
        basic_check_str=("role:admin"),
        description="Add a single tag to a project.",
        scope_types=["system", "domain", "project"],
        operations=[{"method": "PUT", "path": "/v3/projects/{project_id}/tags/{value}"}],
    ),
    base.APIRule(
        name="identity:delete_project_tags",
        check_str=(
            "(role:admin and system_scope:all) or (role:admin and domain_id:%(target.project.domain_id)s) or (role:admin and project_id:%(target.project.id)s)"
        ),
        basic_check_str=("role:admin"),
        description="Remove all tags from a project.",
        scope_types=["system", "domain", "project"],
        operations=[{"method": "DELETE", "path": "/v3/projects/{project_id}/tags"}],
    ),
    base.APIRule(
        name="identity:delete_project_tag",
        check_str=(
            "(role:admin and system_scope:all) or (role:admin and domain_id:%(target.project.domain_id)s) or (role:admin and project_id:%(target.project.id)s)"
        ),
        basic_check_str=("role:admin"),
        description="Delete a specified tag from project.",
        scope_types=["system", "domain", "project"],
        operations=[{"method": "DELETE", "path": "/v3/projects/{project_id}/tags/{value}"}],
    ),
    base.APIRule(
        name="identity:list_projects_for_endpoint",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List projects allowed to access an endpoint.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/OS-EP-FILTER/endpoints/{endpoint_id}/projects"},
        ],
    ),
    base.APIRule(
        name="identity:add_endpoint_to_project",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Allow project to access an endpoint.",
        scope_types=["system"],
        operations=[
            {
                "method": "PUT",
                "path": "/v3/OS-EP-FILTER/projects/{project_id}/endpoints/{endpoint_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:check_endpoint_in_project",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Check if a project is allowed to access an endpoint.",
        scope_types=["system"],
        operations=[
            {
                "method": "GET",
                "path": "/v3/OS-EP-FILTER/projects/{project_id}/endpoints/{endpoint_id}",
            },
            {
                "method": "HEAD",
                "path": "/v3/OS-EP-FILTER/projects/{project_id}/endpoints/{endpoint_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:list_endpoints_for_project",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List the endpoints a project is allowed to access.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/OS-EP-FILTER/projects/{project_id}/endpoints"},
        ],
    ),
    base.APIRule(
        name="identity:remove_endpoint_from_project",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Remove access to an endpoint from a project that has previously been given explicit access.",
        scope_types=["system"],
        operations=[
            {
                "method": "DELETE",
                "path": "/v3/OS-EP-FILTER/projects/{project_id}/endpoints/{endpoint_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:create_protocol",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create federated protocol.",
        scope_types=["system"],
        operations=[
            {
                "method": "PUT",
                "path": "/v3/OS-FEDERATION/identity_providers/{idp_id}/protocols/{protocol_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:update_protocol",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update federated protocol.",
        scope_types=["system"],
        operations=[
            {
                "method": "PATCH",
                "path": "/v3/OS-FEDERATION/identity_providers/{idp_id}/protocols/{protocol_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:get_protocol",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get federated protocol.",
        scope_types=["system"],
        operations=[
            {
                "method": "GET",
                "path": "/v3/OS-FEDERATION/identity_providers/{idp_id}/protocols/{protocol_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:list_protocols",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List federated protocols.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/OS-FEDERATION/identity_providers/{idp_id}/protocols"},
        ],
    ),
    base.APIRule(
        name="identity:delete_protocol",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete federated protocol.",
        scope_types=["system"],
        operations=[
            {
                "method": "DELETE",
                "path": "/v3/OS-FEDERATION/identity_providers/{idp_id}/protocols/{protocol_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:get_region",
        check_str=(""),
        basic_check_str=("@"),
        description="Show region details.",
        scope_types=["system", "domain", "project"],
        operations=[
            {"method": "GET", "path": "/v3/regions/{region_id}"},
            {"method": "HEAD", "path": "/v3/regions/{region_id}"},
        ],
    ),
    base.APIRule(
        name="identity:list_regions",
        check_str=(""),
        basic_check_str=("@"),
        description="List regions.",
        scope_types=["system", "domain", "project"],
        operations=[
            {"method": "GET", "path": "/v3/regions"},
            {"method": "HEAD", "path": "/v3/regions"},
        ],
    ),
    base.APIRule(
        name="identity:create_region",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create region.",
        scope_types=["system"],
        operations=[
            {"method": "POST", "path": "/v3/regions"},
            {"method": "PUT", "path": "/v3/regions/{region_id}"},
        ],
    ),
    base.APIRule(
        name="identity:update_region",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update region.",
        scope_types=["system"],
        operations=[{"method": "PATCH", "path": "/v3/regions/{region_id}"}],
    ),
    base.APIRule(
        name="identity:delete_region",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete region.",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/v3/regions/{region_id}"}],
    ),
    base.APIRule(
        name="identity:get_registered_limit",
        check_str=(""),
        basic_check_str=("@"),
        description="Show registered limit details.",
        scope_types=["system", "domain", "project"],
        operations=[
            {"method": "GET", "path": "/v3/registered_limits/{registered_limit_id}"},
            {"method": "HEAD", "path": "/v3/registered_limits/{registered_limit_id}"},
        ],
    ),
    base.APIRule(
        name="identity:list_registered_limits",
        check_str=(""),
        basic_check_str=("@"),
        description="List registered limits.",
        scope_types=["system", "domain", "project"],
        operations=[
            {"method": "GET", "path": "/v3/registered_limits"},
            {"method": "HEAD", "path": "/v3/registered_limits"},
        ],
    ),
    base.APIRule(
        name="identity:create_registered_limits",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create registered limits.",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/v3/registered_limits"}],
    ),
    base.APIRule(
        name="identity:update_registered_limit",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update registered limit.",
        scope_types=["system"],
        operations=[{"method": "PATCH", "path": "/v3/registered_limits/{registered_limit_id}"}],
    ),
    base.APIRule(
        name="identity:delete_registered_limit",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete registered limit.",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/v3/registered_limits/{registered_limit_id}"}],
    ),
    base.APIRule(
        name="identity:list_revoke_events",
        check_str=("rule:service_or_admin"),
        basic_check_str=("role:admin"),
        description="List revocation events.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/v3/OS-REVOKE/events"}],
    ),
    base.APIRule(
        name="identity:get_role",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Show role details.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/roles/{role_id}"},
            {"method": "HEAD", "path": "/v3/roles/{role_id}"},
        ],
    ),
    base.APIRule(
        name="identity:list_roles",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List roles.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/roles"},
            {"method": "HEAD", "path": "/v3/roles"},
        ],
    ),
    base.APIRule(
        name="identity:create_role",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create role.",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/v3/roles"}],
    ),
    base.APIRule(
        name="identity:update_role",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update role.",
        scope_types=["system"],
        operations=[{"method": "PATCH", "path": "/v3/roles/{role_id}"}],
    ),
    base.APIRule(
        name="identity:delete_role",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete role.",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/v3/roles/{role_id}"}],
    ),
    base.APIRule(
        name="identity:get_domain_role",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Show domain role.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/roles/{role_id}"},
            {"method": "HEAD", "path": "/v3/roles/{role_id}"},
        ],
    ),
    base.APIRule(
        name="identity:list_domain_roles",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List domain roles.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/roles?domain_id={domain_id}"},
            {"method": "HEAD", "path": "/v3/roles?domain_id={domain_id}"},
        ],
    ),
    base.APIRule(
        name="identity:create_domain_role",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create domain role.",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/v3/roles"}],
    ),
    base.APIRule(
        name="identity:update_domain_role",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update domain role.",
        scope_types=["system"],
        operations=[{"method": "PATCH", "path": "/v3/roles/{role_id}"}],
    ),
    base.APIRule(
        name="identity:delete_domain_role",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete domain role.",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/v3/roles/{role_id}"}],
    ),
    base.APIRule(
        name="identity:list_role_assignments",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and domain_id:%(target.domain_id)s)"
        ),
        basic_check_str=(
            "role:admin or role:reader or project_id:%(project_id)s or user_id:%(user_id)s"
        ),
        description="List role assignments.",
        scope_types=["system", "domain"],
        operations=[
            {"method": "GET", "path": "/v3/role_assignments"},
            {"method": "HEAD", "path": "/v3/role_assignments"},
        ],
    ),
    base.APIRule(
        name="identity:list_role_assignments_for_tree",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and domain_id:%(target.project.domain_id)s) or (role:admin and project_id:%(target.project.id)s)"
        ),
        basic_check_str=("role:admin or role:reader"),
        description="List all role assignments for a given tree of hierarchical projects.",
        scope_types=["system", "domain", "project"],
        operations=[
            {"method": "GET", "path": "/v3/role_assignments?include_subtree"},
            {"method": "HEAD", "path": "/v3/role_assignments?include_subtree"},
        ],
    ),
    base.APIRule(
        name="identity:get_service",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Show service details.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/v3/services/{service_id}"}],
    ),
    base.APIRule(
        name="identity:list_services",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List services.",
        scope_types=["system"],
        operations=[{"method": "GET", "path": "/v3/services"}],
    ),
    base.APIRule(
        name="identity:create_service",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create service.",
        scope_types=["system"],
        operations=[{"method": "POST", "path": "/v3/services"}],
    ),
    base.APIRule(
        name="identity:update_service",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update service.",
        scope_types=["system"],
        operations=[{"method": "PATCH", "path": "/v3/services/{service_id}"}],
    ),
    base.APIRule(
        name="identity:delete_service",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete service.",
        scope_types=["system"],
        operations=[{"method": "DELETE", "path": "/v3/services/{service_id}"}],
    ),
    base.APIRule(
        name="identity:create_service_provider",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Create federated service provider.",
        scope_types=["system"],
        operations=[
            {
                "method": "PUT",
                "path": "/v3/OS-FEDERATION/service_providers/{service_provider_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:list_service_providers",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List federated service providers.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/OS-FEDERATION/service_providers"},
            {"method": "HEAD", "path": "/v3/OS-FEDERATION/service_providers"},
        ],
    ),
    base.APIRule(
        name="identity:get_service_provider",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="Get federated service provider.",
        scope_types=["system"],
        operations=[
            {
                "method": "GET",
                "path": "/v3/OS-FEDERATION/service_providers/{service_provider_id}",
            },
            {
                "method": "HEAD",
                "path": "/v3/OS-FEDERATION/service_providers/{service_provider_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:update_service_provider",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Update federated service provider.",
        scope_types=["system"],
        operations=[
            {
                "method": "PATCH",
                "path": "/v3/OS-FEDERATION/service_providers/{service_provider_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:delete_service_provider",
        check_str=("role:admin and system_scope:all"),
        basic_check_str=("role:admin"),
        description="Delete federated service provider.",
        scope_types=["system"],
        operations=[
            {
                "method": "DELETE",
                "path": "/v3/OS-FEDERATION/service_providers/{service_provider_id}",
            },
        ],
    ),
    base.APIRule(
        name="identity:revocation_list",
        check_str=("rule:service_or_admin"),
        basic_check_str=("!"),
        description="List revoked PKI tokens.",
        scope_types=["system", "project"],
        operations=[{"method": "GET", "path": "/v3/auth/tokens/OS-PKI/revoked"}],
    ),
    base.APIRule(
        name="identity:check_token",
        check_str=("(role:reader and system_scope:all) or rule:token_subject"),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="Check a token.",
        scope_types=["system", "domain", "project"],
        operations=[{"method": "HEAD", "path": "/v3/auth/tokens"}],
    ),
    base.APIRule(
        name="identity:validate_token",
        check_str=(
            "(role:reader and system_scope:all) or rule:service_role or rule:token_subject"
        ),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="Validate a token.",
        scope_types=["system", "domain", "project"],
        operations=[{"method": "GET", "path": "/v3/auth/tokens"}],
    ),
    base.APIRule(
        name="identity:revoke_token",
        check_str=("(role:admin and system_scope:all) or rule:token_subject"),
        basic_check_str=("role:admin or user_id:%(user_id)s"),
        description="Revoke a token.",
        scope_types=["system", "domain", "project"],
        operations=[{"method": "DELETE", "path": "/v3/auth/tokens"}],
    ),
    base.APIRule(
        name="identity:create_trust",
        check_str=("user_id:%(trust.trustor_user_id)s"),
        basic_check_str=("role:admin or user_id:%(user_id)s"),
        description="Create trust.",
        scope_types=["project"],
        operations=[{"method": "POST", "path": "/v3/OS-TRUST/trusts"}],
    ),
    base.APIRule(
        name="identity:list_trusts",
        check_str=("role:reader and system_scope:all"),
        basic_check_str=("role:admin or role:reader"),
        description="List trusts.",
        scope_types=["system"],
        operations=[
            {"method": "GET", "path": "/v3/OS-TRUST/trusts"},
            {"method": "HEAD", "path": "/v3/OS-TRUST/trusts"},
        ],
    ),
    base.APIRule(
        name="identity:list_trusts_for_trustor",
        check_str=(
            "role:reader and system_scope:all or user_id:%(target.trust.trustor_user_id)s"
        ),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="List trusts for trustor.",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/v3/OS-TRUST/trusts?trustor_user_id={trustor_user_id}"},
            {"method": "HEAD", "path": "/v3/OS-TRUST/trusts?trustor_user_id={trustor_user_id}"},
        ],
    ),
    base.APIRule(
        name="identity:list_trusts_for_trustee",
        check_str=(
            "role:reader and system_scope:all or user_id:%(target.trust.trustee_user_id)s"
        ),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="List trusts for trustee.",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/v3/OS-TRUST/trusts?trustee_user_id={trustee_user_id}"},
            {"method": "HEAD", "path": "/v3/OS-TRUST/trusts?trustee_user_id={trustee_user_id}"},
        ],
    ),
    base.APIRule(
        name="identity:list_roles_for_trust",
        check_str=(
            "role:reader and system_scope:all or user_id:%(target.trust.trustor_user_id)s or user_id:%(target.trust.trustee_user_id)s"
        ),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="List roles delegated by a trust.",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/v3/OS-TRUST/trusts/{trust_id}/roles"},
            {"method": "HEAD", "path": "/v3/OS-TRUST/trusts/{trust_id}/roles"},
        ],
    ),
    base.APIRule(
        name="identity:get_role_for_trust",
        check_str=(
            "role:reader and system_scope:all or user_id:%(target.trust.trustor_user_id)s or user_id:%(target.trust.trustee_user_id)s"
        ),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="Check if trust delegates a particular role.",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/v3/OS-TRUST/trusts/{trust_id}/roles/{role_id}"},
            {"method": "HEAD", "path": "/v3/OS-TRUST/trusts/{trust_id}/roles/{role_id}"},
        ],
    ),
    base.APIRule(
        name="identity:delete_trust",
        check_str=("role:admin and system_scope:all or user_id:%(target.trust.trustor_user_id)s"),
        basic_check_str=("role:admin or user_id:%(user_id)s"),
        description="Revoke trust.",
        scope_types=["system", "project"],
        operations=[{"method": "DELETE", "path": "/v3/OS-TRUST/trusts/{trust_id}"}],
    ),
    base.APIRule(
        name="identity:get_trust",
        check_str=(
            "role:reader and system_scope:all or user_id:%(target.trust.trustor_user_id)s or user_id:%(target.trust.trustee_user_id)s"
        ),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="Get trust.",
        scope_types=["system", "project"],
        operations=[
            {"method": "GET", "path": "/v3/OS-TRUST/trusts/{trust_id}"},
            {"method": "HEAD", "path": "/v3/OS-TRUST/trusts/{trust_id}"},
        ],
    ),
    base.APIRule(
        name="identity:get_user",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and token.domain.id:%(target.user.domain_id)s) or user_id:%(target.user.id)s"
        ),
        basic_check_str=("role:admin or role:reader or user_id:%(user_id)s"),
        description="Show user details.",
        scope_types=["system", "domain", "project"],
        operations=[
            {"method": "GET", "path": "/v3/users/{user_id}"},
            {"method": "HEAD", "path": "/v3/users/{user_id}"},
        ],
    ),
    base.APIRule(
        name="identity:list_users",
        check_str=(
            "(role:reader and system_scope:all) or (role:reader and domain_id:%(target.domain_id)s)"
        ),
        basic_check_str=("role:admin or role:reader"),
        description="List users.",
        scope_types=["system", "domain"],
        operations=[
            {"method": "GET", "path": "/v3/users"},
            {"method": "HEAD", "path": "/v3/users"},
        ],
    ),
    base.APIRule(
        name="identity:list_projects_for_user",
        check_str=(""),
        basic_check_str=("@"),
        description="List all projects a user has access to via role assignments.",
        scope_types=["project"],
        operations=[{"method": "GET", "path": " /v3/auth/projects"}],
    ),
    base.APIRule(
        name="identity:list_domains_for_user",
        check_str=(""),
        basic_check_str=("@"),
        description="List all domains a user has access to via role assignments.",
        scope_types=["project"],
        operations=[{"method": "GET", "path": "/v3/auth/domains"}],
    ),
    base.APIRule(
        name="identity:create_user",
        check_str=(
            "(role:admin and system_scope:all) or (role:admin and token.domain.id:%(target.user.domain_id)s)"
        ),
        basic_check_str=("role:admin"),
        description="Create a user.",
        scope_types=["system", "domain"],
        operations=[{"method": "POST", "path": "/v3/users"}],
    ),
    base.APIRule(
        name="identity:update_user",
        check_str=(
            "(role:admin and system_scope:all) or (role:admin and token.domain.id:%(target.user.domain_id)s)"
        ),
        basic_check_str=("role:admin"),
        description="Update a user, including administrative password resets.",
        scope_types=["system", "domain"],
        operations=[{"method": "PATCH", "path": "/v3/users/{user_id}"}],
    ),
    base.APIRule(
        name="identity:delete_user",
        check_str=(
            "(role:admin and system_scope:all) or (role:admin and token.domain.id:%(target.user.domain_id)s)"
        ),
        basic_check_str=("role:admin"),
        description="Delete a user.",
        scope_types=["system", "domain"],
        operations=[{"method": "DELETE", "path": "/v3/users/{user_id}"}],
    ),
)

__all__ = ("list_rules",)
