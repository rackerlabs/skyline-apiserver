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

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from skyline_apiserver.config import openstack
from skyline_apiserver.policy.base import Enforcer
from skyline_apiserver.policy.manager.cloudkitty import list_rules
from skyline_apiserver.types.constants import SUPPORTED_SERVICE_EPS


@pytest.mark.parametrize(
    "rule", ["summary:get_summary", "report:get_summary", "report:get_total"]
)
@pytest.mark.parametrize(
    "roles, project_id, allowed",
    [
        (["reader"], "project-a", True),
        (["reader"], "project-b", False),
        (["member"], "project-a", True),
        (["member"], "project-b", False),
        (["_member_"], "project-a", True),
        (["_member_"], "project-b", False),
        (["reader"], None, False),
        (["member"], None, False),
        (["_member_"], None, False),
        (["admin"], "project-b", True),
        ([], "project-a", False),
    ],
)
def test_summary_permissions(monkeypatch, rule, roles, project_id, allowed):
    monkeypatch.setattr(Enforcer, "load_rules", lambda self: None)
    enforcer = Enforcer(service="cloudkitty")
    enforcer.register_rules(list_rules)
    assert (
        enforcer.authorize(
            rule,
            {"project_id": "project-a"},
            {"roles": roles, "project_id": project_id},
        )
        is allowed
    )


@pytest.mark.parametrize(
    "rule",
    [
        "rating:list_modules",
        "rating:get_module",
        "rating:update_module",
        "rating:module_config",
        "report:list_tenants",
    ],
)
def test_configuration_requires_admin(monkeypatch, rule):
    monkeypatch.setattr(Enforcer, "load_rules", lambda self: None)
    enforcer = Enforcer(service="cloudkitty")
    enforcer.register_rules(list_rules)
    for roles in (["reader"], ["member"], ["_member_"], []):
        assert not enforcer.authorize(rule, {}, {"roles": roles})
    assert enforcer.authorize(rule, {}, {"roles": ["admin"]})


@pytest.mark.parametrize("version", ["", "/v1", "/v2"])
def test_rating_catalog_proxy(monkeypatch, version):
    pytest.importorskip("skyline_console")
    from skyline_apiserver.cmd import generate_nginx

    client = Mock()
    client.services.list.return_value = [SimpleNamespace(id="rating-id", type="rating")]
    client.endpoints.list.return_value = [
        SimpleNamespace(
            service_id="rating-id",
            region="RegionOne",
            url="https://rating.example:8889" + version,
        )
    ]
    monkeypatch.setattr(generate_nginx, "get_system_session", lambda: None)
    monkeypatch.setattr(generate_nginx, "KeystoneClient", lambda **kwargs: client)
    monkeypatch.setattr(
        generate_nginx,
        "CONF",
        SimpleNamespace(
            openstack=SimpleNamespace(
                service_mapping=openstack.service_mapping.default,
                interface_type="public",
                default_region="RegionOne",
                nginx_prefix="/api/openstack",
                qonos_endpoint="",
            )
        ),
    )
    endpoint = generate_nginx.get_proxy_endpoints()["RegionOne-rating"]
    assert endpoint.location == "/api/openstack/regionone/cloudkitty/"
    assert endpoint.url == "https://rating.example:8889/"
    assert SUPPORTED_SERVICE_EPS["cloudkitty"] == ["cloudkitty"]


def test_generate_cloudkitty_policy(tmp_path):
    from click.testing import CliRunner

    from skyline_apiserver.cmd.policy_manager import generate_conf

    result = CliRunner().invoke(generate_conf, ["--dir", str(tmp_path)])
    assert result.exit_code == 0, result.output
    policy = (tmp_path / "cloudkitty" / "policy.yaml").read_text()
    for name in ("summary:get_summary", "rating:update_module", "report:get_summary"):
        assert '"' + name + '"' in policy
