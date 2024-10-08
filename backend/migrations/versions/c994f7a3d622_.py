"""empty message

Revision ID: c994f7a3d622
Revises: 7ec49afe420f
Create Date: 2023-06-25 21:03:37.432459

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c994f7a3d622"
down_revision = "c37ea1a80143"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("message", sa.Column("is_read", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("message", "is_read")
    # ### end Alembic commands ###
