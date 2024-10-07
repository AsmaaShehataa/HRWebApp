"""Initial migration with leave requests and relationships

Revision ID: eebfd44fd229
Revises: 
Create Date: 2024-10-06 05:17:19.446536

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'eebfd44fd229'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create the 'leave_requests' table
    op.create_table(
        'leave_requests',
        sa.Column('id', sa.String(length=60), nullable=False),
        sa.Column('employee_id', sa.String(length=60), sa.ForeignKey('employees.id'), nullable=False),
        sa.Column('start_date', sa.DateTime, nullable=False),
        sa.Column('end_date', sa.DateTime, nullable=False),
        sa.Column('leave_type', sa.String(length=60), nullable=False),
        sa.Column('status', sa.Integer, default=0, nullable=False),
        sa.Column('leave_days', sa.String(length=255), nullable=False),
        sa.Column('approved_by', sa.String(length=60), sa.ForeignKey('employees.id'), nullable=True),
        sa.Column('reason', sa.String(length=1000), nullable=True),
        sa.Column("deleted_at", sa.DateTime, nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # Reverse the changes made in the upgrade step
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_column('head_employee_id')
