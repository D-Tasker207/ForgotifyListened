"""empty message

Revision ID: 9e0f45310659
Revises: 
Create Date: 2022-11-15 20:36:42.667594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e0f45310659'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artist',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('rec_count', sa.Integer(), nullable=True),
    sa.Column('img', sa.String(length=100), nullable=True),
    sa.Column('external_url', sa.String(length=64), nullable=True),
    sa.Column('uri', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_artist_name'), 'artist', ['name'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('last_pulled', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=False)
    op.create_table('album',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('rec_count', sa.Integer(), nullable=True),
    sa.Column('img', sa.String(length=100), nullable=True),
    sa.Column('external_url', sa.String(length=64), nullable=True),
    sa.Column('uri', sa.String(length=64), nullable=True),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_album_name'), 'album', ['name'], unique=False)
    op.create_table('user_to_artist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.Column('forgotten', sa.Integer(), nullable=True),
    sa.Column('long_term', sa.Integer(), nullable=True),
    sa.Column('med_term', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_to_artist_artist_id'), 'user_to_artist', ['artist_id'], unique=False)
    op.create_index(op.f('ix_user_to_artist_forgotten'), 'user_to_artist', ['forgotten'], unique=False)
    op.create_index(op.f('ix_user_to_artist_long_term'), 'user_to_artist', ['long_term'], unique=False)
    op.create_index(op.f('ix_user_to_artist_med_term'), 'user_to_artist', ['med_term'], unique=False)
    op.create_index(op.f('ix_user_to_artist_user_id'), 'user_to_artist', ['user_id'], unique=False)
    op.create_table('song',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('rec_count', sa.Integer(), nullable=True),
    sa.Column('external_url', sa.String(length=64), nullable=True),
    sa.Column('uri', sa.String(length=64), nullable=True),
    sa.Column('album_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['album_id'], ['album.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_song_name'), 'song', ['name'], unique=False)
    op.create_table('user_to_album',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('album_id', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.Column('forgotten', sa.Integer(), nullable=True),
    sa.Column('long_term', sa.Integer(), nullable=True),
    sa.Column('med_term', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['album_id'], ['album.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_to_album_album_id'), 'user_to_album', ['album_id'], unique=False)
    op.create_index(op.f('ix_user_to_album_forgotten'), 'user_to_album', ['forgotten'], unique=False)
    op.create_index(op.f('ix_user_to_album_long_term'), 'user_to_album', ['long_term'], unique=False)
    op.create_index(op.f('ix_user_to_album_med_term'), 'user_to_album', ['med_term'], unique=False)
    op.create_index(op.f('ix_user_to_album_user_id'), 'user_to_album', ['user_id'], unique=False)
    op.create_table('artist_to_song',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.String(length=64), nullable=True),
    sa.Column('song_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['song_id'], ['song.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_artist_to_song_artist_id'), 'artist_to_song', ['artist_id'], unique=False)
    op.create_index(op.f('ix_artist_to_song_song_id'), 'artist_to_song', ['song_id'], unique=False)
    op.create_table('user_to_song',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('song_id', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.Column('forgotten', sa.Integer(), nullable=True),
    sa.Column('long_term', sa.Integer(), nullable=True),
    sa.Column('med_term', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['song_id'], ['song.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_to_song_forgotten'), 'user_to_song', ['forgotten'], unique=False)
    op.create_index(op.f('ix_user_to_song_long_term'), 'user_to_song', ['long_term'], unique=False)
    op.create_index(op.f('ix_user_to_song_med_term'), 'user_to_song', ['med_term'], unique=False)
    op.create_index(op.f('ix_user_to_song_song_id'), 'user_to_song', ['song_id'], unique=False)
    op.create_index(op.f('ix_user_to_song_user_id'), 'user_to_song', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_to_song_user_id'), table_name='user_to_song')
    op.drop_index(op.f('ix_user_to_song_song_id'), table_name='user_to_song')
    op.drop_index(op.f('ix_user_to_song_med_term'), table_name='user_to_song')
    op.drop_index(op.f('ix_user_to_song_long_term'), table_name='user_to_song')
    op.drop_index(op.f('ix_user_to_song_forgotten'), table_name='user_to_song')
    op.drop_table('user_to_song')
    op.drop_index(op.f('ix_artist_to_song_song_id'), table_name='artist_to_song')
    op.drop_index(op.f('ix_artist_to_song_artist_id'), table_name='artist_to_song')
    op.drop_table('artist_to_song')
    op.drop_index(op.f('ix_user_to_album_user_id'), table_name='user_to_album')
    op.drop_index(op.f('ix_user_to_album_med_term'), table_name='user_to_album')
    op.drop_index(op.f('ix_user_to_album_long_term'), table_name='user_to_album')
    op.drop_index(op.f('ix_user_to_album_forgotten'), table_name='user_to_album')
    op.drop_index(op.f('ix_user_to_album_album_id'), table_name='user_to_album')
    op.drop_table('user_to_album')
    op.drop_index(op.f('ix_song_name'), table_name='song')
    op.drop_table('song')
    op.drop_index(op.f('ix_user_to_artist_user_id'), table_name='user_to_artist')
    op.drop_index(op.f('ix_user_to_artist_med_term'), table_name='user_to_artist')
    op.drop_index(op.f('ix_user_to_artist_long_term'), table_name='user_to_artist')
    op.drop_index(op.f('ix_user_to_artist_forgotten'), table_name='user_to_artist')
    op.drop_index(op.f('ix_user_to_artist_artist_id'), table_name='user_to_artist')
    op.drop_table('user_to_artist')
    op.drop_index(op.f('ix_album_name'), table_name='album')
    op.drop_table('album')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_artist_name'), table_name='artist')
    op.drop_table('artist')
    # ### end Alembic commands ###
