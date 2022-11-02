import spotipy
from spotipy.oauth2 import SpotifyOAuth

class Spotify:

    sp = None
    
    def __init__(self):
        scope = "user-library-read"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    def example_get(self):
        myList = []
        results = self.sp.current_user_saved_tracks()
        for idx, item in enumerate(results['items']):
            track = item['track']
            myList.append((idx, track['artists'][0]['name'], "-", track['name']))

        return myList
