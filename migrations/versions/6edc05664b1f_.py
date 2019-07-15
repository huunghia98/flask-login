"""empty message

Revision ID: 6edc05664b1f
Revises: 060bceb542c4
Create Date: 2019-07-14 10:05:22.943431

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6edc05664b1f'
down_revision = '060bceb542c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('email', table_name='signup_users')
    op.drop_index('username', table_name='signup_users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('username', 'signup_users', ['username'], unique=True)
    op.create_index('email', 'signup_users', ['email'], unique=True)
    # ### end Alembic commands ###
