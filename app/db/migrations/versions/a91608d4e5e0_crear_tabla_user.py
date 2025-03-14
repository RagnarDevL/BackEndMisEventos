"""Crear tabla user

Revision ID: a91608d4e5e0
Revises: c8e29ada2802
Create Date: 2025-03-11 14:28:42.218631

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a91608d4e5e0'
down_revision: Union[str, None] = 'c8e29ada2802'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('token', sa.String(length=255), nullable=True)  # Puedes agregar el token aquí si lo deseas
    )
    pass

def downgrade():
    op.drop_table('users')
    pass
