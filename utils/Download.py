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

    def __init__(self, playlist_link, output_folder):
        self.__link = clear_link(playlist_link)
        self.__output_folder = output_folder
        self.__all_tracks = []

        export_environment_variables()
        self.load_tracks()
    

    def load_tracks(self):
        """
        Buscar lista de musicas da playlist
        """
        self.__all_tracks = get_link_tracks(self.__link)
        self.__playlist_id = self.save_playlist()
    

    def save_playlist(self):
        """
        Salvar a playlist na memória
        """
        if not self.exists():
            playlist_id = Playlist.create(name=get_playlist_name(self.__link), link=self.__link)
        else:
            result_query = Playlist.select().dicts().where(Playlist.link == self.__link)
            for line in result_query:
                playlist_id = line.get('id')

        return playlist_id
     

    def exists(self):
        """
        Checa se a playlist já foi baixada
        """
        result = False
        result_query = Playlist.select().where(Playlist.link == self.__link)
        if result_query:
            result = True

        return result


    def is_updated(self):
        """
        Checar se a playlist já foi baixada e está atualizada
        """
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