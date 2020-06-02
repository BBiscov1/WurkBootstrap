"""empty message

Revision ID: cf7fff675773
Revises: 6a26432baef6
Create Date: 2020-05-30 09:28:41.814118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf7fff675773'
down_revision = '6a26432baef6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('booking', 'claimedby')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('booking', sa.Column('claimedby', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###