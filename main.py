from utils.functions import *
from utils.Download import Download
from models.init_db import create_tables

class Main():

    def init(self):
        """
        Perguntar link da para donwload e iniciar download
        """
        donwload_link = input_user('Informe o link de uma musica, album ou playlist')
        output_folder = get_output_directory()
        
        self.download(donwload_link, output_folder)


    def download(self, donwload_link, output_folder):
        """
        Realizar donwload das músicas
        """
        self.worker = Download(donwload_link, output_folder)
        
        if self.worker.exists():
            response = input_user('Essa playlist já foi baixada uma vez, deseja somente atualizá-la? (S/N)', limit_response=['S', 'N'])
            
            if response == 'S':
                if self.worker.is_updated():
                    print('Essa playlist já está atualizada!')
            else:
                self.worker.download_all()

        for index, total_tracks, track in self.worker.download_tracks():
            print(f'{index}/{total_tracks} {track} - OK')


if __name__ == '__main__':
    create_tables()
    
    clean_screen()
    app = Main()
    app.init()
