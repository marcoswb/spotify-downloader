from dotenv import load_dotenv
from os import getenv, environ, system
from os.path import isdir
import configparser
from mutagen.easyid3 import EasyID3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def is_null(value):
    formated_value = str(value).strip()
    return formated_value == ''


def get_link_tracks(download_link, type_register):
    load_dotenv()

    client_id = getenv('SPOTIFY_CLIENT_ID')
    client_secret = getenv('SPOTIFY_CLIENT_SECRET')

    spotify_client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    ))

    all_tracks = []
    name_playlist = None
    if type_register == 'track':
        spotify_search = spotify_client.track(download_link)
        all_tracks.append({ 'name': spotify_search['name'], 'url': download_link })
    else:
        if type_register == 'album':
            result = spotify_client.album_tracks(download_link)
            name_playlist = spotify_client.album(download_link).get('name')
            tracks_infos = result.get('items')

            if result.get('next'):
                tracks_infos.extend(get_next_results(spotify_client, result))

            for track in tracks_infos:
                url = track.get('external_urls', {}).get('spotify')
                name = track.get('name')
                all_tracks.append({'url': url, 'name': name})
        else:
            result = spotify_client.playlist_items(download_link)
            name_playlist = spotify_client.user_playlist(user=None, playlist_id=download_link, fields='name').get('name')
            tracks_infos = result.get('items')

            if result.get('next'):
                tracks_infos.extend(get_next_results(spotify_client, result))

            for track in tracks_infos:
                url = track.get('track', {}).get('external_urls', {}).get('spotify')
                name = track.get('track', {}).get('name')
                all_tracks.append({'url': url, 'name': name})

    return all_tracks, name_playlist


def get_next_results(spotify_client, result):
    new_result = spotify_client.next(result)

    all_results = new_result.get('items')
    if new_result.get('next'):
        all_results.extend(get_next_results(spotify_client, new_result))

    return all_results


def export_environment_variables():
    load_dotenv()

    client_id = getenv('SPOTIFY_CLIENT_ID')
    client_secret = getenv('SPOTIFY_CLIENT_SECRET')

    environ["SPOTIPY_CLIENT_ID"] = client_id
    environ["SPOTIPY_CLIENT_SECRET"] = client_secret


def clear_link(link):
    end_position = str(link).index('si=') -1
    return str(link)[:end_position]


def input_user(message, limit_response=None, check_is_dir=False, allow_empty=False):
    """
    Perguntar algo ao usuário
    """
    while True:
        response = input(f'{message} => ')
        
        if not limit_response:
            if is_null(response):
                if allow_empty:
                    result = None
                    break
                print('Digite uma resposta válida!')
            else:
                if check_is_dir:
                    if not isdir(response):
                        print('Digite um diretório válido!')
                    else:
                        result = str(response)
                        break
                else:
                    result = str(response)
                    break
        else:
            if response.upper() not in limit_response:
                print('Digite uma resposta válida!')
            else:
                result = str(response).upper()
                break
    
    return result


def get_output_directory():
    """
    Checa se existe um arquivo config.ini com a configuração
    do caminho de saída e se não existir cria ele
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    if not config.get('DEFAULT', 'output_directory', fallback=False):
        with open('config.ini', 'w') as configfile:
            response = input_user('Informe a pasta de saída', check_is_dir=True)
            config['DEFAULT']['output_directory'] = response
            config.write(configfile)

    return config.get('DEFAULT', 'output_directory')


def clean_screen():
    """
    Limpar tela do terminal
    """
    system('cls')


def get_track_infos(path_track):
    """
    Recupera informações de uma música
    """
    result = EasyID3(path_track)
    return result