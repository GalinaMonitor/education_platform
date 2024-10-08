"""empty message

Revision ID: 2b3ab9780760
Revises: c994f7a3d622
Create Date: 2023-07-14 18:18:13.174412

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2b3ab9780760"
down_revision = "c994f7a3d622"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("is_admin", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "is_admin")
    # ### end Alembic commands ###
