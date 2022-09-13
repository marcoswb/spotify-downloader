from sys import exit
from dotenv import load_dotenv
from os import getenv, system
from PySide6.QtWidgets import QApplication, QMainWindow
from resources.screen import UiMainWindow
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from utils.functions import *
from utils.components import *

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__window = UiMainWindow()
        self.__window.setup_ui(self)
        self.link_components()

        load_dotenv()

        client_id = getenv('SPOTIFY_CLIENT_ID')
        client_secret = getenv('SPOTIFY_CLIENT_SECRET')

        self.spotify_client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        ))

    

    def link_components(self):
        """
        Vincular componentes da interface
        """
        self.__textbox_playlist_link = self.__window.textbox__playlist_link
        self.__listview_downloaded_music = self.__window.listview__downloaded_music
        self.__button_download = self.__window.button__download
        self.__progressbar_status_download = self.__window.progressbar__status_download

        self.__button_download.clicked.connect(self.download)
    

    def init(self):
        """
        Renderizar janela
        """
        self.__listview_downloaded_music.clear()
        self.__progressbar_status_download.setValue(0)
        self.show()


    def download(self):
        playlist_link = self.__textbox_playlist_link.text()
        output_folder = '~/Downloads'

        if is_null(playlist_link):
            error_message(self, 'Preencha a campo de link da playlist!')
            self.__textbox_playlist_link.clear()
            self.__textbox_playlist_link.setFocus()
            return

        for track in self.spotify_client.playlist_tracks(playlist_link)['items']:
            url = track['track']['external_urls']['spotify']
            print(url)
            system(f"spotify_dl -l '{url}' -o {output_folder}")

        show_message(self, 'Processo Finalizado', 'FIM.')
    

if __name__ == '__main__':
    app = QApplication([])
    
    window = Main()
    window.init()

    exit(app.exec())