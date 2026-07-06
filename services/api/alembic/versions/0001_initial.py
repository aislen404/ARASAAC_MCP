"""Initial schema for materials and audit events."""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001_initial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        "materials",
        sa.Column("material_id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        if_not_exists=True,
    )
    op.create_index(
        "ix_materials_created_at",
        "materials",
        ["created_at"],
        if_not_exists=True,
    )
    op.create_table(
        "audit_events",
        sa.Column("event_id", sa.String(length=36), primary_key=True),
        sa.Column("material_id", sa.String(length=36), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        if_not_exists=True,
    )
    op.create_index(
        "ix_audit_events_material_id",
        "audit_events",
        ["material_id"],
        if_not_exists=True,
    )
    op.create_index(
        "ix_audit_events_occurred_at",
        "audit_events",
        ["occurred_at"],
        if_not_exists=True,
    )
    op.create_table(
        "pictogram_embeddings",
        sa.Column("pictogram_id", sa.Integer(), primary_key=True),
        sa.Column("label", sa.String(length=120), nullable=False),
        sa.Column("pictogram_metadata", sa.JSON(), nullable=False),
        sa.Column("embedding", sa.String(), nullable=True),
        if_not_exists=True,
    )


def downgrade() -> None:
    op.drop_table("pictogram_embeddings")
    op.drop_index("ix_audit_events_occurred_at", table_name="audit_events")
    op.drop_index("ix_audit_events_material_id", table_name="audit_events")
    op.drop_table("audit_events")
    op.drop_index("ix_materials_created_at", table_name="materials")
    op.drop_table("materials")
