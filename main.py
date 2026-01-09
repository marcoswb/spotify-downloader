from utils.functions import *
from utils.Download import Download
from models.init_db import create_tables
from models.Playlist import Playlist

class Main:

    def __init__(self):
        self.__update_playlists = None

    def init(self):
        """
        Perguntar link da para donwload e iniciar download
        """
        print('1 - Atualizar todas as playlists')
        print('2 - Baixar novas playlists')
        option = int(input_user('Escolha uma opção para continuar', limit_response=['1', '2']))

        downloads = []
        if option == 1:
            self.__update_playlists = True

            result_query = Playlist.select(Playlist.link).dicts()
            downloads.extend([aux.get('link') for aux in list(result_query)])
        else:
            download_link = input_user('Informe o link de uma musica, album ou playlist')
            downloads.append(download_link)

            while download_link:
                download_link = input_user('Informe mais um link de uma musica, album ou playlist ou tecle ENTER para iniciar os downloads', allow_empty=True)
                if download_link:
                    downloads.append(download_link)
                else:
                    break

        output_folder = get_output_directory()
        for download_link in downloads:
            self.download(download_link, output_folder)


    def download(self, download_link, output_folder):
        """
        Realizar donwload das músicas
        """
        worker = Download(download_link, output_folder)
        
        if worker.exists():
            if self.__update_playlists is None:
                response = input_user('Essa playlist já foi baixada uma vez, deseja somente atualizá-la? (S/N)', limit_response=['S', 'N'])
                if response == 'S':
                    self.__update_playlists = True
                else:
                    self.__update_playlists = False

            if self.__update_playlists:
                if worker.is_updated():
                    name = worker.get_playlist_name()
                    print(f'"{name}" já está atualizada!')
            else:
                worker.download_all()

        for index, total_tracks, track in worker.download_tracks():
            print(f'{index}/{total_tracks} {track} - OK')


if __name__ == '__main__':
    create_tables()
    
    clean_screen()
    app = Main()
    app.init()
