"""empty message

Revision ID: 6cede65d808c
Revises: b0d96b84a3eb
Create Date: 2022-11-30 11:16:40.768401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cede65d808c'
down_revision = 'b0d96b84a3eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_task_name', table_name='task')
    op.drop_table('task')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('description', sa.VARCHAR(length=128), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('complete', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_task_name', 'task', ['name'], unique=False)
    # ### end Alembic commands ###