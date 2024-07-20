"""Initial Migration

Revision ID: 9353b99b95dc
Revises: 
Create Date: 2024-07-20 15:51:29.890009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9353b99b95dc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_email', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('phone_number', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('service_policy_agreement', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('privacy_policy_agreement', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('third_party_information_agreement', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('nickname', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('social_provider', postgresql.ENUM('naver', name='socialprovider'), autoincrement=False, nullable=False),
    sa.Column('joined_datetime', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    op.create_index('ix_user_email', 'user', ['email'], unique=True)
    # ### end Alembic commands ###
