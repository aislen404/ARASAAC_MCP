"""Add workspaces and workspace scoping to materials and audit events."""

from collections.abc import Sequence
from datetime import UTC, datetime
import json
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

revision: str = "0002_workspaces"
down_revision: str | None = "0001_initial"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "workspaces",
        sa.Column("workspace_id", sa.String(length=36), primary_key=True),
        sa.Column("slug", sa.String(length=120), nullable=False, unique=True),
        sa.Column("display_name", sa.String(length=120), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        if_not_exists=True,
    )
    op.create_index("ix_workspaces_slug", "workspaces", ["slug"], if_not_exists=True)

    with op.batch_alter_table("materials") as batch:
        batch.add_column(sa.Column("workspace_id", sa.String(length=36), nullable=True))
        batch.add_column(sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))
        batch.add_column(sa.Column("status", sa.String(length=32), nullable=True))
    with op.batch_alter_table("audit_events") as batch:
        batch.add_column(sa.Column("workspace_id", sa.String(length=36), nullable=True))

    connection = op.get_bind()
    legacy_workspace_id = str(uuid4())
    timestamp = datetime.now(UTC)
    legacy_slug = f"legacy-{timestamp.strftime('%Y%m%d%H%M%S')}"
    legacy_payload = {
        "workspace_id": legacy_workspace_id,
        "slug": legacy_slug,
        "display_name": None,
        "created_at": timestamp.isoformat(),
        "updated_at": timestamp.isoformat(),
    }
    connection.execute(
        sa.text(
            "INSERT INTO workspaces (workspace_id, slug, display_name, created_at, updated_at, payload) VALUES (:workspace_id, :slug, :display_name, :created_at, :updated_at, :payload)"
        ),
        {
            "workspace_id": legacy_workspace_id,
            "slug": legacy_slug,
            "display_name": None,
            "created_at": timestamp,
            "updated_at": timestamp,
            "payload": json.dumps(legacy_payload),
        },
    )
    connection.execute(
        sa.text("UPDATE materials SET workspace_id = :workspace_id WHERE workspace_id IS NULL"),
        {"workspace_id": legacy_workspace_id},
    )
    connection.execute(
        sa.text(
            "UPDATE materials SET updated_at = created_at WHERE updated_at IS NULL"
        )
    )
    material_rows = connection.execute(sa.text("SELECT material_id, payload FROM materials")).mappings()
    for row in material_rows:
        payload = row["payload"] or {}
        if isinstance(payload, str):
            payload = json.loads(payload)
        status = payload.get("status", "draft")
        connection.execute(
            sa.text("UPDATE materials SET status = :status WHERE material_id = :material_id"),
            {"status": status, "material_id": row["material_id"]},
        )
    connection.execute(
        sa.text("UPDATE audit_events SET workspace_id = :workspace_id WHERE workspace_id IS NULL"),
        {"workspace_id": legacy_workspace_id},
    )

    with op.batch_alter_table("materials") as batch:
        batch.alter_column("workspace_id", nullable=False)
        batch.alter_column("updated_at", nullable=False)
        batch.alter_column("status", nullable=False)
        batch.create_foreign_key(
            "fk_materials_workspace_id",
            "workspaces",
            ["workspace_id"],
            ["workspace_id"],
        )
        batch.create_index("ix_materials_workspace_status", ["workspace_id", "status"], unique=False)
        batch.create_index("ix_materials_workspace_updated", ["workspace_id", "updated_at"], unique=False)
    with op.batch_alter_table("audit_events") as batch:
        batch.alter_column("workspace_id", nullable=False)
        batch.create_foreign_key(
            "fk_audit_events_workspace_id",
            "workspaces",
            ["workspace_id"],
            ["workspace_id"],
        )
        batch.create_index("ix_audit_events_workspace_created", ["workspace_id", "occurred_at"], unique=False)


def downgrade() -> None:
    with op.batch_alter_table("audit_events") as batch:
        batch.drop_index("ix_audit_events_workspace_created")
        batch.drop_constraint("fk_audit_events_workspace_id", type_="foreignkey")
        batch.drop_column("workspace_id")
    with op.batch_alter_table("materials") as batch:
        batch.drop_index("ix_materials_workspace_updated")
        batch.drop_index("ix_materials_workspace_status")
        batch.drop_constraint("fk_materials_workspace_id", type_="foreignkey")
        batch.drop_column("status")
        batch.drop_column("updated_at")
        batch.drop_column("workspace_id")
    op.drop_index("ix_workspaces_slug", table_name="workspaces")
    op.drop_table("workspaces")