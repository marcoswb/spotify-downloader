from subprocess import run, DEVNULL
import concurrent.futures
from PySide6.QtCore import QObject, Signal
from tempfile import TemporaryDirectory
from shutil import copy
from os import listdir

from utils.functions import *

class Download(QObject):
    finished = Signal()
    progress = Signal(dict)

    def init(self, link, output_folder):
        self.__link = link
        self.__output_folder = output_folder
        self.__all_tracks = get_link_tracks(self.__link)
        self.__percent_update = (100 / len(self.__all_tracks))
        export_environment_variables()


    def download_tracks(self):
        temp_directory = TemporaryDirectory()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []

            for track in self.__all_tracks:
                url = track.get('url')
                name = track.get('name')
                futures.append(executor.submit(self.download, link=url, name_track=name, output_folder=temp_directory.name))

            for index, future in enumerate(concurrent.futures.as_completed(futures)):
                track_name = future.result()
                self.progress.emit({'percent':self.__percent_update * index, 'track_name': track_name})

        self.move_output_folder(temp_directory.name)
        temp_directory.cleanup()
        self.finished.emit()
    

    def download(self, link, name_track, output_folder):
        run([f"spotify_dl -l '{link}' -o {output_folder}"], shell=True, stdout=DEVNULL)
        return name_track


    def move_output_folder(self, temp_directory):
        for directory in listdir(temp_directory):
            full_path = os.path.join(temp_directory, directory)
            for file in listdir(full_path):
                if file.endswith('.mp3'):
                    path_file = os.path.join(full_path, file)
                    copy(path_file, self.__output_folder)