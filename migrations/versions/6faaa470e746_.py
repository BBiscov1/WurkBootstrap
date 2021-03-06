"""empty message

Revision ID: 6faaa470e746
Revises: 58fe57bc7b7f
Create Date: 2020-05-12 17:12:36.637241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6faaa470e746'
down_revision = '58fe57bc7b7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client', sa.Column('address', sa.String(length=128), nullable=True))
    op.add_column('client', sa.Column('bookingid', sa.String(length=6), nullable=True))
    op.add_column('client', sa.Column('city', sa.String(length=128), nullable=True))
    op.add_column('client', sa.Column('state', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('client', 'state')
    op.drop_column('client', 'city')
    op.drop_column('client', 'bookingid')
    op.drop_column('client', 'address')
    # ### end Alembic commands ###
