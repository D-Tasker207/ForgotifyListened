from app import db, login
from flask import current_app
from flask_login import UserMixin 


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True)
    last_pulled = db.Column(db.DateTime)
    forgotten_songs = db.relationship("UserToSongF", backref='user', lazy='dynamic')
    forgotten_artists = db.relationship("UserToArtistF", backref='user', lazy='dynamic')
    forgotten_albums = db.relationship("UserToAlbumF", backref='user', lazy='dynamic')

    one_year_songs = db.relationship("UserToSongOY", backref='user', lazy='dynamic')
    one_year_artists = db.relationship("UserToArtistOY", backref='user', lazy='dynamic')
    one_year_albums = db.relationship("UserToAlbumOY", backref='user', lazy='dynamic')

    six_month_songs = db.relationship("UserToSongSM", backref='user', lazy='dynamic')
    six_month_artists = db.relationship("UserToArtistSM", backref='user', lazy='dynamic')
    six_month_albums = db.relationship("UserToAlbumSM", backref='user', lazy='dynamic')

    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Album(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True)
    rec_count = db.Column(db.Integer, default=0)
    img = db.Column(db.String(100))
    external_url = db.Column(db.String(64))
    uri = db.Column(db.String(64))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    songs = db.relationship("Song", backref="album", lazy='dynamic')
    user2albumF = db.relationship('UserToAlbumF', backref='album', lazy='dynamic')
    user2albumOY = db.relationship('UserToAlbumOY', backref='album', lazy='dynamic')
    user2albumSM = db.relationship('UserToAlbumSM', backref='album', lazy='dynamic')


class Artist(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True)
    rec_count = db.Column(db.Integer)
    img = db.Column(db.String(100))
    external_url = db.Column(db.String(64))
    uri = db.Column(db.String(64))
    songs = db.relationship('ArtistToSong', backref='artist', lazy='dynamic')
    user2artistF = db.relationship('UserToArtistF', backref='artist', lazy='dynamic')
    user2artistOY = db.relationship('UserToArtistOY', backref='artist', lazy='dynamic')
    user2artistSM = db.relationship('UserToArtistSM', backref='artist', lazy='dynamic')


class Song(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True)
    rec_count = db.Column(db.Integer)
    external_url = db.Column(db.String(64))
    uri = db.Column(db.String(64))
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    artists = db.relationship('ArtistToSong', backref='song', lazy='dynamic')
    user2songF = db.relationship('UserToSongF', backref='song', lazy='dynamic')
    user2songOY = db.relationship('UserToSongOY', backref='song', lazy='dynamic')
    user2songSM = db.relationship('UserToSongSM', backref='song', lazy='dynamic')


class ArtistToSong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(64), db.ForeignKey('artist.id'), index=True)
    song_id = db.Column(db.String(64), db.ForeignKey('song.id'), index=True)

class UserToSongF(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.String(64), db.ForeignKey('song.id'), index=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), index=True)

    def __repr__(self):
        return str(self.song_id) + " " + str(self.user_id)

class UserToSongOY(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.String(64), db.ForeignKey('song.id'), index=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), index=True)

    def __repr__(self):
        return str(self.song_id) + " " + str(self.user_id)

class UserToSongSM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.String(64), db.ForeignKey('song.id'), index=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), index=True)

    def __repr__(self):
        return str(self.song_id) + " " + str(self.user_id)


class UserToAlbumF(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.String(64), db.ForeignKey('album.id'), index=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), index=True)

    def __repr__(self):
        return str(self.album_id) + " " + str(self.user_id)

class UserToAlbumOY(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.String(64), db.ForeignKey('album.id'), index=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), index=True)

    def __repr__(self):
        return str(self.album_id) + " " + str(self.user_id)

class UserToAlbumSM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.String(64), db.ForeignKey('album.id'), index=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), index=True)

    def __repr__(self):
        return str(self.album_id) + " " + str(self.user_id)


class UserToArtistF(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(64), db.ForeignKey('artist.id'), index=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), index=True)

    def __repr__(self):
        return str(self.artist_id) + " " + str(self.user_id)

class UserToArtistOY(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(64), db.ForeignKey('artist.id'), index=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), index=True)

    def __repr__(self):
        return str(self.artist_id) + " " + str(self.user_id)

class UserToArtistSM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(64), db.ForeignKey('artist.id'), index=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), index=True)

    def __repr__(self):
        return str(self.artist_id) + " " + str(self.user_id)
