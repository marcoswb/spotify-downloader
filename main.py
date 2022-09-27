from utils.functions import *
from utils.Download import Download
from models.init_db import create_tables

class Main():

    def init(self):
        """
        Perguntar link da playlist e confirmar caminho de saída
        """
        while True:
            playlist_link = input('Informe o link da playlist -> ')
            output_folder = input('Informe a pasta de saída -> ')

            if is_null(playlist_link):
                print('Preencha a campo de link da playlist!')
            elif is_null(output_folder):
                print('Preencha a campo de pasta de saída!')
            else:
                break

        self.download(playlist_link, output_folder)


    def download(self, playlist_link, output_folder):
        self.worker = Download()
        self.worker.init(playlist_link, output_folder)
        number_tracks = self.worker.get_number_tracks()

        if self.worker.check_existence():
            response = input('Essa playlist já foi baixada uma vez, deseja somente atualizá-la? (S/N)')
            
            if response.upper() == 'S':
                self.worker.only_update()

        for index, track in self.worker.download_tracks():
            print(f'{index}/{number_tracks} {track} - OK')


if __name__ == '__main__':
    create_tables()
    
    app = Main()
    app.init()
