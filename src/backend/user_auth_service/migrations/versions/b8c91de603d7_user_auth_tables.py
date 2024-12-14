"""user_auth_tables

Revision ID: b8c91de603d7
Revises: 8ddfbda808c2
Create Date: 2024-12-14 14:42:37.422720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8c91de603d7'
down_revision: Union[str, None] = '8ddfbda808c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('token', sa.String(length=512), nullable=False),
    sa.Column('entity_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('legal_adress', sa.String(length=255), nullable=False),
    sa.Column('physical_adress', sa.String(length=255), nullable=False),
    sa.Column('phone_number', sa.String(length=50), nullable=True),
    sa.Column('user_role', sa.Enum('NotVerifyed', 'Verifyed', 'Admin', name='userroleenum'), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone_number')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('auth')
    # ### end Alembic commands ###
