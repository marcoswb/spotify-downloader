from subprocess import run, DEVNULL
import concurrent.futures
from time import sleep
from tempfile import TemporaryDirectory
from shutil import copy
from os import listdir
from os.path import join

from utils.functions import *
from models.Playlist import Playlist
from models.Track import Track

class Download():

    def init(self, link, output_folder):
        export_environment_variables()

        self.__link = clear_link(link)
        self.__output_folder = output_folder
        self.__all_tracks = get_link_tracks(self.__link)
        playlist_exist = self.check_existence()
        self.__playlist_id = self.save_playlist()

        return playlist_exist


    def download_tracks(self):
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
                yield index+1, track_name

        self.move_output_folder(temp_directory.name)
        temp_directory.cleanup()
    

    def download(self, link, name_track, output_folder):
        run([f"spotify_dl -l '{link}' -o {output_folder}"], shell=True, stdout=DEVNULL)
        return name_track, link


    def move_output_folder(self, temp_directory):
        for directory in listdir(temp_directory):
            full_path = join(temp_directory, directory)
            for file in listdir(full_path):
                if file.endswith('.mp3'):
                    path_file = join(full_path, file)
                    copy(path_file, self.__output_folder)
    

    def check_existence(self):
        result = False
        result_query = Playlist.select().where(Playlist.link == self.__link)
        if result_query:
            result = True

        return result
    

    def save_playlist(self):
        if not self.check_existence():
            playlist_id = Playlist.create(name=get_playlist_name(self.__link), link=self.__link)
        else:
            result_query = Playlist.select().dicts().where(Playlist.link == self.__link)
            for line in result_query:
                playlist_id = line.get('id')

        return playlist_id

    
    def save_track(self, playlist_id, name, link):
        Track.create(playlist_id=playlist_id, name=name, link=link)


    def download_all(self):
        Track.delete().execute()
    
    
    def exist_track(self, playlist_id, name, link):
        result = False
        result_query = Track.select().where(Track.playlist_id == playlist_id, Track.name == name, Track.link == link)
        if result_query:
            result = True

        return result
    

    def get_number_tracks(self):
        result = []
        for track in self.__all_tracks:
            url = track.get('url')
            name = track.get('name')
            if not self.exist_track(self.__playlist_id, name, url):
                result.append(track)

        return len(result)