
from dotenv import load_dotenv
from os import getenv

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def is_null(value):
    formated_value = str(value).strip()
    return formated_value == ''

def get_link_tracks(playlist_link):
    load_dotenv()

    client_id = getenv('SPOTIFY_CLIENT_ID')
    client_secret = getenv('SPOTIFY_CLIENT_SECRET')

    spotify_client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    ))

    for track in spotify_client.playlist_tracks(playlist_link)['items']:
        url = track['track']['external_urls']['spotify']
        yield url
    