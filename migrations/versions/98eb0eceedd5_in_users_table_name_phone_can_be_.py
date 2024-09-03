"""in Users table name, phone can be nulluble

Revision ID: 98eb0eceedd5
Revises: 6434f6a13b11
Create Date: 2024-08-29 03:58:07.254766

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '98eb0eceedd5'
down_revision = '6434f6a13b11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=128),
               nullable=True)
        batch_op.drop_constraint('users_ibfk_1', type_='foreignkey')
        batch_op.drop_column('role_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role_id', mysql.VARCHAR(length=128), nullable=False))
        batch_op.create_foreign_key('users_ibfk_1', 'roles', ['role_id'], ['id'])
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)

    # ### end Alembic commands ###
