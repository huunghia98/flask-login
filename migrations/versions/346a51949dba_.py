"""empty message

Revision ID: 346a51949dba
Revises: 8f26c391f4cc
Create Date: 2019-08-07 15:31:55.744470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '346a51949dba'
down_revision = '8f26c391f4cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('expire_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blacklist')
    # ### end Alembic commands ###