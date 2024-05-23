"""empty message

Revision ID: 703aeee2673a
Revises: 16b4430750c0
Create Date: 2024-05-22 19:51:09.699695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '703aeee2673a'
down_revision = '16b4430750c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.add_column(sa.Column('teste', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.drop_column('teste')

    # ### end Alembic commands ###
