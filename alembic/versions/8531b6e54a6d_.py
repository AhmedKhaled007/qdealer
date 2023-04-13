"""empty message

Revision ID: 8531b6e54a6d
Revises: ca53a9a0912a
Create Date: 2023-04-06 00:12:12.035973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8531b6e54a6d'
down_revision = 'ca53a9a0912a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('img_path', sa.String(), nullable=False),
    sa.Column('car_ad_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_ad_id'], ['car_ads.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_images_id'), 'images', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_images_id'), table_name='images')
    op.drop_table('images')
    # ### end Alembic commands ###