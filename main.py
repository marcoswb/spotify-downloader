from sys import exit
from PySide6.QtWidgets import QApplication, QMainWindow
from resources.screen import UiMainWindow
from PySide6.QtCore import QThread

from utils.functions import *
from utils.components import *
from utils.Download import Download

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
    

    def init(self):
        """
        Renderizar janela
        """
        self.__listview_downloaded_music.clear()
        self.__progressbar_status_download.setValue(0)
        self.show()


    def download(self):
        self.__progressbar_status_download.setValue(0)
        self.__textbox_playlist_link.setText('https://open.spotify.com/playlist/321aOHCg49aXIvEk6YO6OR?si=31e517d850914f94&pt=b729683a372e97ad519b41aaf04c1f3b')
        playlist_link = self.__textbox_playlist_link.text()
        output_folder = '~/Downloads'

        if is_null(playlist_link):
            error_message(self, 'Preencha a campo de link da playlist!')
            self.__textbox_playlist_link.clear()
            self.__textbox_playlist_link.setFocus()
            return

        self.thread = QThread()
        self.worker = Download()
        self.worker.init(playlist_link, output_folder)
        
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.download_tracks)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.update_progressbar)
        self.worker.finished.connect(self.finish_process)
        
        self.thread.start()

    
    def update_progressbar(self, progress_value):
        self.__progressbar_status_download.setValue(progress_value)

    def finish_process(self):
        show_message(self, 'Processo Finalizado', 'FIM.')
        self.__progressbar_status_download.setValue(100)


if __name__ == '__main__':
    app = QApplication([])
    
    window = Main()
    window.init()

    exit(app.exec())