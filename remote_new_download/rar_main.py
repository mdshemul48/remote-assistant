from rarbg import download, getMegnet
from search_api import search_movies
from server_search_api import scan_our_movie_dir, search_movie
from convart_sys import full_name_to_onlyName_and_year
from qbit_download_api import Qbit_download
from imdb__ import *
from save_data import entry, downloaded
import json
import time
from datetime import datetime


def printing(massage):
    status_time = datetime.now()
    status_time = status_time.strftime("%I:%M:%S %p %d/%m/%Y")
    try:
        log_line = f"[{status_time}] DownloadBot: {massage}"
    except:
        log_line = f"[{status_time}] {massage}"
    file = open(r"D:\shimul\Remote Assistant\log.txt", "a")
    # print(log_line)
    file.write(f"{log_line}\n")


def main():
    printing("Starting The Script")
    qbit = Qbit_download(
        "http://202.136.91.166:8080/", "Awesome", "Awesome")
    downlaoding_in_torrent = {}
    for movie in qbit.get_all_downloading():
        try:
            name, year = full_name_to_onlyName_and_year(movie)
            downlaoding_in_torrent[name+" "+str(year)] = {"year": year}
        except:
            continue
    list_of_movie_dir = [r"Q:\.uploading 1tb",
                         r"D:\shimul\super power",
                         r"D:\shimul\Do not open",
                         r"Q:\.uploading 1tb\ready to publish",
                         r"Q:\.uploading 1tb\incoming"]

    my_download = scan_our_movie_dir(list_of_movie_dir)
    printing("scan done")
    all_torrent = download(
        f"https://rarbgmirror.org/torrents.php?category=44%3B54")
    for torrent in all_torrent["data"]:
        # geting torrent and search the movie
        full_title = torrent["title"]

        title, year = full_name_to_onlyName_and_year(full_title)

        if full_title in json.load(open(r"D:\shimul\Remote Assistant\remote_new_download\downloaded.json")):
            downloaded(full_title)
            printing(f"already exist.. {full_title}")
            continue

        search_results = search_movies(title, year)
        if type(search_results) == str:
            printing(f"already exist.. {full_title}")
            continue
        if type(search_results) == list and search_movie(my_download, title, year) and search_movie(downlaoding_in_torrent, title, year) and torrent["size"] <= 5.6 and full_title not in json.load(open(r"D:\shimul\Remote Assistant\remote_new_download\downloaded.json")):
            printing(f"adding to torrent {full_title}")
            movie_id = torrent["imdb"]
            try:
                language = get_language(movie_id)
            except:
                continue
            megnet = getMegnet(torrent["href_link"])

            qbit.download_movie(
                megnet, r"D:\shimul\super power", language)
            poster = get_poster(movie_id)
            genres = get_genres(movie_id)
            downlaoding_in_torrent[title +
                                   " "+str(year)] = {"year": year}
            entry(full_title, language, poster,
                  genres, movie_id, search_results)
            downloaded(full_title)
            printing(f"added to torrent.. {full_title}")
        else:
            downloaded(full_title)
            printing(f"already exist.. {full_title}")
    printing("i'm going to sleep..")


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            printing(f"error {e}")
        time.sleep(3600)
