"""Agregar campo token a User

Revision ID: c8e29ada2802
Revises: 
Create Date: 2025-03-11 14:22:09.559719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8e29ada2802'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Agregar el campo 'token' a la tabla 'User '
    op.add_column('user', sa.Column('token', sa.String(length=255), nullable=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
