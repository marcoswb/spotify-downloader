
from dotenv import load_dotenv
from os import getenv
import os

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

    all_tracks = []
    for track in spotify_client.playlist_tracks(playlist_link)['items']:
        url = track['track']['external_urls']['spotify']
        name = track['track']['name']
        all_tracks.append({'url': url, 'name': name})
    
    return all_tracks


def get_playlist_name(playlist_link):
    load_dotenv()
    auth_manager = SpotifyClientCredentials()
    credential = spotipy.Spotify(auth_manager=auth_manager)
    user_id = getenv('SPOTIFY_USER_ID')

    playlists = credential.user_playlists(user_id)
    while playlists:
        for index, playlist in enumerate(playlists['items']):
            if playlist.get('external_urls').get('spotify') in playlist_link:
                return playlist.get('name')


def export_environment_variables():
    load_dotenv()

    client_id = getenv('SPOTIFY_CLIENT_ID')
    client_secret = getenv('SPOTIFY_CLIENT_SECRET')

    os.environ["SPOTIPY_CLIENT_ID"] = client_id
    os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret


def clear_link(link):
    end_position = str(link).index('si=') -1
    return str(link)[:end_position]