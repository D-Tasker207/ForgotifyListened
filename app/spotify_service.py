import spotipy
from flask import session, redirect, url_for
from flask_login  import current_user
from app import db
from datetime import datetime
from rq import get_current_job
from app.models import Album, Artist, Song, ArtistToSong, User, UserToAlbum, UserToArtist, UserToSong, Task


# def _set_task_progress(progress):
#     job = get_current_job()
#     if job:
#         job.meta['progress'] = progress
#         job.save_meta()

#         task = Task.query.get(job.get_id())
        
#         if progress >= 100:
#             task.complete = True
#         db.session.commit()

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
    add_user_song_links(long_term_data[0], data_type)
    add_user_artist_links(long_term_data[1], data_type)
    add_user_album_links(long_term_data[2], data_type)
    
def add_user_long_term_data(long_term_data):
    data_type = [0,1,0]
    add_user_song_links(long_term_data[0], data_type)
    add_user_artist_links(long_term_data[1], data_type)
    add_user_album_links(long_term_data[2], data_type)

def add_user_med_term_data(med_term_data):
    data_type = [0,0,1]
    add_user_song_links(med_term_data[0], data_type)
    add_user_artist_links(med_term_data[1], data_type)
    add_user_album_links(med_term_data[2], data_type)

def add_user_song_links(song_list, data_type):
    for song in song_list:
        entry_present = UserToSong.query.filter_by(song_id = song['id'], user_id = current_user.id, 
            forgotten=data_type[0], long_term=data_type[1], med_term=data_type[2]).first()
        if (entry_present is None):
            new_u2s = UserToSong(
                user_id = current_user.id, 
                song_id = song['id'], 
                forgotten=data_type[0], 
                long_term=data_type[1], 
                med_term=data_type[2])
            db.session.add(new_u2s)
            db.session.commit()

def add_user_artist_links(artist_list, data_type):
    for artist in artist_list:
        entry_present = UserToArtist.query.filter_by(artist_id = artist['id'], user_id = current_user.id,
        forgotten=data_type[0], long_term=data_type[1], med_term=data_type[2]).first()
        if (entry_present is None):
            new_u2ar = UserToArtist(
                user_id = current_user.id,
                artist_id = artist['id'], 
                forgotten=data_type[0], 
                long_term=data_type[1],
                med_term=data_type[2])
            db.session.add(new_u2ar)
            db.session.commit()

def add_user_album_links(album_list, data_type):
    u2al = []
    for album in album_list:
        
        entry_present = UserToAlbum.query.filter_by(album_id = album['id'], user_id = current_user.id, 
            forgotten=data_type[0], long_term=data_type[1], med_term=data_type[2]).first() 
        if (entry_present is None):
            new_u2al = UserToAlbum(
                user_id= current_user.id, 
                album_id= album['id'], 
                forgotten=data_type[0], 
                long_term=data_type[1], 
                med_term=data_type[2])
            db.session.add(new_u2al)
            db.session.commit()

def update_user_data():
    delete_current_user_links()
    user_data = get_new_user_data()
    create_user_links(user_data)
    User.query.filter_by(id=current_user.get_id()).first().last_pulled = datetime.now() 

def delete_current_user_links():
    #delete all links in the user join tables
    UserToAlbum.filter_by(user_id=current_user.id).delete()
    UserToArtist.filter_by(user_id=current_user.id).delete()
    UserToSong.filter_by(user_id=current_user.id).delete()
    db.session.commit()