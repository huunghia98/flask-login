"""empty message

Revision ID: b2e03efa134c
Revises: 346a51949dba
Create Date: 2019-08-07 15:40:31.429496

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b2e03efa134c'
down_revision = '346a51949dba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blacklist', sa.Column('status', sa.Enum('active', 'ban', 'lock_in_time', name='status'), nullable=True))
    op.drop_column('users', 'status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('status', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('blacklist', 'status')
    # ### end Alembic commands ###
