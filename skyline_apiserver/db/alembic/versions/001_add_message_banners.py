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

"""add message banners

Revision ID: 001
Revises: 000
Create Date: 2026-05-04

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "001"
down_revision = "000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "message_banners",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("impacted_service", sa.String(length=255), nullable=True),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("region", sa.String(length=255), nullable=True),
        sa.Column("source", sa.String(length=32), nullable=False),
        sa.Column("source_id", sa.String(length=255), nullable=True),
        sa.Column("source_url", sa.String(length=1024), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_message_banners_type"),
        "message_banners",
        ["type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_message_banners_expires_at"),
        "message_banners",
        ["expires_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_message_banners_region"),
        "message_banners",
        ["region"],
        unique=False,
    )
    op.create_index(
        op.f("ix_message_banners_source"),
        "message_banners",
        ["source"],
        unique=False,
    )
    op.create_index(
        op.f("ix_message_banners_source_id"),
        "message_banners",
        ["source_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_message_banners_source_id"), table_name="message_banners")
    op.drop_index(op.f("ix_message_banners_source"), table_name="message_banners")
    op.drop_index(op.f("ix_message_banners_region"), table_name="message_banners")
    op.drop_index(op.f("ix_message_banners_expires_at"), table_name="message_banners")
    op.drop_index(op.f("ix_message_banners_type"), table_name="message_banners")
    op.drop_table("message_banners")
