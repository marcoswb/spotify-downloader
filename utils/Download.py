from os import system
import concurrent.futures
from PySide6.QtCore import QObject, Signal
from time import sleep

from utils.functions import *

class Download(QObject):
    finished = Signal()
    progress = Signal(int)

    def init(self, link, output_folder):
        self.__link = link
        self.__output_folder = output_folder
        self.__all_tracks = get_link_tracks(self.__link)
        self.__percent_update = (100 / len(self.__all_tracks))


    def download_tracks(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []

            for url_track in self.__all_tracks:
                futures.append(executor.submit(self.download, link=url_track, output_folder=self.__output_folder))

            for index, future in enumerate(concurrent.futures.as_completed(futures)):
                future.result()
                self.progress.emit(self.__percent_update * index)

        self.finished.emit()
    

    def download(self, link, output_folder):
        sleep(2)
        # system(f"spotify_dl -l '{link}' -o {output_folder}")