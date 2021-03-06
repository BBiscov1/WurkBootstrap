"""changed around employee type

Revision ID: b2af451b982f
Revises: 6d101af56099
Create Date: 2020-05-23 08:57:29.770558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2af451b982f'
down_revision = '6d101af56099'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wurker')
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
    op.create_table('wurker',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('wid', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('fullname', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('bio', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='wurker_pkey'),
    sa.UniqueConstraint('wid', name='wurker_wid_key')
    )
    # ### end Alembic commands ###
