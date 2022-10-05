from subprocess import run, DEVNULL
import concurrent.futures
from tempfile import TemporaryDirectory
from shutil import copy
from os import listdir
from os.path import join

from utils.functions import *
from models.Playlist import Playlist
from models.Track import Track

class Download():

    def __init__(self, donwload_link, output_folder):
        self.__link = clear_link(donwload_link)
        self.__output_folder = output_folder
        self.__all_tracks = []
        self.__type = self.check_type()
        self.__playlist_id = 0
        self.__check_exists = self.exists()

        export_environment_variables()
        self.load_tracks()


    def load_tracks(self):
        """
        Buscar lista de musicas da playlist ou album
        """
        self.__all_tracks = get_link_tracks(self.__link, self.__type)
        if self.__type != 'track':
            self.__playlist_id = self.save_playlist()
    

    def save_playlist(self):
        """
        Salvar a playlist na memória
        """
        if not self.exists():
            playlist_id = Playlist.create(link=self.__link)
        else:
            result_query = Playlist.select().dicts().where(Playlist.link == self.__link)
            for line in result_query:
                playlist_id = line.get('id')

        return playlist_id
     

    def exists(self):
        """
        Checa se a playlist já foi baixada
        """
        if self.__type == 'track':
            result = False
        else:
            if self.__playlist_id:
                result = self.__check_exists
            else:
                result = False
                result_query = Playlist.select().where(Playlist.link == self.__link)
                if result_query:
                    result = True

        return result


    def is_updated(self):
        """
        Checar se a playlist já foi baixada e está atualizada
        """
        if self.__type == 'track':
            return False
        else:
            return self.number_tracks_to_download() == 0
    

    def number_tracks_to_download(self):
        """
        Checar quantas musicas será necessário baixar
        """
        result = []
        for track in self.__all_tracks:
            url = track.get('url')
            name = track.get('name')
            if not self.exist_track(self.__playlist_id, name, url):
                result.append(track)

        return len(result)


    def download_all(self):
        """
        Apaga todas as musicas já baixadas da playlist
        """
        Track.delete().where(Track.playlist_id == self.__playlist_id).execute()


    def download_tracks(self):
        """
        Realiza o donwload das musicas da playlist
        """
        total_tracks = self.number_tracks_to_download()
        temp_directory = TemporaryDirectory()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []

            for track in self.__all_tracks:
                url = track.get('url')
                name = track.get('name')
                if not self.exist_track(self.__playlist_id, name, url):
                    futures.append(executor.submit(self.download, link=url, name_track=name, output_folder=temp_directory.name))

            for index, future in enumerate(concurrent.futures.as_completed(futures)):
                track_name, link_track = future.result()
                if self.__playlist_id:
                    self.save_track(self.__playlist_id, track_name, link_track)

                yield index+1, total_tracks, track_name

        self.move_output_folder(temp_directory.name)
        temp_directory.cleanup()
 
    
    def exist_track(self, playlist_id, name, link):
        """
        Checa se a musica já foi baixada
        """
        result = False
        result_query = Track.select().where(Track.playlist_id == playlist_id, Track.name == name, Track.link == link)
        if result_query:
            result = True

        return result


    def download(self, link, name_track, output_folder):
        """
        Executa via linha de comando a instrução para baixar uma musica
        """
        run([f"spotify_dl -l '{link}' -o {output_folder}"], shell=True, stdout=DEVNULL)
        return name_track, link

    
    def save_track(self, playlist_id, name, link):
        """
        Salvar musica na memória
        """
        Track.create(playlist_id=playlist_id, name=name, link=link)


    def move_output_folder(self, temp_directory):
        """
        Move todas as musicas do diretório temporário para
        a pasta de saída informada pelo usuário
        """
        for directory in listdir(temp_directory):
            full_path = join(temp_directory, directory)
            for file in listdir(full_path):
                if file.endswith('.mp3'):
                    path_file = join(full_path, file)
                    copy(path_file, self.__output_folder)
    
    
    def check_type(self):
        """
        Checa se o link para baixar é referente a uma playlist, album ou musica aleatória
        """
        types = ['playlist', 'album', 'track']
        for type in types:
            if type in self.__link:
                return type