from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# Revision identifiers, used by Alembic.
revision = '82d253df819d'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Get the current database connection
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    # Check existing indexes in the 'admins' table
    existing_indexes_admins = [index['name'] for index in inspector.get_indexes('admins')]

    with op.batch_alter_table('admins', schema=None) as batch_op:
        # Check if columns already exist
        if 'deleted_at' not in [col['name'] for col in inspector.get_columns('admins')]:
            batch_op.add_column(sa.Column('deleted_at', sa.DateTime(), nullable=True))
        if 'dummy_field' not in [col['name'] for col in inspector.get_columns('admins')]:
            batch_op.add_column(sa.Column('dummy_field', sa.String(length=60), nullable=True))
        
        # Ensure 'id' column is set as primary key and has a unique constraint
        if 'id' not in [col['name'] for col in inspector.get_columns('admins')]:
            batch_op.add_column(sa.Column('id', sa.String(length=60), primary_key=True, nullable=False))
            batch_op.create_unique_constraint('uq_admins_id', ['id'])
        else:
            # Modify 'id' column to be primary key and add unique constraint if it exists but isn't defined as such
            batch_op.alter_column('id', existing_type=mysql.VARCHAR(length=60), primary_key=True, nullable=False)
            batch_op.create_unique_constraint('uq_admins_id', ['id'])

        if 'created_at' not in [col['name'] for col in inspector.get_columns('admins')]:
            batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
        if 'updated_at' not in [col['name'] for col in inspector.get_columns('admins')]:
            batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))
        
        # Alter columns
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=128),
               nullable=True)
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=128),
               type_=sa.String(length=256),
               existing_nullable=False)
        batch_op.alter_column('role',
               existing_type=mysql.TINYINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               existing_server_default=sa.text("'1'"))

        # Drop index if it exists
        if 'email' in existing_indexes_admins:
            batch_op.drop_index('email')

        # Drop foreign key constraint if it exists
        existing_foreign_keys = [fk['name'] for fk in inspector.get_foreign_keys('admins')]
        if 'admins_ibfk_1' in existing_foreign_keys:
            batch_op.drop_constraint('admins_ibfk_1', type_='foreignkey')

        # Drop column if it exists
        if 'admin_id' in [col['name'] for col in inspector.get_columns('admins')]:
            batch_op.drop_column('admin_id')

    # Check existing indexes in the 'employees' table
    existing_indexes_employees = [index['name'] for index in inspector.get_indexes('employees')]

    with op.batch_alter_table('employees', schema=None) as batch_op:
        if 'admin_id' not in [col['name'] for col in inspector.get_columns('employees')]:
            batch_op.add_column(sa.Column('admin_id', sa.String(length=60), nullable=True))
        if 'dummy_field' not in [col['name'] for col in inspector.get_columns('employees')]:
            batch_op.add_column(sa.Column('dummy_field', sa.String(length=50), nullable=True))
        
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=128),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.alter_column('salary',
               existing_type=mysql.VARCHAR(length=128),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.alter_column('role',
               existing_type=mysql.TINYINT(),
               type_=sa.Integer(),
               nullable=False,
               comment=None,
               existing_comment='0 -> Employee, 1 -> Admin',
               existing_server_default=sa.text("'0'"))
        batch_op.alter_column('created_at',
               existing_type=mysql.DATETIME(),
               nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
        batch_op.alter_column('updated_at',
               existing_type=mysql.DATETIME(),
               nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

        # Drop index if it exists
        if 'email' in existing_indexes_employees:
            batch_op.drop_index('email')

        # Create foreign key constraint
        batch_op.create_foreign_key(None, 'admins', ['admin_id'], ['id'])

    # Check existing columns in the 'settings' table
    existing_columns_settings = [col['name'] for col in inspector.get_columns('settings')]

    with op.batch_alter_table('settings', schema=None) as batch_op:
        if 'id' not in existing_columns_settings:
            batch_op.add_column(sa.Column('id', sa.String(length=60), nullable=False))
        if 'created_at' not in existing_columns_settings:
            batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
        if 'updated_at' not in existing_columns_settings:
            batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###

def downgrade():
    with op.batch_alter_table('settings', schema=None) as batch_op:
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('id')

    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_index('email', ['email'], unique=True)
        batch_op.alter_column('updated_at',
               existing_type=mysql.DATETIME(),
               nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
        batch_op.alter_column('created_at',
               existing_type=mysql.DATETIME(),
               nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
        batch_op.alter_column('role',
               existing_type=sa.Integer(),
               type_=mysql.TINYINT(),
               nullable=True,
               comment='0 -> Employee, 1 -> Admin',
               existing_server_default=sa.text("'0'"))
        batch_op.alter_column('salary',
               existing_type=sa.Integer(),
               type_=mysql.VARCHAR(length=128),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=128),
               existing_nullable=False)
        batch_op.drop_column('dummy_field')
        batch_op.drop_column('admin_id')

    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.drop_constraint('uq_admins_id', type_='unique')
        batch_op.create_index('email', ['email'], unique=True)
        batch_op.alter_column('role',
               existing_type=sa.Integer(),
               type_=mysql.TINYINT(),
               existing_nullable=False,
               existing_server_default=sa.text("'1'"))
        batch_op.alter_column('password',
               existing_type=sa.String(length=256),
               type_=mysql.VARCHAR(length=128),
               existing_nullable=False)
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('id')
        batch_op.drop_column('dummy_field')
        batch_op.drop_column('deleted_at')

    # ### end Alembic commands ###
