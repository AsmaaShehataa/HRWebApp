"""adding attendance table to the db

Revision ID: 7e0b0dd59e3c
Revises: 82d253df819d
Create Date: 2024-09-26 01:42:21.176088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e0b0dd59e3c'
down_revision = '82d253df819d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attendance',
    sa.Column('employee_id', sa.String(length=60), nullable=False),
    sa.Column('check_in', sa.DateTime(), nullable=False),
    sa.Column('check_out', sa.DateTime(), nullable=True),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('admins', schema=None) as batch_op:
        pass  # Add your batch operations here

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.create_index('uq_admins_id', ['id'], unique=True)

    op.drop_table('attendance')
    # ### end Alembic commands ###
