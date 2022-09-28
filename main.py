from utils.functions import *
from utils.Download import Download
from models.init_db import create_tables

class Main():

    def init(self):
        """
        Perguntar link da playlist e confirmar caminho de saída
        """
        playlist_link = input_user('Informe o link da playlist')
        output_folder = input_user('Informe a pasta de saída', check_is_dir=True)

        self.download(playlist_link, output_folder)


    def download(self, playlist_link, output_folder):
        """
        Realizar donwload das músicas
        """
        self.worker = Download()
        self.worker.init(playlist_link, output_folder)
        number_tracks = self.worker.get_number_tracks()

        if self.worker.check_existence():
            response = input_user('Essa playlist já foi baixada uma vez, deseja somente atualizá-la? (S/N)', limit_response=['S', 'N'])
            
            if response == 'S':
                self.worker.only_update()

        for index, track in self.worker.download_tracks():
            print(f'{index}/{number_tracks} {track} - OK')


if __name__ == '__main__':
    create_tables()
    
    app = Main()
    app.init()
