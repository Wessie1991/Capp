"""empty message

Revision ID: 5fa14b63f511
Revises: 
Create Date: 2018-04-13 17:34:23.747131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fa14b63f511'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chats', sa.Column('see_flag', sa.String(length=4), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chats', 'see_flag')
    # ### end Alembic commands ###
