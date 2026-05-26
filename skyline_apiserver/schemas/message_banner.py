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

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class MessageBannerBase(BaseModel):
    type: Literal["maintenance", "notification"] = Field(
        ..., description="Banner type"
    )
    title: Optional[str] = Field(None, description="Banner title")
    message: str = Field(..., description="Banner message/details")
    impacted_service: Optional[str] = Field(
        None, description="Impacted service for maintenance banners"
    )
    start_at: Optional[datetime] = Field(
        None, description="Start date/time in UTC"
    )
    expires_at: datetime = Field(
        ..., description="Expiration date/time in UTC"
    )
    region: Optional[str] = Field(
        None, description="Region. Null means all regions"
    )


class CreateMessageBanner(MessageBannerBase):
    """"""


class UpdateMessageBanner(BaseModel):
    """All fields optional to support partial updates."""

    type: Optional[Literal["maintenance", "notification"]] = Field(
        None, description="Banner type"
    )
    title: Optional[str] = Field(None, description="Banner title")
    message: Optional[str] = Field(None, description="Banner message/details")
    impacted_service: Optional[str] = Field(
        None, description="Impacted service for maintenance banners"
    )
    start_at: Optional[datetime] = Field(
        None, description="Start date/time in UTC"
    )
    expires_at: Optional[datetime] = Field(
        None, description="Expiration date/time in UTC"
    )
    region: Optional[str] = Field(
        None, description="Region. Null means all regions"
    )
    enabled: Optional[bool] = Field(
        None, description="Whether banner is enabled"
    )


class MessageBanner(MessageBannerBase):
    id: str = Field(..., description="Banner ID")
    source: Literal["manual", "rss_feed"] = Field(
        "manual", description="Banner source"
    )
    source_id: Optional[str] = Field(
        None, description="External source identifier"
    )
    source_url: Optional[str] = Field(
        None, description="External source URL"
    )
    enabled: bool = Field(True, description="Whether banner is enabled")
    created_at: datetime = Field(..., description="Created time")
    updated_at: datetime = Field(..., description="Updated time")


class MessageBanners(BaseModel):
    message_banners: List[MessageBanner] = Field(
        ..., description="Message banners"
    )
