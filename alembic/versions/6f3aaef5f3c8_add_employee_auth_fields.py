"""add employee authentication fields

Revision ID: 6f3aaef5f3c8
Revises: f3417eaaacd1
Create Date: 2026-08-08 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6f3aaef5f3c8"
down_revision: Union[str, Sequence[str], None] = "f3417eaaacd1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("employees", sa.Column("username", sa.String(length=100), nullable=True))
    op.add_column("employees", sa.Column("password_hash", sa.String(length=255), nullable=True))
    op.add_column("employees", sa.Column("is_active", sa.Boolean(), nullable=True, server_default=sa.true()))
    op.add_column("employees", sa.Column("role", sa.String(length=20), nullable=True, server_default="EMPLOYEE"))

    op.create_unique_constraint("uq_employees_username", "employees", ["username"])

    op.execute(
        "UPDATE employees SET username = CONCAT('employee', id) WHERE username IS NULL"
    )
    op.execute(
        "UPDATE employees SET password_hash = 'todo' WHERE password_hash IS NULL"
    )

    op.alter_column("employees", "username", nullable=False)
    op.alter_column("employees", "password_hash", nullable=False)
    op.alter_column("employees", "is_active", server_default=None)
    op.alter_column("employees", "role", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_employees_username", "employees", type_="unique")
    op.drop_column("employees", "role")
    op.drop_column("employees", "is_active")
    op.drop_column("employees", "password_hash")
    op.drop_column("employees", "username")
