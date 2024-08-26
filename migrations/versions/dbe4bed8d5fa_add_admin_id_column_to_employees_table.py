"""Add admin_id column to employees table

Revision ID: dbe4bed8d5fa
Revises: 1f3fed5ee87f
Create Date: 2024-08-26 03:01:43.731876

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'dbe4bed8d5fa'
down_revision = '1f3fed5ee87f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.drop_constraint('admins_ibfk_1', type_='foreignkey')
        batch_op.drop_column('admin_id')

    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.add_column(sa.Column('admin_id', sa.String(length=60), nullable=False))
        batch_op.create_foreign_key(None, 'admins', ['admin_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('admin_id')

    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.add_column(sa.Column('admin_id', mysql.VARCHAR(length=60), nullable=False))
        batch_op.create_foreign_key('admins_ibfk_1', 'employees', ['admin_id'], ['id'])

    # ### end Alembic commands ###
