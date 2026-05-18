# Copyright 2021 99cloud
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

from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone
from functools import wraps
from typing import Any, Dict, List, Optional, Sequence, Union

from sqlalchemy import Insert, Update, delete, func, insert, or_, select, update
from sqlalchemy.sql.elements import ClauseElement

from skyline_apiserver.types import Fn

from .base import DB, inject_db
from .models import (
    MessageBanners,
    RevokedToken,
    Settings,
)


MESSAGE_BANNER_COLUMNS = set(MessageBanners.c.keys())
MESSAGE_BANNER_UPDATE_COLUMNS = MESSAGE_BANNER_COLUMNS - {"id", "created_at"}


def check_db_connected(fn: Fn) -> Any:
    @wraps(fn)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        await inject_db()
        db = DB.get()
        assert db is not None, "Database is not connected."
        return await fn(*args, **kwargs)

    return wrapper


@check_db_connected
async def check_token(token_id: str) -> bool:
    count_label = "revoked_count"
    query = (
        select(func.count(RevokedToken.c.uuid).label(count_label))
        .select_from(RevokedToken)
        .where(RevokedToken.c.uuid == token_id)
    )
    db = DB.get()
    async with db.transaction():
        result = await db.fetch_one(query)

    count = getattr(result, count_label, 0)
    return count > 0


@check_db_connected
async def revoke_token(token_id: str, expire: int) -> Any:
    query = insert(RevokedToken)
    db = DB.get()
    async with db.transaction():
        result = await db.execute(query, {"uuid": token_id, "expire": expire})

    return result


@check_db_connected
async def purge_revoked_token() -> Any:
    now = int(time.time()) - 1
    query = delete(RevokedToken).where(RevokedToken.c.expire < now)
    db = DB.get()
    async with db.transaction():
        result = await db.execute(query)

    return result


@check_db_connected
async def list_settings() -> Any:
    query = select(Settings)
    db = DB.get()
    async with db.transaction():
        result = await db.fetch_all(query)

    return result


@check_db_connected
async def get_setting(key: str) -> Any:
    query = select(Settings).where(Settings.c.key == key)
    db = DB.get()
    async with db.transaction():
        result = await db.fetch_one(query)

    return result


@check_db_connected
async def update_setting(key: str, value: Any) -> Any:
    get_query = (
        select(Settings.c.key, Settings.c.value).where(Settings.c.key == key).with_for_update()
    )
    db = DB.get()
    async with db.transaction():
        is_exist = await db.fetch_one(get_query)
        stmt: Union[Insert, Update]
        if is_exist is None:
            stmt = insert(Settings).values(key=key, value=value)
        else:
            stmt = update(Settings).where(Settings.c.key == key).values(value=value)
        await db.execute(stmt)
        result = await db.fetch_one(get_query)

    return result


@check_db_connected
async def delete_setting(key: str) -> Any:
    query = delete(Settings).where(Settings.c.key == key)
    db = DB.get()
    async with db.transaction():
        result = await db.execute(query)

    return result


def _region_conditions(
    region: Optional[str] = None,
) -> List[ClauseElement]:
    conditions: List[ClauseElement] = []
    if region:
        conditions.append(
            or_(
                MessageBanners.c.region.is_(None),
                MessageBanners.c.region == region,
            )
        )
    return conditions


@check_db_connected
async def list_message_banners(
    region: Optional[str] = None,
) -> Sequence[Any]:
    query = select(MessageBanners).order_by(MessageBanners.c.created_at.desc())
    conditions = _region_conditions(region=region)
    if conditions:
        query = query.where(*conditions)
    db = DB.get()
    async with db.transaction():
        result = await db.fetch_all(query)

    return result


@check_db_connected
async def list_active_message_banners(
    region: Optional[str] = None,
) -> Sequence[Any]:
    now = datetime.now(timezone.utc)
    conditions = [
        MessageBanners.c.enabled.is_(True),
        MessageBanners.c.expires_at > now,
    ]
    if region:
        conditions.extend(_region_conditions(region=region))
    query = (
        select(MessageBanners)
        .where(*conditions)
        .order_by(MessageBanners.c.created_at.desc())
    )
    db = DB.get()
    async with db.transaction():
        result = await db.fetch_all(query)

    return result


@check_db_connected
async def get_message_banner(banner_id: str) -> Optional[Any]:
    query = select(MessageBanners).where(MessageBanners.c.id == banner_id)
    db = DB.get()
    async with db.transaction():
        result = await db.fetch_one(query)

    return result


@check_db_connected
async def create_message_banner(values: Dict[str, Any]) -> Optional[Any]:
    now = datetime.now(timezone.utc)
    banner_id = values.get("id") or str(uuid.uuid4())
    filtered_values = {
        key: value for key, value in values.items() if key in MESSAGE_BANNER_COLUMNS
    }
    data = {
        **filtered_values,
        "id": banner_id,
        "created_at": values.get("created_at") or now,
        "updated_at": values.get("updated_at") or now,
    }
    query = insert(MessageBanners).values(**data)
    get_query = select(MessageBanners).where(MessageBanners.c.id == banner_id)
    db = DB.get()
    async with db.transaction():
        await db.execute(query)
        result = await db.fetch_one(get_query)

    return result


@check_db_connected
async def update_message_banner(banner_id: str, values: Dict[str, Any]) -> Optional[Any]:
    filtered_values = {
        key: value for key, value in values.items() if key in MESSAGE_BANNER_UPDATE_COLUMNS
    }
    data = {
        **filtered_values,
        "updated_at": datetime.now(timezone.utc),
    }
    query = (
        update(MessageBanners)
        .where(MessageBanners.c.id == banner_id)
        .values(**data)
    )
    get_query = select(MessageBanners).where(MessageBanners.c.id == banner_id)
    db = DB.get()
    async with db.transaction():
        await db.execute(query)
        result = await db.fetch_one(get_query)

    return result


@check_db_connected
async def delete_message_banner(banner_id: str) -> Optional[Any]:
    get_query = select(MessageBanners).where(MessageBanners.c.id == banner_id)
    delete_query = delete(MessageBanners).where(MessageBanners.c.id == banner_id)
    db = DB.get()
    async with db.transaction():
        result = await db.fetch_one(get_query)
        await db.execute(delete_query)
    return result


@check_db_connected
async def sync_rss_feed_ext_message_banner(values: Dict[str, Any]) -> Optional[Any]:
    source = values["source"]
    source_id = values["source_id"]
    get_query = select(MessageBanners).where(
        MessageBanners.c.source == source,
        MessageBanners.c.source_id == source_id,
    )
    db = DB.get()
    async with db.transaction():
        existing = await db.fetch_one(get_query)

    if existing is None:
        return await create_message_banner(values)
    update_values = values.copy()
    update_values.pop("enabled", None)
    return await update_message_banner(existing.id, update_values)
