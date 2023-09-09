"""Nullable location.

Revision ID: e3eefd8da820
Revises: 06f358d1aec7
Create Date: 2023-09-02 22:38:32.450313
"""
from typing import Sequence, Union

import geoalchemy2
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e3eefd8da820'
down_revision: Union[str, None] = '06f358d1aec7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Adjusted
    op.alter_column(
        'photos',
        'location',
        existing_type=geoalchemy2.types.Geography(
            geometry_type='POINT',
            srid=4326,
            from_text='ST_GeogFromText',
            name='geography',
            nullable=False,
        ),
        type_=geoalchemy2.types.Geography(
            geometry_type='POINT',
            srid=4326,
            from_text='ST_GeogFromText',
            name='geography',
        ),
        nullable=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Adjusted
    op.alter_column(
        'photos',
        'location',
        existing_type=geoalchemy2.types.Geography(
            from_text='ST_GeogFromText',
            name='geography',
            geometry_type='POINT',
            srid=4326,
        ),
        type_=geoalchemy2.types.Geography(
            geometry_type='POINT',
            srid=4326,
            from_text='ST_GeogFromText',
            name='geography',
            nullable=False,
        ),
        nullable=False,
    )
    # ### end Alembic commands ###