"""create post table

Revision ID: cf72cfc834f2
Revises:
Create Date: 2023-04-03 21:46:59.532463

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'cf72cfc834f2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create the posts table
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("published",
                  sa.Boolean,
                  nullable=False,
                  server_default=sa.false()),
        sa.Column("updated_at",
                  sa.TIMESTAMP,
                  nullable=False,
                  server_default=sa.func.now(),
                  onupdate=sa.func.now()),
        sa.Column("created_at",
                  sa.TIMESTAMP,
                  nullable=False,
                  server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("posts")
