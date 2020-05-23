"""empty message

Revision ID: cde06f895469
Revises: b2af451b982f
Create Date: 2020-05-23 08:59:39.113159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cde06f895469'
down_revision = 'b2af451b982f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('post_wid_fkey', 'post', type_='foreignkey')
    op.drop_column('post', 'wid')
    op.add_column('user', sa.Column('bio', sa.String(length=500), nullable=True))
    op.add_column('user', sa.Column('isemployee', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'isemployee')
    op.drop_column('user', 'bio')
    op.add_column('post', sa.Column('wid', sa.VARCHAR(length=10), autoincrement=False, nullable=True))
    op.create_foreign_key('post_wid_fkey', 'post', 'wurker', ['wid'], ['wid'])
    # ### end Alembic commands ###