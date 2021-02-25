"""empty message

Revision ID: 8dc59538280c
Revises: 70390976b144
Create Date: 2020-09-05 09:34:09.016560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8dc59538280c'
down_revision = '70390976b144'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('college_covid',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('state', sa.String(length=255), nullable=True),
    sa.Column('county', sa.String(length=255), nullable=True),
    sa.Column('average_college_total_confirmed_count_cumsum', sa.Float(), nullable=True),
    sa.Column('average_college_medunit_confirmed_count_cumsum', sa.Float(), nullable=True),
    sa.Column('average_college_total_death_count_cumsum', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('county', 'state')
    )
    op.create_index('myindex_college_covid', 'college_covid', ['county', 'state'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('myindex_college_covid', table_name='college_covid')
    op.drop_table('college_covid')
    # ### end Alembic commands ###
