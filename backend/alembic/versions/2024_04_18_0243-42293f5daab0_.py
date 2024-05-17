"""empty message

Revision ID: 42293f5daab0
Revises: 017a399f6696
Create Date: 2024-04-18 02:43:47.116719

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "42293f5daab0"
down_revision: Union[str, None] = "017a399f6696"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_users_username", table_name="users")
    op.create_index(
        op.f("ix_users_username"), "users", ["username"], unique=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.create_index("ix_users_username", "users", ["username"], unique=False)
    # ### end Alembic commands ###