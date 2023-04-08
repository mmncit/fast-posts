"""create user table

Revision ID: a6ea37ffc009
Revises: cf72cfc834f2
Create Date: 2023-04-03 22:46:41.630737

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'a6ea37ffc009'
down_revision = 'cf72cfc834f2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users", sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("created_at",
                  sa.TIMESTAMP(),
                  nullable=False,
                  server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"))


def downgrade() -> None:
    op.drop_table("users")
