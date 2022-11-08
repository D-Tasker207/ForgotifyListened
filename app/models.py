from app import db, login
from flask_login import UserMixin 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True)
    last_pulled = db.Column(db.DateTime)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    img = db.Column(db.String(100))
    external_url = db.Column(db.String(64))
    uri = db.Column(db.String(64))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    img = db.Column(db.String(100))
    external_url = db.Column(db.String(64))
    uri = db.Column(db.String(64))
    artist2song = db.relationship('ArtistToSong', backref='artist', lazy='dynamic')

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    external_url = db.Column(db.String(64))
    uri = db.Column(db.String(64))
    album = db.Column(db.Integer, db.ForeignKey('album.id'))
    artist2song = db.relationship('ArtistToSong', backref='song', lazy='dynamic')

class ArtistToSong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), index=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), index=True)

class UserToSong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)

class UserToAlbum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)

class UserToArtist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)