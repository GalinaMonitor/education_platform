"""add_get_welcome_message

Revision ID: bc59144df905
Revises: 8310e731138e
Create Date: 2023-08-31 17:39:59.026378

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "bc59144df905"
down_revision = "8310e731138e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("chat", sa.Column("get_welcome_message", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("chat", "get_welcome_message")
    # ### end Alembic commands ###
