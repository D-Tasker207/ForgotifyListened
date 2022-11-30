"""empty message

Revision ID: 4e49a3232289
Revises: 6cede65d808c
Create Date: 2022-11-30 12:38:49.208916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e49a3232289'
down_revision = '6cede65d808c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_to_artist_f',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_to_artist_f_artist_id'), 'user_to_artist_f', ['artist_id'], unique=False)
    op.create_index(op.f('ix_user_to_artist_f_user_id'), 'user_to_artist_f', ['user_id'], unique=False)
    op.create_table('user_to_artist_oy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_to_artist_oy_artist_id'), 'user_to_artist_oy', ['artist_id'], unique=False)
    op.create_index(op.f('ix_user_to_artist_oy_user_id'), 'user_to_artist_oy', ['user_id'], unique=False)
    op.create_table('user_to_artist_sm',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_to_artist_sm_artist_id'), 'user_to_artist_sm', ['artist_id'], unique=False)
    op.create_index(op.f('ix_user_to_artist_sm_user_id'), 'user_to_artist_sm', ['user_id'], unique=False)
    op.create_table('user_to_album_f',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('album_id', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['album_id'], ['album.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_to_album_f_album_id'), 'user_to_album_f', ['album_id'], unique=False)
    op.create_index(op.f('ix_user_to_album_f_user_id'), 'user_to_album_f', ['user_id'], unique=False)
    op.create_table('user_to_album_oy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('album_id', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['album_id'], ['album.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_to_album_oy_album_id'), 'user_to_album_oy', ['album_id'], unique=False)
    op.create_index(op.f('ix_user_to_album_oy_user_id'), 'user_to_album_oy', ['user_id'], unique=False)
    op.create_table('user_to_album_sm',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('album_id', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['album_id'], ['album.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_to_album_sm_album_id'), 'user_to_album_sm', ['album_id'], unique=False)
    op.create_index(op.f('ix_user_to_album_sm_user_id'), 'user_to_album_sm', ['user_id'], unique=False)
    op.create_table('user_to_song_f',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('song_id', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['song_id'], ['song.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_to_song_f_song_id'), 'user_to_song_f', ['song_id'], unique=False)
    op.create_index(op.f('ix_user_to_song_f_user_id'), 'user_to_song_f', ['user_id'], unique=False)
    op.create_table('user_to_song_oy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('song_id', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['song_id'], ['song.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_to_song_oy_song_id'), 'user_to_song_oy', ['song_id'], unique=False)
    op.create_index(op.f('ix_user_to_song_oy_user_id'), 'user_to_song_oy', ['user_id'], unique=False)
    op.create_table('user_to_song_sm',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('song_id', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['song_id'], ['song.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_to_song_sm_song_id'), 'user_to_song_sm', ['song_id'], unique=False)
    op.create_index(op.f('ix_user_to_song_sm_user_id'), 'user_to_song_sm', ['user_id'], unique=False)
    op.drop_index('ix_user_to_artist_artist_id', table_name='user_to_artist')
    op.drop_index('ix_user_to_artist_forgotten', table_name='user_to_artist')
    op.drop_index('ix_user_to_artist_long_term', table_name='user_to_artist')
    op.drop_index('ix_user_to_artist_med_term', table_name='user_to_artist')
    op.drop_index('ix_user_to_artist_user_id', table_name='user_to_artist')
    op.drop_table('user_to_artist')
    op.drop_index('ix_user_to_album_album_id', table_name='user_to_album')
    op.drop_index('ix_user_to_album_forgotten', table_name='user_to_album')
    op.drop_index('ix_user_to_album_long_term', table_name='user_to_album')
    op.drop_index('ix_user_to_album_med_term', table_name='user_to_album')
    op.drop_index('ix_user_to_album_user_id', table_name='user_to_album')
    op.drop_table('user_to_album')
    op.drop_index('ix_user_to_song_forgotten', table_name='user_to_song')
    op.drop_index('ix_user_to_song_long_term', table_name='user_to_song')
    op.drop_index('ix_user_to_song_med_term', table_name='user_to_song')
    op.drop_index('ix_user_to_song_song_id', table_name='user_to_song')
    op.drop_index('ix_user_to_song_user_id', table_name='user_to_song')
    op.drop_table('user_to_song')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_to_song',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('song_id', sa.VARCHAR(length=64), nullable=True),
    sa.Column('user_id', sa.VARCHAR(length=64), nullable=True),
    sa.Column('forgotten', sa.INTEGER(), nullable=True),
    sa.Column('long_term', sa.INTEGER(), nullable=True),
    sa.Column('med_term', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['song_id'], ['song.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_to_song_user_id', 'user_to_song', ['user_id'], unique=False)
    op.create_index('ix_user_to_song_song_id', 'user_to_song', ['song_id'], unique=False)
    op.create_index('ix_user_to_song_med_term', 'user_to_song', ['med_term'], unique=False)
    op.create_index('ix_user_to_song_long_term', 'user_to_song', ['long_term'], unique=False)
    op.create_index('ix_user_to_song_forgotten', 'user_to_song', ['forgotten'], unique=False)
    op.create_table('user_to_album',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('album_id', sa.VARCHAR(length=64), nullable=True),
    sa.Column('user_id', sa.VARCHAR(length=64), nullable=True),
    sa.Column('forgotten', sa.INTEGER(), nullable=True),
    sa.Column('long_term', sa.INTEGER(), nullable=True),
    sa.Column('med_term', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['album_id'], ['album.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_to_album_user_id', 'user_to_album', ['user_id'], unique=False)
    op.create_index('ix_user_to_album_med_term', 'user_to_album', ['med_term'], unique=False)
    op.create_index('ix_user_to_album_long_term', 'user_to_album', ['long_term'], unique=False)
    op.create_index('ix_user_to_album_forgotten', 'user_to_album', ['forgotten'], unique=False)
    op.create_index('ix_user_to_album_album_id', 'user_to_album', ['album_id'], unique=False)
    op.create_table('user_to_artist',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('artist_id', sa.VARCHAR(length=64), nullable=True),
    sa.Column('user_id', sa.VARCHAR(length=64), nullable=True),
    sa.Column('forgotten', sa.INTEGER(), nullable=True),
    sa.Column('long_term', sa.INTEGER(), nullable=True),
    sa.Column('med_term', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_to_artist_user_id', 'user_to_artist', ['user_id'], unique=False)
    op.create_index('ix_user_to_artist_med_term', 'user_to_artist', ['med_term'], unique=False)
    op.create_index('ix_user_to_artist_long_term', 'user_to_artist', ['long_term'], unique=False)
    op.create_index('ix_user_to_artist_forgotten', 'user_to_artist', ['forgotten'], unique=False)
    op.create_index('ix_user_to_artist_artist_id', 'user_to_artist', ['artist_id'], unique=False)
    op.drop_index(op.f('ix_user_to_song_sm_user_id'), table_name='user_to_song_sm')
    op.drop_index(op.f('ix_user_to_song_sm_song_id'), table_name='user_to_song_sm')
    op.drop_table('user_to_song_sm')
    op.drop_index(op.f('ix_user_to_song_oy_user_id'), table_name='user_to_song_oy')
    op.drop_index(op.f('ix_user_to_song_oy_song_id'), table_name='user_to_song_oy')
    op.drop_table('user_to_song_oy')
    op.drop_index(op.f('ix_user_to_song_f_user_id'), table_name='user_to_song_f')
    op.drop_index(op.f('ix_user_to_song_f_song_id'), table_name='user_to_song_f')
    op.drop_table('user_to_song_f')
    op.drop_index(op.f('ix_user_to_album_sm_user_id'), table_name='user_to_album_sm')
    op.drop_index(op.f('ix_user_to_album_sm_album_id'), table_name='user_to_album_sm')
    op.drop_table('user_to_album_sm')
    op.drop_index(op.f('ix_user_to_album_oy_user_id'), table_name='user_to_album_oy')
    op.drop_index(op.f('ix_user_to_album_oy_album_id'), table_name='user_to_album_oy')
    op.drop_table('user_to_album_oy')
    op.drop_index(op.f('ix_user_to_album_f_user_id'), table_name='user_to_album_f')
    op.drop_index(op.f('ix_user_to_album_f_album_id'), table_name='user_to_album_f')
    op.drop_table('user_to_album_f')
    op.drop_index(op.f('ix_user_to_artist_sm_user_id'), table_name='user_to_artist_sm')
    op.drop_index(op.f('ix_user_to_artist_sm_artist_id'), table_name='user_to_artist_sm')
    op.drop_table('user_to_artist_sm')
    op.drop_index(op.f('ix_user_to_artist_oy_user_id'), table_name='user_to_artist_oy')
    op.drop_index(op.f('ix_user_to_artist_oy_artist_id'), table_name='user_to_artist_oy')
    op.drop_table('user_to_artist_oy')
    op.drop_index(op.f('ix_user_to_artist_f_user_id'), table_name='user_to_artist_f')
    op.drop_index(op.f('ix_user_to_artist_f_artist_id'), table_name='user_to_artist_f')
    op.drop_table('user_to_artist_f')
    # ### end Alembic commands ###