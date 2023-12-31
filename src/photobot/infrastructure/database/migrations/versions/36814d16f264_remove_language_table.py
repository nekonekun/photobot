"""Remove language table.

Revision ID: 36814d16f264
Revises: 973f798e8331
Create Date: 2023-09-02 23:12:27.315002
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '36814d16f264'
down_revision: Union[str, None] = '973f798e8331'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Adjusted
    op.drop_constraint('users_language_code_fkey', 'users', type_='foreignkey')
    op.drop_table('languages')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Adjusted
    op.create_foreign_key(
        'users_language_code_fkey',
        'users',
        'languages',
        ['language_code'],
        ['code'],
    )
    op.create_table(
        'languages',
        sa.Column(
            'code',
            sa.VARCHAR(length=2),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint('code', name='pk__languages'),
    )
    # ### end Alembic commands ###
