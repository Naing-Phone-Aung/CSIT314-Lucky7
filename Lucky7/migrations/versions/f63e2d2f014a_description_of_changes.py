"""Description of changes

Revision ID: f63e2d2f014a
Revises: e0c6bdf91c0c
Create Date: 2024-11-13 22:55:15.395039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f63e2d2f014a'
down_revision = 'e0c6bdf91c0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('listing',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('image_url', sa.String(length=255), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('model', sa.String(length=50), nullable=False),
    sa.Column('color', sa.String(length=30), nullable=False),
    sa.Column('mileage', sa.Integer(), nullable=False),
    sa.Column('steering_type', sa.Enum('Automatic', 'Manual', name='steering_type_enum'), nullable=False),
    sa.Column('steering_position', sa.Enum('Left', 'Right', name='steering_position_enum'), nullable=False),
    sa.Column('fuel_type', sa.Enum('Diesel', 'Petrol', 'Electric', name='fuel_type_enum'), nullable=False),
    sa.Column('horsepower', sa.Integer(), nullable=False),
    sa.Column('previous_owners', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('seller_id', sa.Integer(), nullable=False),
    sa.Column('agent_id', sa.Integer(), nullable=False),
    sa.Column('buyer_id', sa.Integer(), nullable=True),
    sa.Column('views', sa.Integer(), nullable=True),
    sa.Column('favs', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['user_account.id'], ),
    sa.ForeignKeyConstraint(['buyer_id'], ['user_account.id'], ),
    sa.ForeignKeyConstraint(['seller_id'], ['user_account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('star_rating', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('agent_id', sa.Integer(), nullable=False),
    sa.Column('seller_id', sa.Integer(), nullable=True),
    sa.Column('buyer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['user_account.id'], ),
    sa.ForeignKeyConstraint(['buyer_id'], ['user_account.id'], ),
    sa.ForeignKeyConstraint(['seller_id'], ['user_account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favourites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('listing_id', sa.Integer(), nullable=False),
    sa.Column('buyer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['buyer_id'], ['user_account.id'], ),
    sa.ForeignKeyConstraint(['listing_id'], ['listing.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favourites')
    op.drop_table('review')
    op.drop_table('listing')
    # ### end Alembic commands ###
