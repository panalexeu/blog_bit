"""empty message

Revision ID: 64faa661edcb
Revises: 6e4418195e97
Create Date: 2023-11-16 19:33:21.838221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64faa661edcb'
down_revision = '6e4418195e97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('like',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('like')
    # ### end Alembic commands ###
