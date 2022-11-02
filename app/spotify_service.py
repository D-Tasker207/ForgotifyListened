import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID");
CLIENT_SECRET = os.getenv("CLIENT_SECRET");

AUTH_URL = 'https://accounts.spotify.com/api/token'

auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

auth_response_data = auth_response.json()

access_token = auth_response_data['access_token']

headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}

BASE_URL = 'https://api.spotify.com/v1/'

track_id = '5jnoK2o5jY46qhPR30RepX?si=5cbc9ebf83014961'

r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
r.json()

print(r.text)