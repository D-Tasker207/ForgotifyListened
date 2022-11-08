import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import session, redirect, url_for
from flask_login  import current_user
from  app import db
from app.models import Album, Artist, Song, ArtistToSong, User, UserToAlbum, UserToArtist, UserToSong

def example_get():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect(url_for('index'))

    sp = spotipy.Spotify(auth_manager=auth_manager)

    myList = []
    results = sp.current_user_top_tracks(limit=50, time_range="short_term")

    for idx, item in enumerate(results['items']):
        thisSong = {
            'name': item['name'],
            'img': item['album']['images'][2]['url'],
        }
        artists = []
        for artist in item['artists']:
            artists.append(artist['name'])
        thisSong['artists'] = artists
        myList.append(thisSong)
            
    return myList

def get_user():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    return sp.current_user()


def get_user_current_trcks():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect(url_for('index'))

    results = sp.current_user_top_tracks(limit=50, time_range="short_term")

    songs = []
    artists = []
    albums = []

    for track in results['items']:
        thisSong = {
            'id': track['id'],
            'name': track['name'],
            'external_url': track['external_urls']['spotify'],
            'uri': track['uri'],
            'album_id': track['album']['id'],
            'artists': []
        }

        for artist in track['artists']:
            artist_info = sp.artist(artist_id=artist['id'])

            thisSong['artists'].append(artist_info['id'])
            
            thisArtist = {
                'id': artist_info['id'],
                'name': artist_info['name'],
                'external_url': artist_info['external_urls']['spotify'],
                'uri': artist_info['uri'],
                'img': artist_info['images'][0]['url']
            }
            artists.append(thisArtist)
        songs.append(thisSong)

        thisAlbum = {
            'id': track['album']['id'],
            'name': track['album']['name'],
            'img': track['album']['images'][0]['url'],
            'external_url': track['album']['external_urls']['spotify'],
            'uri': track['album']['uri'],
            'artist_id': track['album']['artist'][0]['id']
        }

        albums.append(thisAlbum)

    return (songs, artists, albums)

def add_artists_to_db(artists_list):
    artists_to_add = []
    for artist in artists_list:
        artist_exists = Artist.query.filter_by(id=artist['id']).first()

        if artist_exists == None:
            new_artist = Artist(id=artist['id'], name=artist['name'], img=artist['img'], external_url=artist['external_url'], uri=artist['uri'])
            artists_to_add.append(new_artist)
    
    db.session.addAll(artists_to_add)
    db.session.commit()

def add_albums_to_db(albums_list):
    albums_to_add = []
    for album in albums_list:
        album_exists = Album.query.filter_by(id=album['id']).first()

        if album_exists == None:
            new_album = Album(id=album['id'], name=album['name'], img=album['img'], external_url=album['external_url'], uri=album['uri'], artist_id=album['artist_id'])
            albums_to_add.append(new_album)

    db.session.addAll(albums_to_add)   
    db.session.commit()

def add_songs_to_db(songs_list):
    songs_to_add = []
    artist_to_song_to_add = []
    for song in songs_list:
        song_exists = Song.query.filter_by(id=song['id']).first()

        if song_exists == None:
            new_song = Song(id=song['id'], name=song['name'], img=song['img'], external_url=song['external_url'], uri=song['uri'], albut_id=song['album_id'])
            songs_to_add.append(new_song)
            for artist in song['artists']:
                new_artist_to_song = ArtistToSong(artist_id=artist, song_id=song['id'])
                artist_to_song_to_add.append(new_artist_to_song)
    
    db.session.addAll(songs_to_add)
    db.session.addAll(artist_to_song_to_add)
    db.session.commit()