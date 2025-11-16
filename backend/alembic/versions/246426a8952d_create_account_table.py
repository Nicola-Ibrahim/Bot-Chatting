"""create account table

Revision ID: 246426a8952d
Revises: 
Create Date: 2025-01-10 19:56:33.639505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '246426a8952d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the ``users`` table to persist user aggregates.  Columns
    # mirror those defined in ``src/database/models/user.py``.  The
    # ``id`` column is an auto-incrementing integer primary key,
    # ``uuid`` stores the domain identifier as a string, and
    # ``email`` is unique and indexed for fast lookup.  ``created_at``
    # and ``updated_at`` provide audit timestamps.
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            comment="Last update timestamp",
        ),
        sa.Column("uuid", sa.String(length=36), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=256), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.UniqueConstraint("uuid", name="uq_users_uuid"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    # Create indexes on uuid and email to align with the SQLAlchemy model
    op.create_index("ix_users_uuid", "users", ["uuid"], unique=True)
    op.create_index("ix_users_email", "users", ["email"], unique=True)


def downgrade() -> None:
    # Drop indexes and then the users table
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_uuid", table_name="users")
    op.drop_table("users")
