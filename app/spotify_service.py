import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import session, request, redirect

scope = "user-top-read"

def example_get():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)

    # if not auth_manager.validate_token(cache_handler.get_cached_token()):
    #     return redirect('/')

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
