"""empty message

Revision ID: 2eed958cbca3
Revises: 8dc59538280c
Create Date: 2021-03-02 18:04:49.735560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2eed958cbca3'
down_revision = '8dc59538280c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tweet_table_1',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tweet_id', sa.String(length=255), nullable=True),
    sa.Column('place_name', sa.String(length=255), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('text', sa.String(length=300), nullable=True),
    sa.Column('hate_prob', sa.Float(), nullable=True),
    sa.Column('counterhate_prob', sa.Float(), nullable=True),
    sa.Column('neutral_prob', sa.Float(), nullable=True),
    sa.Column('other_prob', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tweet_table_1')
    # ### end Alembic commands ###