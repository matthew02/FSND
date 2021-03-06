"""empty message

Revision ID: 521baddb6e4a
Revises: 866398209fef
Create Date: 2020-05-30 06:02:33.034631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '521baddb6e4a'
down_revision = '866398209fef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('show_artist_id_fkey', 'show', type_='foreignkey')
    op.drop_constraint('show_venue_id_fkey', 'show', type_='foreignkey')
    op.create_foreign_key(None, 'show', 'artist', ['artist_id'], ['id'], ondelete='cascade')
    op.create_foreign_key(None, 'show', 'venue', ['venue_id'], ['id'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'show', type_='foreignkey')
    op.drop_constraint(None, 'show', type_='foreignkey')
    op.create_foreign_key('show_venue_id_fkey', 'show', 'venue', ['venue_id'], ['id'])
    op.create_foreign_key('show_artist_id_fkey', 'show', 'artist', ['artist_id'], ['id'])
    # ### end Alembic commands ###
