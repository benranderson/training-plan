"""empty message

Revision ID: 0e41e78563c4
Revises: e4e46dd976a5
Create Date: 2017-09-08 13:23:34.216570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e41e78563c4'
down_revision = 'e4e46dd976a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles')
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'role_id')
    op.drop_column('workout', 'color')
    op.drop_column('workout', 'textColor')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workout', sa.Column('textColor', sa.VARCHAR(), nullable=True))
    op.add_column('workout', sa.Column('color', sa.VARCHAR(), nullable=True))
    op.add_column('users', sa.Column('role_id', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'users', 'roles', ['role_id'], ['id'])
    op.create_table('roles',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###