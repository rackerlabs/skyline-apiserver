# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0

from __future__ import annotations
from typing import Any, Dict, Optional

from fastapi import APIRouter, Body, Depends, Header, HTTPException, Query, status
from keystoneauth1.session import Session

from skyline_apiserver import schemas
from skyline_apiserver.api import deps
from skyline_apiserver.client.openstack import freezer
from skyline_apiserver.client.utils import generate_session
from skyline_apiserver.types import constants

router = APIRouter()


@router.get(
    "/extension/freezer/jobs",
    description="List Freezer Jobs",
    response_model=schemas.FreezerJobsResponse,
    status_code=status.HTTP_200_OK,
)
async def list_jobs(
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header("", alias=constants.INBOUND_HEADER, regex=constants.INBOUND_HEADER_REGEX),
    limit: int = Query(500),
    offset: int = Query(0),
    search: Optional[str] = Query(None),
) -> schemas.FreezerJobsResponse:
    session = await generate_session(profile=profile)
    search_query = {"match": [{"_all": search}]} if search else None
    jobs = await freezer.list_jobs(profile=profile, session=session, global_request_id=x_openstack_request_id, limit=limit, offset=offset, search=search_query)
    return schemas.FreezerJobsResponse(jobs=jobs)


@router.get(
    "/extension/freezer/jobs/{job_id}",
    description="Get Freezer Job",
    response_model=schemas.FreezerJobResponse,
    status_code=status.HTTP_200_OK,
)
async def get_job(
    job_id: str,
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header("", alias=constants.INBOUND_HEADER, regex=constants.INBOUND_HEADER_REGEX),
) -> schemas.FreezerJobResponse:
    session = await generate_session(profile=profile)
    job = await freezer.get_job(profile=profile, session=session, global_request_id=x_openstack_request_id, job_id=job_id)
    return schemas.FreezerJobResponse(**job)


@router.post(
    "/extension/freezer/jobs",
    description="Create Freezer Job",
    response_model=schemas.FreezerCreatedResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_job(
    body: schemas.FreezerJobCreate = Body(...),
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header("", alias=constants.INBOUND_HEADER, regex=constants.INBOUND_HEADER_REGEX),
) -> schemas.FreezerCreatedResponse:
    session = await generate_session(profile=profile)
    job_id = await freezer.create_job(profile=profile, session=session, global_request_id=x_openstack_request_id, job=body.dict(exclude_none=True))
    return schemas.FreezerCreatedResponse(id=job_id)


@router.delete(
    "/extension/freezer/jobs/{job_id}",
    description="Delete Freezer Job",
    response_model=schemas.FreezerMessageResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_job(
    job_id: str,
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header("", alias=constants.INBOUND_HEADER, regex=constants.INBOUND_HEADER_REGEX),
) -> schemas.FreezerMessageResponse:
    session = await generate_session(profile=profile)
    await freezer.delete_job(profile=profile, session=session, global_request_id=x_openstack_request_id, job_id=job_id)
    return schemas.FreezerMessageResponse(message="Job deleted successfully")


@router.post(
    "/extension/freezer/jobs/{job_id}/start",
    description="Start Freezer Job",
    response_model=schemas.FreezerMessageResponse,
    status_code=status.HTTP_200_OK,
)
async def start_job(
    job_id: str,
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header("", alias=constants.INBOUND_HEADER, regex=constants.INBOUND_HEADER_REGEX),
) -> schemas.FreezerMessageResponse:
    session = await generate_session(profile=profile)
    await freezer.start_job(profile=profile, session=session, global_request_id=x_openstack_request_id, job_id=job_id)
    return schemas.FreezerMessageResponse(message="Job started successfully")


@router.post(
    "/extension/freezer/jobs/{job_id}/stop",
    description="Stop Freezer Job",
    response_model=schemas.FreezerMessageResponse,
    status_code=status.HTTP_200_OK,
)
async def stop_job(
    job_id: str,
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header("", alias=constants.INBOUND_HEADER, regex=constants.INBOUND_HEADER_REGEX),
) -> schemas.FreezerMessageResponse:
    session = await generate_session(profile=profile)
    await freezer.stop_job(profile=profile, session=session, global_request_id=x_openstack_request_id, job_id=job_id)
    return schemas.FreezerMessageResponse(message="Job stopped successfully")


@router.get(
    "/extension/freezer/actions",
    description="List Freezer Actions",
    response_model=schemas.FreezerActionsResponse,
    status_code=status.HTTP_200_OK,
)
async def list_actions(
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header("", alias=constants.INBOUND_HEADER, regex=constants.INBOUND_HEADER_REGEX),
    limit: int = Query(500),
    offset: int = Query(0),
    search: Optional[str] = Query(None),
) -> schemas.FreezerActionsResponse:
    session = await generate_session(profile=profile)
    search_query = {"match": [{"_all": search}]} if search else None
    actions = await freezer.list_actions(profile=profile, session=session, global_request_id=x_openstack_request_id, limit=limit, offset=offset, search=search_query)
    return schemas.FreezerActionsResponse(actions=actions)


@router.get(
    "/extension/freezer/actions/{action_id}",
    description="Get Freezer Action",
    response_model=schemas.FreezerActionResponse,
    status_code=status.HTTP_200_OK,
)
async def get_action(
    action_id: str,
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header("", alias=constants.INBOUND_HEADER, regex=constants.INBOUND_HEADER_REGEX),
) -> schemas.FreezerActionResponse:
    session = await generate_session(profile=profile)
    action = await freezer.get_action(profile=profile, session=session, global_request_id=x_openstack_request_id, action_id=action_id)
    return schemas.FreezerActionResponse(**action)


@router.post(
    "/extension/freezer/actions",
    description="Create Freezer Action",
    response_model=schemas.FreezerCreatedResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_action(
    body: schemas.FreezerActionCreate = Body(...),
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header("", alias=constants.INBOUND_HEADER, regex=constants.INBOUND_HEADER_REGEX),
) -> schemas.FreezerCreatedResponse:
    session = await generate_session(profile=profile)
    action_id = await freezer.create_action(profile=profile, session=session, global_request_id=x_openstack_request_id, action=body.dict(exclude_none=True))
    return schemas.FreezerCreatedResponse(id=action_id)


@router.delete(
    "/extension/freezer/actions/{action_id}",
    description="Delete Freezer Action",
    response_model=schemas.FreezerMessageResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_action(
    action_id: str,
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header("", alias=constants.INBOUND_HEADER, regex=constants.INBOUND_HEADER_REGEX),
) -> schemas.FreezerMessageResponse:
    session = await generate_session(profile=profile)
    await freezer.delete_action(profile=profile, session=session, global_request_id=x_openstack_request_id, action_id=action_id)
    return schemas.FreezerMessageResponse(message="Action deleted successfully")


@router.get(
    "/extension/freezer/clients",
    description="List Freezer Clients",
    response_model=schemas.FreezerClientsResponse,
    status_code=status.HTTP_200_OK,
)
async def list_clients(
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header("", alias=constants.INBOUND_HEADER, regex=constants.INBOUND_HEADER_REGEX),
    limit: int = Query(500),
    offset: int = Query(0),
    search: Optional[str] = Query(None),
) -> schemas.FreezerClientsResponse:
    session = await generate_session(profile=profile)
    search_query = {"match": [{"_all": search}]} if search else None
    clients = await freezer.list_clients(profile=profile, session=session, global_request_id=x_openstack_request_id, limit=limit, offset=offset, search=search_query)
    return schemas.FreezerClientsResponse(clients=clients)


@router.delete(
    "/extension/freezer/clients/{client_id}",
    description="Delete Freezer Client",
    response_model=schemas.FreezerMessageResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_client(
    client_id: str,
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header("", alias=constants.INBOUND_HEADER, regex=constants.INBOUND_HEADER_REGEX),
) -> schemas.FreezerMessageResponse:
    session = await generate_session(profile=profile)
    await freezer.delete_client(profile=profile, session=session, global_request_id=x_openstack_request_id, client_id=client_id)
    return schemas.FreezerMessageResponse(message="Client deleted successfully")


@router.get(
    "/extension/freezer/backups",
    description="List Freezer Backups",
    response_model=schemas.FreezerBackupsResponse,
    status_code=status.HTTP_200_OK,
)
async def list_backups(
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header("", alias=constants.INBOUND_HEADER, regex=constants.INBOUND_HEADER_REGEX),
    limit: int = Query(500),
    offset: int = Query(0),
    search: Optional[str] = Query(None),
) -> schemas.FreezerBackupsResponse:
    session = await generate_session(profile=profile)
    search_query = {"match": [{"_all": search}]} if search else None
    backups = await freezer.list_backups(profile=profile, session=session, global_request_id=x_openstack_request_id, limit=limit, offset=offset, search=search_query)
    return schemas.FreezerBackupsResponse(backups=backups)


@router.delete(
    "/extension/freezer/backups/{backup_id}",
    description="Delete Freezer Backup",
    response_model=schemas.FreezerMessageResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_backup(
    backup_id: str,
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header("", alias=constants.INBOUND_HEADER, regex=constants.INBOUND_HEADER_REGEX),
) -> schemas.FreezerMessageResponse:
    session = await generate_session(profile=profile)
    await freezer.delete_backup(profile=profile, session=session, global_request_id=x_openstack_request_id, backup_id=backup_id)
    return schemas.FreezerMessageResponse(message="Backup deleted successfully")


@router.post(
    "/extension/freezer/backups/{backup_id}/restore",
    description="Restore a Freezer Backup",
    response_model=schemas.FreezerMessageResponse,
    status_code=status.HTTP_200_OK,
)
async def restore_backup(
    backup_id: str,
    body: schemas.FreezerBackupRestore = Body(...),
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header("", alias=constants.INBOUND_HEADER, regex=constants.INBOUND_HEADER_REGEX),
) -> schemas.FreezerMessageResponse:
    session = await generate_session(profile=profile)
    backups = await freezer.list_backups(profile=profile, session=session, global_request_id=x_openstack_request_id, limit=1, offset=0, search={"match": [{"backup_id": backup_id}]})
    if not backups:
        raise HTTPException(status_code=404, detail="Backup not found")
    backup = backups[0]
    meta = backup.get("backup_metadata", {})

    backup_name = (
        meta.get("backup_name")
        or backup.get("backup_name")
        or body.backup_id
    )
    container = (
        meta.get("container")
        or backup.get("container")
        or ""
    )
    storage = (
        meta.get("storage")
        or backup.get("storage")
        or "local"
    )
    hostname = (
        meta.get("hostname")
        or backup.get("hostname")
        or ""
    )

    mode = meta.get("mode") or "fs"

    freezer_action: Dict[str, Any] = {
        "action": "restore",
        "backup_name": backup_name,
        "container": container,
        "hostname": hostname,
        "storage": storage,
        "mode": mode,
    }

    if mode == "nova":
        freezer_action["engine_name"] = "nova"
        freezer_action["nova-inst-id"] = meta.get("nova_inst_id")
        freezer_action["restore_abs_path"] = "/tmp/freezer-nova-restore"
        if body.network_id:
            freezer_action["nova-restore-network"] = body.network_id
    elif mode == "cinder":
        freezer_action["cinder_vol_id"] = meta.get("cinder_vol_id")
    else:
        freezer_action["restore_abs_path"] = body.path
        freezer_action["overwrite"] = True

    action_data: Dict[str, Any] = {"freezer_action": freezer_action}

    if storage == "ssh":
        action_data["freezer_action"].update({
            "ssh_host": meta.get("ssh_host"),
            "ssh_key": meta.get("ssh_key"),
            "ssh_username": meta.get("ssh_username"),
            "ssh_port": meta.get("ssh_port"),
        })
    action_id = await freezer.create_action(profile=profile, session=session, global_request_id=x_openstack_request_id, action=action_data)

    job_data: Dict[str, Any] = {
        "job_actions": [{"action_id": action_id, "freezer_action": action_data["freezer_action"]}],
        "client_id": body.client,
        "description": f"Restore {meta.get('backup_name')} for {body.client}",
        "job_schedule": {},
    }
    job_id = await freezer.create_job(profile=profile, session=session, global_request_id=x_openstack_request_id, job=job_data)
    await freezer.start_job(profile=profile, session=session, global_request_id=x_openstack_request_id, job_id=job_id)
    return schemas.FreezerMessageResponse(message="Restore job started successfully")


def _build_bootstrap_script(
    instance_name: str,
    username: str,
    password: str,
    project_id: str,
    user_domain_name: str,
    project_domain_name: str,
    keystone_url: str,
    freezer_url: str,
) -> str:
    """Build the shell script that installs and configures freezer-scheduler
    on a VM using username/password auth (Option D).

    NOTE: freezerclient only supports password/token auth, so we use the
    user's own credentials here. Any '$' in the password must be doubled
    ('$$') because oslo_config performs variable substitution on values.

    This script is returned to the caller as both:
      - user_data  (cloud-init, for Skyline-created VMs — injected at boot)
      - bootstrap_script  (for existing/CLI VMs — user pastes it via SSH)
    """
    # '$' must be doubled for oslo_config; systemd needs the raw value.
    escaped_password = password.replace("$", "$$")  # for oslo_config .conf
    raw_password = password                          # for systemd Environment=

    return f"""#!/bin/bash
# Freezer backup bootstrap — generated by Skyline
# Registers this VM under the owning tenant's project.
set -euo pipefail

# Idempotent: skip if already installed
if [ -f /opt/freezer-venv/bin/freezer-scheduler ]; then
    echo "Freezer already installed on {instance_name}, skipping."
    exit 0
fi

echo "Installing Freezer on {instance_name}..."

# Multi-distro package install: works across Debian/Ubuntu (apt),
# RHEL/Rocky/Alma/CentOS/Fedora (dnf/yum) and openSUSE/SLES (zypper).
if command -v apt-get >/dev/null 2>&1; then
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq
    apt-get install -y -qq python3-dev python3-venv python3-pip libssl-dev gcc git
elif command -v dnf >/dev/null 2>&1; then
    dnf install -y python3 python3-devel python3-pip openssl-devel gcc git
elif command -v yum >/dev/null 2>&1; then
    yum install -y python3 python3-devel python3-pip openssl-devel gcc git
elif command -v zypper >/dev/null 2>&1; then
    zypper --non-interactive install python3 python3-devel python3-pip libopenssl-devel gcc git
else
    echo "No supported package manager found (apt/dnf/yum/zypper)." >&2
    exit 1
fi

python3 -m venv /opt/freezer-venv
/opt/freezer-venv/bin/pip install --quiet --upgrade pip
/opt/freezer-venv/bin/pip install --quiet pymysql git+https://opendev.org/openstack/freezer.git@master

SITE_PACKAGES=$(/opt/freezer-venv/bin/python -c 'import site; print(site.getsitepackages()[0])')
echo 'import warnings; warnings.simplefilter("ignore")' \
    > "$SITE_PACKAGES/zzz_suppress_warnings.pth"

mkdir -p /etc/freezer /var/log/freezer /var/lib/freezer

# Write scheduler config. Auth must be provided BOTH as deprecated os-*
# keys under [DEFAULT] AND in [service_auth] — the [service_auth] section
# alone does not bind reliably in this freezerclient version.
cat > /etc/freezer/freezer-scheduler.conf <<'FCONF_END'
[DEFAULT]
log_file = /var/log/freezer/scheduler.log
os-auth-url = {keystone_url}
os-backup-url = {freezer_url}
os-username = {username}
os-password = {escaped_password}
os-project-id = {project_id}
os-user-domain-name = {user_domain_name}
os-project-domain-name = {project_domain_name}
os-identity-api-version = 3
os-endpoint-type = publicURL

[scheduler]
client-id = {instance_name}
jobs-dir = /var/lib/freezer
interval = 60
insecure = true

[service_auth]
auth-url = {keystone_url}
backup-url = {freezer_url}
username = {username}
password = {escaped_password}
project-id = {project_id}
user-domain-name = {user_domain_name}
project-domain-name = {project_domain_name}
identity-api-version = 3
endpoint-type = publicURL
FCONF_END

chmod 640 /etc/freezer/freezer-scheduler.conf

# IMPORTANT: Environment= lines pass credentials to child freezer-agent
# process for restore operations (agent spawned by scheduler needs auth).
cat > /etc/systemd/system/freezer-scheduler.service <<'FSVC_END'
[Unit]
Description=Freezer Scheduler
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
Environment="OS_AUTH_URL={keystone_url}"
Environment="OS_USERNAME={username}"
Environment="OS_PASSWORD={raw_password}"
Environment="OS_USER_DOMAIN_NAME={user_domain_name}"
Environment="OS_PROJECT_DOMAIN_NAME={project_domain_name}"
Environment="OS_PROJECT_ID={project_id}"
Environment="OS_IDENTITY_API_VERSION=3"
Environment="OS_ENDPOINT_TYPE=publicURL"
Environment="OS_INSECURE=true"
Environment="PYTHONHTTPSVERIFY=0"
Environment="PYTHONWARNINGS=ignore"
ExecStart=/opt/freezer-venv/bin/freezer-scheduler \\
    --config-file /etc/freezer/freezer-scheduler.conf \\
    --no-daemon start
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
FSVC_END

systemctl daemon-reload
systemctl enable freezer-scheduler
systemctl start freezer-scheduler

echo "Freezer scheduler installed and started on {instance_name}"
"""


@router.post(
    "/extension/freezer/enable-backup",
    description=(
        "Prepare per-tenant Freezer backup enablement for a Skyline-created VM. "
        "Builds cloud-init user-data (using the caller's own username/password) "
        "that the console injects into the Nova boot request with config-drive, "
        "so the freezer agent + scheduler install automatically on first boot. "
        "The VM is registered under the caller's own project. No admin privilege "
        "and no application credential are used."
    ),
    response_model=schemas.FreezerEnableBackupResponse,
    status_code=status.HTTP_201_CREATED,
)
async def enable_backup(
    body: schemas.FreezerEnableBackupRequest = Body(...),
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header(
        "",
        alias=constants.INBOUND_HEADER,
        regex=constants.INBOUND_HEADER_REGEX,
    ),
) -> schemas.FreezerEnableBackupResponse:
    session = await generate_session(profile=profile)

    # Caller supplies the password; everything else defaults to their profile.
    username = body.username or profile.user.name
    project_id = body.project_id or profile.project.id
    user_domain_name = body.user_domain_name or profile.user.domain.name
    project_domain_name = (
        body.project_domain_name or profile.project.domain.name
    )

    from skyline_apiserver.client.utils import get_endpoint

    # VM reaches only public endpoints, independent of apiserver interface_type.
    keystone_url = await get_endpoint(
        region=profile.region,
        service="identity",
        session=session,
        interface="public",
    )
    freezer_url = await get_endpoint(
        region=profile.region,
        service="backup",
        session=session,
        interface="public",
    )

    script = _build_bootstrap_script(
        instance_name=body.instance_name,
        username=username,
        password=body.password,
        project_id=project_id,
        user_domain_name=user_domain_name,
        project_domain_name=project_domain_name,
        keystone_url=keystone_url,
        freezer_url=freezer_url,
    )

    # SECURITY: the script embeds the caller's password; returned only as
    # cloud-init user-data and never logged.
    return schemas.FreezerEnableBackupResponse(
        instance_id=body.instance_id,
        instance_name=body.instance_name,
        project_id=profile.project.id,
        user_data=script,
    )


async def _iter_client_jobs(
    profile: schemas.Profile,
    session: Session,
    global_request_id: str,
    client_id: str,
) -> list:
    """Return all Freezer jobs registered under the given client.

    Freezer namespaces the client_id as ``<project_id>_<client_id>`` (e.g.
    ``f33654...fed5_myvm``). The caller passes the bare instance name, so an
    exact match on that alone misses the real records. We list the caller's
    jobs and match any of:
      - the bare name (``myvm``),
      - the project-prefixed form (``<project_id>_myvm``),
      - any ``<prefix>_myvm`` suffix (defensive, in case the prefix differs).
    """
    jobs = await freezer.list_jobs(
        profile=profile,
        session=session,
        global_request_id=global_request_id,
        limit=500,
        offset=0,
        search=None,
    )
    project_id = getattr(profile.project, "id", "") or ""
    candidates = {client_id, "{0}_{1}".format(project_id, client_id)}
    suffix = "_{0}".format(client_id)
    matched = []
    for job in jobs:
        jid = job.get("client_id") or ""
        if jid in candidates or jid.endswith(suffix):
            matched.append(job)
    return matched


@router.post(
    "/extension/freezer/disable-backup",
    description=(
        "Pause Freezer backup for a VM. Stops all scheduled jobs registered "
        "under the VM's Freezer client using the caller's own session token — "
        "no password and no application credential are involved. Existing "
        "backups in object storage are retained, and the agent stays installed "
        "so backup can be resumed later. Idempotent."
    ),
    response_model=schemas.FreezerMessageResponse,
    status_code=status.HTTP_200_OK,
)
async def disable_backup(
    body: schemas.FreezerDisableBackupRequest = Body(...),
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header(
        "",
        alias=constants.INBOUND_HEADER,
        regex=constants.INBOUND_HEADER_REGEX,
    ),
) -> schemas.FreezerMessageResponse:
    session = await generate_session(profile=profile)
    client_id = body.client_id or body.instance_id

    jobs = await _iter_client_jobs(
        profile=profile,
        session=session,
        global_request_id=x_openstack_request_id,
        client_id=client_id,
    )

    stopped = 0
    for job in jobs:
        job_id = job.get("job_id")
        if not job_id:
            continue
        await freezer.stop_job(
            profile=profile,
            session=session,
            global_request_id=x_openstack_request_id,
            job_id=job_id,
        )
        stopped += 1

    return schemas.FreezerMessageResponse(
        message=(
            f"Backup paused for instance {body.instance_id}: stopped {stopped} "
            f"scheduled job(s). Existing backups are retained."
        )
    )


@router.post(
    "/extension/freezer/resume-backup",
    description=(
        "Resume a previously paused VM's Freezer backup by re-starting its "
        "scheduled jobs. Password-less — valid only when the agent is already "
        "installed on the VM (enabled at create time). Idempotent."
    ),
    response_model=schemas.FreezerMessageResponse,
    status_code=status.HTTP_200_OK,
)
async def resume_backup(
    body: schemas.FreezerResumeBackupRequest = Body(...),
    profile: schemas.Profile = Depends(deps.get_profile_update_jwt),
    x_openstack_request_id: str = Header(
        "",
        alias=constants.INBOUND_HEADER,
        regex=constants.INBOUND_HEADER_REGEX,
    ),
) -> schemas.FreezerMessageResponse:
    session = await generate_session(profile=profile)
    client_id = body.client_id or body.instance_id

    jobs = await _iter_client_jobs(
        profile=profile,
        session=session,
        global_request_id=x_openstack_request_id,
        client_id=client_id,
    )

    started = 0
    for job in jobs:
        job_id = job.get("job_id")
        if not job_id:
            continue
        await freezer.start_job(
            profile=profile,
            session=session,
            global_request_id=x_openstack_request_id,
            job_id=job_id,
        )
        started += 1

    return schemas.FreezerMessageResponse(
        message=(
            f"Backup resumed for instance {body.instance_id}: started "
            f"{started} scheduled job(s)."
        )
    )
