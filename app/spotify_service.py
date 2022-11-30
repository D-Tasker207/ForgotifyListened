import spotipy
from flask import session, redirect, url_for
from flask_login  import current_user
from app import db
from datetime import datetime
from app.models import Album, Artist, Song, ArtistToSong, User, UserToAlbumF, UserToArtistF, UserToSongF, UserToAlbumOY, UserToSongOY, UserToArtistOY, UserToSongOY, UserToSongOY, UserToAlbumSM, UserToArtistSM, UserToSongSM

def get_user():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    return sp.current_user()

def get_new_user_data():
    short_term_data = get_user_current_tracks("short_term")
    medium_term_data = get_user_current_tracks("medium_term")
    long_term_data = get_user_current_tracks("long_term")

    user_data = [short_term_data, medium_term_data, long_term_data]

    for data in user_data:
        add_songs_to_db(data[0])
        add_artists_to_db(data[1])
        add_albums_to_db(data[2])
        
    return user_data

#this is not a good name for the function but idk what a a better name would be. 
# it creates the links between the user and the music stuff for the mystuff pages
def create_user_links():
    user_data = get_new_user_data()

    add_user_long_term_data(user_data[2])
    add_user_med_term_data(user_data[1])
    add_user_forgotten_data(user_data)

    u = User.query.filter_by(id=current_user.get_id()).first()
    u.last_pulled = datetime.now()
    db.session.add(u)
    db.session.commit()

def get_user_current_tracks(time_range):
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect(url_for('index'))

    results = sp.current_user_top_tracks(limit=50, time_range=time_range)

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
                'uri': artist_info['uri']
            }
            try:
                thisArtist['img']= artist_info['images'][0]['url']
            except IndexError:
                thisArtist['img'] = 'na'

            artists.append(thisArtist)
        songs.append(thisSong)

        thisAlbum = {
            'id': track['album']['id'],
            'name': track['album']['name'],
            'img': track['album']['images'][0]['url'],
            'external_url': track['album']['external_urls']['spotify'],
            'uri': track['album']['uri'],
            'artist_id': track['album']['artists'][0]['id']
        }

        albums.append(thisAlbum)

    return (songs, artists, albums)

def add_artists_to_db(artists_list):
    for artist in artists_list:
        artist_exists = Artist.query.filter_by(id=artist['id']).first()

        if artist_exists == None:
            new_artist = Artist(
                id=artist['id'], 
                name=artist['name'], 
                img=artist['img'], 
                external_url=artist['external_url'], 
                uri=artist['uri']
            )
            db.session.add(new_artist)
            db.session.commit()

def add_albums_to_db(albums_list):
    for album in albums_list:
        album_exists = Album.query.filter_by(id=album['id']).first()

        if album_exists == None:
            new_album = Album(
                id=album['id'], 
                name=album['name'], 
                img=album['img'], 
                external_url=album['external_url'], 
                uri=album['uri'], 
                artist_id=album['artist_id']
            )
            db.session.add(new_album)
            db.session.commit()

def add_songs_to_db(songs_list):
    for song in songs_list:
        song_exists = Song.query.filter_by(id=song['id']).first()

        if song_exists == None:
            new_song = Song(
                id=song['id'], 
                name=song['name'], 
                external_url=song['external_url'], 
                uri=song['uri'], 
                album_id=song['album_id']
            )
            db.session.add(new_song)
            for artist in song['artists']:
                new_artist_to_song = ArtistToSong(
                    artist_id=artist, 
                    song_id=song['id']
                )
                db.session.add(new_artist_to_song)
                db.session.commit()

#good god theres a lot of loops here
def add_user_forgotten_data(user_data):
    data_type = [1,0,0]
    long_term_data = user_data[2]
    med_term_data = user_data[1]
    short_term_data = user_data[0]

    # songs
    for i in long_term_data[0]:
        if ((i in med_term_data[0]) or (i in short_term_data[0])):
            long_term_data[0].remove(i)

    # artist
    for i in long_term_data[1]:
        if ((i in med_term_data[1]) or (i in short_term_data[1])):
            long_term_data[1].remove(i)

    # album
    for i in long_term_data[2]:
        if ((i in med_term_data[2]) or (i in short_term_data[2])):
            long_term_data[2].remove(i)
    
    print("AHHHHHH")
    add_F_user_song_links(long_term_data[0])
    add_F_user_artist_links(long_term_data[1])
    add_F_user_album_links(long_term_data[2])
    
def add_user_long_term_data(long_term_data):
    add_LT_user_song_links(long_term_data[0])
    add_LT_user_artist_links(long_term_data[1])
    add_LT_user_album_links(long_term_data[2])

def add_user_med_term_data(med_term_data):
    add_MT_user_song_links(med_term_data[0])
    add_MT_user_artist_links(med_term_data[1])
    add_MT_user_album_links(med_term_data[2])

def add_LT_user_song_links(song_list):
    for song in song_list:
        entry_present = UserToSongOY.query.filter_by(song_id = song['id'], user_id = current_user.id).first()
        if (entry_present is None):
            new_u2s = UserToSongOY(
                user_id = current_user.id, 
                song_id = song['id'])
            db.session.add(new_u2s)
            db.session.commit()

def add_MT_user_song_links(song_list):
    for song in song_list:
        entry_present = UserToSongSM.query.filter_by(song_id = song['id'], user_id = current_user.id).first()
        if (entry_present is None):
            new_u2s = UserToSongSM(
                user_id = current_user.id, 
                song_id = song['id'])
            db.session.add(new_u2s)
            db.session.commit()

def add_F_user_song_links(song_list):
    for song in song_list:
        entry_present = UserToSongF.query.filter_by(song_id = song['id'], user_id = current_user.id).first()
        if (entry_present is None):
            new_u2s = UserToSongF(
                user_id = current_user.id, 
                song_id = song['id'])
            db.session.add(new_u2s)
            db.session.commit()

def add_LT_user_artist_links(artist_list):
    for artist in artist_list:
        entry_present = UserToArtistOY.query.filter_by(artist_id = artist['id'], user_id = current_user.id).first()
        if (entry_present is None):
            new_u2ar = UserToArtistOY(
                user_id = current_user.id,
                artist_id = artist['id'])
            db.session.add(new_u2ar)
            db.session.commit()

def add_MT_user_artist_links(artist_list):
    for artist in artist_list:
        entry_present = UserToArtistSM.query.filter_by(artist_id = artist['id'], user_id = current_user.id).first()
        if (entry_present is None):
            new_u2ar = UserToArtistSM(
                user_id = current_user.id,
                artist_id = artist['id'])
            db.session.add(new_u2ar)
            db.session.commit()

def add_F_user_artist_links(artist_list):
    for artist in artist_list:
        entry_present = UserToArtistF.query.filter_by(artist_id = artist['id'], user_id = current_user.id).first()
        if (entry_present is None):
            new_u2ar = UserToArtistF(
                user_id = current_user.id,
                artist_id = artist['id'])
            db.session.add(new_u2ar)
            db.session.commit()

def add_LT_user_album_links(album_list):
    for album in album_list:
        entry_present = UserToAlbumOY.query.filter_by(album_id = album['id'], user_id = current_user.id).first() 
        if (entry_present is None):
            new_u2al = UserToAlbumOY(
                user_id= current_user.id, 
                album_id= album['id'])
            db.session.add(new_u2al)
            db.session.commit()

def add_MT_user_album_links(album_list):
    for album in album_list:
        entry_present = UserToAlbumSM.query.filter_by(album_id = album['id'], user_id = current_user.id).first() 
        if (entry_present is None):
            new_u2al = UserToAlbumSM(
                user_id= current_user.id, 
                album_id= album['id'])
            db.session.add(new_u2al)
            db.session.commit()

def add_F_user_album_links(album_list):
    for album in album_list:
        entry_present = UserToAlbumF.query.filter_by(album_id = album['id'], user_id = current_user.id).first() 
        if (entry_present is None):
            new_u2al = UserToAlbumF(
                user_id= current_user.id, 
                album_id= album['id'])
            db.session.add(new_u2al)
            db.session.commit()

def update_user_data():
    delete_current_user_links()
    user_data = get_new_user_data()
    create_user_links(user_data)
    User.query.filter_by(id=current_user.get_id()).first().last_pulled = datetime.now() 

def delete_current_user_links():
    #delete all links in the user join tables
    UserToAlbumF.filter_by(user_id=current_user.id).delete()
    UserToArtistF.filter_by(user_id=current_user.id).delete()
    UserToSongF.filter_by(user_id=current_user.id).delete()

    UserToAlbumOY.filter_by(user_id=current_user.id).delete()
    UserToArtistOY.filter_by(user_id=current_user.id).delete()
    UserToSongOY.filter_by(user_id=current_user.id).delete()

    UserToAlbumSM.filter_by(user_id=current_user.id).delete()
    UserToArtistSM.filter_by(user_id=current_user.id).delete()
    UserToSongSM.filter_by(user_id=current_user.id).delete()
    db.session.commit()