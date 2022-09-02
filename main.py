from sys import exit
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from resources.screen import UiMainWindow

from utils.functions import *
from utils.components import *

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__window = UiMainWindow()
        self.__window.setup_ui(self)
        self.link_components()
    

    def link_components(self):
        """
        Vincular componentes da interface
        """
        self.__textbox_playlist_link = self.__window.textbox__playlist_link
        self.__listview_downloaded_music = self.__window.listview__downloaded_music
        self.__button_download = self.__window.button__download
        self.__progressbar_status_download = self.__window.progressbar__status_download

        self.__button_download.clicked.connect(self.download)
        pass
    

    def init(self):
        """
        Renderizar janela
        """
        self.__listview_downloaded_music.clear()
        self.__progressbar_status_download.setValue(0)
        self.show()


    def download(self):
        playlist_link = self.__textbox_playlist_link.text()

        if is_null(playlist_link):
            error_message(self, 'Preencha a campo de link da playlist!')
            self.__textbox_playlist_link.clear()
            self.__textbox_playlist_link.setFocus()


    

if __name__ == '__main__':
    app = QApplication([])
    
    window = Main()
    window.init()

    exit(app.exec())