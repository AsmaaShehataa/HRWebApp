"""adding a soft delete col to the database

Revision ID: 001ad7426828
Revises: 
Create Date: 2024-08-12 03:14:55.655616

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '001ad7426828'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted_at', sa.DateTime(), nullable=True))
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=150),
               type_=sa.String(length=128),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=150),
               type_=sa.String(length=128),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=250),
               type_=sa.String(length=128),
               existing_nullable=False)
        batch_op.alter_column('phone',
               existing_type=mysql.VARCHAR(length=250),
               type_=sa.String(length=128),
               existing_nullable=False)
        batch_op.alter_column('department',
               existing_type=mysql.VARCHAR(length=250),
               type_=sa.String(length=128),
               existing_nullable=False)
        batch_op.alter_column('salary',
               existing_type=mysql.VARCHAR(length=250),
               type_=sa.String(length=128),
               existing_nullable=False)
        batch_op.alter_column('role',
               existing_type=mysql.TINYINT(),
               type_=sa.Integer(),
               nullable=False,
               comment=None,
               existing_comment='0 -> User, 1 -> Admin',
               existing_server_default=sa.text("'0'"))
        batch_op.alter_column('id',
               existing_type=mysql.VARCHAR(length=150),
               type_=sa.String(length=60),
               existing_nullable=False)
        batch_op.drop_index('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index('email', ['email'], unique=True)
        batch_op.alter_column('id',
               existing_type=sa.String(length=60),
               type_=mysql.VARCHAR(length=150),
               existing_nullable=False)
        batch_op.alter_column('role',
               existing_type=sa.Integer(),
               type_=mysql.TINYINT(),
               nullable=True,
               comment='0 -> User, 1 -> Admin',
               existing_server_default=sa.text("'0'"))
        batch_op.alter_column('salary',
               existing_type=sa.String(length=128),
               type_=mysql.VARCHAR(length=250),
               existing_nullable=False)
        batch_op.alter_column('department',
               existing_type=sa.String(length=128),
               type_=mysql.VARCHAR(length=250),
               existing_nullable=False)
        batch_op.alter_column('phone',
               existing_type=sa.String(length=128),
               type_=mysql.VARCHAR(length=250),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.String(length=128),
               type_=mysql.VARCHAR(length=250),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=128),
               type_=mysql.VARCHAR(length=150),
               existing_nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.String(length=128),
               type_=mysql.VARCHAR(length=150),
               existing_nullable=False)
        batch_op.drop_column('deleted_at')

    # ### end Alembic commands ###
