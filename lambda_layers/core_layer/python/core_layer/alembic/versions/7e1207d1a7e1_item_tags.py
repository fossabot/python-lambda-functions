"""item_tags

Revision ID: 7e1207d1a7e1
Revises: 512ef0aa3fbd
Create Date: 2020-12-29 16:30:14.149037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e1207d1a7e1'
down_revision = '512ef0aa3fbd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('tag', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_tags',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('item_id', sa.String(length=36), nullable=True),
    sa.Column('tag_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('item_tags')
    op.drop_table('tags')
    # ### end Alembic commands ###
