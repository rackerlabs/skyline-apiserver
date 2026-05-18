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

import hashlib
import os
import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from xml.etree import ElementTree

import httpx
from bs4 import BeautifulSoup

from skyline_apiserver.log import LOG

RACKSPACE_STATUS_FEED_URL = "https://rss.status.rackspace.com/snow/statusfeed"
RACKSPACE_STATUS_PRODUCT = "OpenStack Flex"
RACKSPACE_STATUS_TIMEOUT = 10.0

DATETIME_RE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\b")
OUTAGE_RE = re.compile(r"\bOUT\d+\b")
CHANGE_RE = re.compile(r"\bCHG\d+\b")


def _html_to_text(html: str) -> str:
    return BeautifulSoup(html, "html.parser").get_text(separator="\n")


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value


def _float_env(name: str, default: float) -> float:
    value = _env(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        LOG.warning(f"Ignoring invalid float value for {name}: {value}")
        return default


def _feed_url() -> str:
    return _env("RACKSPACE_STATUS_FEED_URL", RACKSPACE_STATUS_FEED_URL)


def _normalize_text(text: str) -> str:
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def _parse_datetime(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").replace(
        tzinfo=timezone.utc
    )


def _parse_date_range(text: str) -> Optional[tuple[datetime, datetime]]:
    matches = DATETIME_RE.findall(text)
    if len(matches) < 2:
        return None
    try:
        start_at = _parse_datetime(matches[0])
        expires_at = _parse_datetime(matches[-1])
    except ValueError:
        return None
    if start_at >= expires_at:
        return None
    return start_at, expires_at


def _parse_single_datetime(text: str) -> Optional[datetime]:
    match = DATETIME_RE.search(text)
    if not match:
        return None
    return _parse_datetime(match.group(0))


def _split_title(title: str) -> List[str]:
    return [part.strip() for part in title.split("|") if part.strip()]


def _is_openstack_flex_item(title: str) -> bool:
    parts = _split_title(title)
    return bool(parts and parts[0].lower() == RACKSPACE_STATUS_PRODUCT.lower())


def _title_region(title: str) -> Optional[str]:
    parts = _split_title(title)
    if len(parts) < 2:
        return None
    return parts[1]


def _normalize_region(region: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", region.upper())


def _extract_source_id(text: str, link: Optional[str], guid: Optional[str] = None) -> str:
    if guid:
        return guid

    outage_match = OUTAGE_RE.search(text)
    if outage_match:
        return outage_match.group(0)

    change_match = CHANGE_RE.search(text)
    if change_match:
        return change_match.group(0)

    raw_id = link or text
    digest = hashlib.sha256(raw_id.encode("utf-8")).hexdigest()[:24]
    return f"rss-{digest}"


def _message_id(source_id: str) -> str:
    return f"rss-feed-{source_id}"


def _message_type(text: str) -> str:
    if "maintenance" in text.lower():
        return "maintenance"
    return "notification"


def _message_text(title: str, description: str) -> str:
    match = re.search(r"\bRackspace will\b", description, re.IGNORECASE)
    if match is not None:
        message = description[match.start():]
    else:
        message = description
    message = DATETIME_RE.sub("", message).strip()
    return message or title


def _item_text(item: ElementTree.Element, tag: str) -> Optional[str]:
    value = item.findtext(tag)
    if value is None:
        return None
    return value.strip()


def _item_to_message_banner_values(
    item: ElementTree.Element,
) -> Optional[Dict[str, Any]]:
    title = _item_text(item, "title") or ""
    if not _is_openstack_flex_item(title):
        return None

    link = _item_text(item, "link")
    guid = _item_text(item, "guid")
    raw_description = _item_text(item, "description") or ""
    description = _normalize_text(_html_to_text(raw_description))
    date_range = _parse_date_range(description)
    if date_range is not None:
        start_at, expires_at = date_range
    else:
        single_dt = _parse_single_datetime(description)
        now = datetime.now(timezone.utc)
        if single_dt is not None and single_dt > now:
            LOG.info(f"Only start_at found for RSS item, expires 1 hour after start: {title}")
            start_at = single_dt
            expires_at = single_dt + timedelta(hours=1)
        else:
            LOG.info(f"No valid date range found for RSS item, applying 1-hour TTL: {title}")
            start_at = None
            expires_at = now + timedelta(hours=1)
    source_id = _extract_source_id(description, link, guid)
    item_region = _title_region(title)
    return {
        "id": _message_id(source_id),
        "type": _message_type(f"{title}\n{description}"),
        "title": title,
        "message": _message_text(title, description),
        "impacted_service": RACKSPACE_STATUS_PRODUCT,
        "start_at": start_at,
        "expires_at": expires_at,
        "region": item_region,
        "source": "rss_feed",
        "source_id": source_id,
        "source_url": link,
        "enabled": True,
    }


async def fetch_rss_feed_message_banner_values() -> List[Dict[str, Any]]:
    """Fetch OpenStack Flex RSS feed items as DB-ready banner values."""

    try:
        async with httpx.AsyncClient(
            timeout=_float_env("RACKSPACE_STATUS_TIMEOUT", RACKSPACE_STATUS_TIMEOUT),
        ) as client:
            response = await client.get(_feed_url())
            response.raise_for_status()
            root = ElementTree.fromstring(response.content)
    except Exception as exc:
        LOG.warning(f"Failed to fetch Rackspace status feed: {exc}")
        return []

    banner_values = []
    seen_ids = set()
    for item in root.findall("./channel/item"):
        values = _item_to_message_banner_values(item)
        if values is None or values["id"] in seen_ids:
            continue

        seen_ids.add(values["id"])
        banner_values.append(values)

    return banner_values
