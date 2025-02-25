"""Add views column to listing

Revision ID: 1d6e3a35bb7c
Revises: 8aa2c9544a4a
Create Date: 2024-11-10 14:17:44.783303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d6e3a35bb7c'
down_revision = '8aa2c9544a4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('listing', schema=None) as batch_op:
        batch_op.add_column(sa.Column('views', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('listing', schema=None) as batch_op:
        batch_op.drop_column('views')

    # ### end Alembic commands ###
