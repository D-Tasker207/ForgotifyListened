from app import db, login
from flask_login import UserMixin 


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True)
    last_pulled = db.Column(db.DateTime)
    songs = db.relationship("UserToSong", backref='user', lazy='dynamic')
    artists = db.relationship("UserToArtist", backref='user', lazy='dynamic')
    albums = db.relationship("UserToAlbum", backref='user', lazy='dynamic')


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Album(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True)
    rec_count = db.Column(db.Integer)
    img = db.Column(db.String(100))
    external_url = db.Column(db.String(64))
    uri = db.Column(db.String(64))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    songs = db.relationship("Song", backref="album", lazy='dynamic')
    song2album = db.relationship('AlbumToSong', backref='album', lazy='dynamic')



class Artist(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True)
    rec_count = db.Column(db.Integer)
    img = db.Column(db.String(100))
    external_url = db.Column(db.String(64))
    uri = db.Column(db.String(64))
    artist2song = db.relationship('ArtistToSong', backref='artist', lazy='dynamic')


class Song(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True)
    rec_count = db.Column(db.Integer)
    external_url = db.Column(db.String(64))
    uri = db.Column(db.String(64))
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    artist2song = db.relationship('ArtistToSong', backref='song', lazy='dynamic')
    song2album = db.relationship('AlbumToSong', backref='song', lazy='dynamic')


class ArtistToSong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(64), db.ForeignKey('artist.id'), index=True)
    song_id = db.Column(db.String(64), db.ForeignKey('song.id'), index=True)

class AlbumToSong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.String(64), db.ForeignKey('album.id'), index=True)
    song_id = db.Column(db.String(64), db.ForeignKey('song.id'), index=True)

class UserToSong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.String(64), db.ForeignKey('song.id'), index=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), index=True)

    #mutually exclusive, should be 1 or 0 for true and false
    forgotten = db.Column(db.Integer, index=True)
    long_term = db.Column(db.Integer,  index=True)
    med_term = db.Column(db.Integer, index=True)


class UserToAlbum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.String(64), db.ForeignKey('album.id'), index=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), index=True)

    #mutually exclusive, should be 1 or 0 for true and false
    forgotten = db.Column(db.Integer, index=True)
    long_term = db.Column(db.Integer,  index=True)
    med_term = db.Column(db.Integer, index=True)


class UserToArtist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(64), db.ForeignKey('artist.id'), index=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), index=True)

    #mutually exclusive, should be 1 or 0 for true and false
    forgotten = db.Column(db.Integer, index=True)
    long_term = db.Column(db.Integer,  index=True)
    med_term = db.Column(db.Integer, index=True)
