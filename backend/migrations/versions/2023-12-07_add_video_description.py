"""add_video_description

Revision ID: b68e36783f13
Revises: bc59144df905
Create Date: 2023-12-07 17:41:45.742110

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b68e36783f13"
down_revision = "bc59144df905"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("video", sa.Column("description", sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("video", "description")
    # ### end Alembic commands ###
