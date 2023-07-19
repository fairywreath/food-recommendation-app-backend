"""Initial migration

Revision ID: 7886fa957817
Revises: 2c7f09d82992
Create Date: 2023-07-19 01:50:18.303240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7886fa957817'
down_revision = '2c7f09d82992'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('restaurant',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('website', sa.String(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('dietary_preferences', sa.ARRAY(sa.Enum('VEGAN', 'VEGETARIAN', 'PESCETARIAN', 'GLUTEN_FREE', 'DAIRY_FREE', 'NUT_FREE', 'HALAL', name='dietary_preferences_enum'), dimensions=1), nullable=True),
    sa.Column('cuisine_genres', sa.ARRAY(sa.Enum('THAI', 'VIETNAMESE', 'SOUTHEAST_ASIAN', 'KOREAN', 'CHINESE', 'JAPANESE', 'INDIAN', 'ITALIAN', 'FRENCH', 'AMERICAN', 'MEXICAN', 'SOUTH_AMERICAN', 'MIDDLE_EASTERN', 'MEDITERRANEAN', name='cuisine_genres_enum'), dimensions=1), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('dietary_preferences', sa.ARRAY(sa.Enum('VEGAN', 'VEGETARIAN', 'PESCETARIAN', 'GLUTEN_FREE', 'DAIRY_FREE', 'NUT_FREE', 'HALAL', name='dietary_preferences_enum'), dimensions=1), nullable=True),
    sa.Column('cuisine_genres', sa.ARRAY(sa.Enum('THAI', 'VIETNAMESE', 'SOUTHEAST_ASIAN', 'KOREAN', 'CHINESE', 'JAPANESE', 'INDIAN', 'ITALIAN', 'FRENCH', 'AMERICAN', 'MEXICAN', 'SOUTH_AMERICAN', 'MIDDLE_EASTERN', 'MEDITERRANEAN', name='cuisine_genres_enum'), dimensions=1), nullable=True),
    sa.Column('spending_budgets', sa.ARRAY(sa.Enum('VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH', name='spending_budget_enum'), dimensions=1), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('favorite_restaurants',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('user_restaurant_rating',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('users_following',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_following')
    op.drop_table('user_restaurant_rating')
    op.drop_table('favorite_restaurants')
    op.drop_table('user')
    op.drop_table('restaurant')
    # ### end Alembic commands ###