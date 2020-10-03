"""Initial revision

Revision ID: cedce8eb10ad
Revises: 
Create Date: 2020-10-02 14:16:12.605509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cedce8eb10ad'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('claimants',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('claimant', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('entities',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('entity', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('factchecking_organizations',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('counter_trustworthy', sa.Integer(), nullable=True),
    sa.Column('counter_not_trustworthy', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('items',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('language', sa.String(length=2), nullable=True),
    sa.Column('status', sa.String(length=36), nullable=True),
    sa.Column('variance', sa.Float(), nullable=True),
    sa.Column('result_score', sa.Float(), nullable=True),
    sa.Column('open_reviews', sa.Integer(), nullable=True),
    sa.Column('open_reviews_level_1', sa.Integer(), nullable=True),
    sa.Column('open_reviews_level_2', sa.Integer(), nullable=True),
    sa.Column('in_progress_reviews_level_1', sa.Integer(), nullable=True),
    sa.Column('in_progress_reviews_level_2', sa.Integer(), nullable=True),
    sa.Column('open_timestamp', sa.DateTime(), nullable=True),
    sa.Column('close_timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('keyphrases',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('phrase', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('levels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=True),
    sa.Column('required_experience_points', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('review_questions',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('mandatory', sa.Boolean(), nullable=True),
    sa.Column('info', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sentiments',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('sentiment', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('factchecks',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=1000), nullable=True),
    sa.Column('url', sa.String(length=1000), nullable=True),
    sa.Column('factchecking_organization_id', sa.String(length=36), nullable=True),
    sa.Column('item_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['factchecking_organization_id'], ['factchecking_organizations.id'], ),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_entities',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('item_id', sa.String(length=36), nullable=True),
    sa.Column('entity_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['entity_id'], ['entities.id'], ),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_keyphrases',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('item_id', sa.String(length=36), nullable=True),
    sa.Column('keyphrase_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['keyphrase_id'], ['keyphrases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_sentiments',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('item_id', sa.String(length=36), nullable=True),
    sa.Column('sentiment_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['sentiment_id'], ['sentiments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('submissions',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('submission_date', sa.DateTime(), nullable=True),
    sa.Column('mail', sa.String(length=100), nullable=True),
    sa.Column('telegram_id', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=36), nullable=True),
    sa.Column('source', sa.String(length=100), nullable=True),
    sa.Column('frequency', sa.String(length=100), nullable=True),
    sa.Column('received_date', sa.DateTime(), nullable=True),
    sa.Column('item_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('urls',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('url', sa.String(length=200), nullable=True),
    sa.Column('claimant_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['claimant_id'], ['claimants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('experience_points', sa.Integer(), nullable=True),
    sa.Column('level_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['level_id'], ['levels.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_urls',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('item_id', sa.String(length=36), nullable=True),
    sa.Column('url_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['url_id'], ['urls.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('is_peer_review', sa.Boolean(), nullable=True),
    sa.Column('peer_review_id', sa.String(length=36), nullable=True),
    sa.Column('belongs_to_good_pair', sa.Boolean(), nullable=True),
    sa.Column('item_id', sa.String(length=36), nullable=True),
    sa.Column('user_id', sa.String(length=36), nullable=True),
    sa.Column('start_timestamp', sa.DateTime(), nullable=True),
    sa.Column('finish_timestamp', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews_in_progress',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('item_id', sa.String(length=36), nullable=True),
    sa.Column('user_id', sa.String(length=36), nullable=True),
    sa.Column('start_timestamp', sa.DateTime(), nullable=True),
    sa.Column('is_peer_review', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('review_answers',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('review_id', sa.String(length=36), nullable=True),
    sa.Column('review_question_id', sa.String(length=36), nullable=True),
    sa.Column('answer', sa.Integer(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['review_id'], ['reviews.id'], ),
    sa.ForeignKeyConstraint(['review_question_id'], ['review_questions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('review_answers')
    op.drop_table('reviews_in_progress')
    op.drop_table('reviews')
    op.drop_table('item_urls')
    op.drop_table('users')
    op.drop_table('urls')
    op.drop_table('submissions')
    op.drop_table('item_sentiments')
    op.drop_table('item_keyphrases')
    op.drop_table('item_entities')
    op.drop_table('factchecks')
    op.drop_table('sentiments')
    op.drop_table('review_questions')
    op.drop_table('levels')
    op.drop_table('keyphrases')
    op.drop_table('items')
    op.drop_table('factchecking_organizations')
    op.drop_table('entities')
    op.drop_table('claimants')
    # ### end Alembic commands ###
