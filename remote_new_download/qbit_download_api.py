from qbittorrent import Client


class Qbit_download:
    def __init__(self, link_of_qbit, username, password):
        self.qbit = Client(link_of_qbit)
        self.qbit.login(username, password)

    def download_movie(self, link, download_path, language):
        self.qbit.download_from_link(
            link, savepath=download_path+"\\"+language, category=language)

    def normal_download(self, link, location, category):
        self.qbit.download_from_link(
            link, savepath=location, category=category)

    def get_all_downloading(self,):
        all_downloading_torrent = self.qbit.torrents()
        all_downloading_torrent_title = []
        for torrent in all_downloading_torrent:
            all_downloading_torrent_title.append(torrent["name"])
        return all_downloading_torrent_title
