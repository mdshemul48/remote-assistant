from qbittorrent import Client
import os
import shutil
from time import sleep
from datetime import datetime, date
import subprocess
import glob
from log import Log


def printing(movie_uploaded, qbit, massage):
    status_time = datetime.now()
    status_time = status_time.strftime("%I:%M:%S %p %d/%m/%Y")
    try:
        log_line = f"[{status_time}] UploadBot: {massage}"
    except:
        log_line = f"[{status_time}] {massage}"
    file = open('log.txt', "a")
    # print(log_line)
    file.write(f"{log_line}\n")


class Qbit:
    def __init__(self, qbit_url, username, password):
        self.qbit = Client(qbit_url)
        self.qbit.login(username, password)

    def get_status(self):
        return self.qbit.torrents()

    def pause_torrent(self, info_hash):
        self.qbit.pause(info_hash)

    def delete_torrent(self, info_hash):
        self.qbit.delete_permanently(info_hash)


def rename_full_folder(path):
    block_list = ["txt", "exe", "nfo", "jpg", "png", "jpeg"]
    for file_path in glob.glob(glob.escape(path)+"/*", recursive=True):
        file_name = file_path.replace(path, "").replace("\\", "")
        new_name = file_name[::-1].replace("-", "###",
                                           1)[::-1].split("###")[0].replace(".", " ")
        for movie_path in glob.glob(glob.escape(file_path)+"/*", recursive=True):
            try:
                file_extension = movie_path[::-
                                            1].replace(".", "_-_", 1)[::-1].split("_-_")[1]
            except:
                continue
            file_or_folder_name = movie_path.replace(
                file_path, "").replace("\\", "")
            if file_or_folder_name == "Subs":
                shutil.rmtree(movie_path)
            elif file_extension in block_list:
                os.remove(movie_path)
        os.rename(file_path, path+"\\"+new_name)


def upload(input_folder, output_folder):
    command = f'rclone copy "{input_folder}" "{output_folder}" --ignore-existing -P'
    os.system(command)
    os.system(command)


def moving_to_temp_folder(*args):
    qbit = args[0]
    torrent = args[1]
    temp_folder = args[2]
    info_hash = torrent["hash"]
    category = torrent["category"]
    qbit.pause_torrent(info_hash)
    folder_path = torrent["content_path"]
    folder_name = torrent["content_path"][::-
                                          1].replace("\\", "$$$$$$", 1)[::-1].split("$$$$$$")[1]
    final_temp_folder = temp_folder+"\\"+category+"\\"+folder_name
    if not os.path.exists(temp_folder+"\\"+category):
        os.makedirs(temp_folder+"\\"+category)
    shutil.move(folder_path, final_temp_folder)
    return info_hash


def total_added_days(added_date: int):
    added_time = datetime.fromtimestamp(
        added_date).strftime("%Y,%m,%d").split(",")
    now_time = datetime.now().strftime("%Y,%m,%d").split(",")
    added_year, added_month, added_day = int(
        added_time[0]), int(added_time[1]), int(added_time[2])

    now_year, now_month, now_day = int(
        now_time[0]), int(now_time[1]), int(now_time[2])

    added = date(added_year, added_month, added_day)
    now = date(now_year, now_month, now_day)
    total_days = now - added
    return total_days.days


def movie_management():
    movie_uploaded = 0
    while True:
        #url, username, password = "http://202.136.89.212:8080/", "sam", ""
        #upload_location = r"V:\.uploading 1tb\yoyo"
        #temp_folder = r"F:\uploadtemp"
        log = Log("data.json")
        url, username, password = "http://202.136.91.166:8080/", "Awesome", "Awesome"
        upload_location = r"Q:\.uploading 1tb\incoming"
        temp_folder = r"D:\shimul\temporary_working_dir"
        if not os.path.exists(temp_folder):
            os.mkdir(temp_folder)
        total_uploading = 0
        working_torrent_info_hash = []
        block_list = ["Mohsin", "", "WWE", "Not Listed", ".Awesome"]

        for torrent in Qbit(url, username, password).get_status():
            if torrent["category"] in block_list:
                continue
            else:
                if torrent["progress"] == 1 and torrent["state"] != "moving" and torrent["category"] not in block_list:
                    printing(movie_uploaded, Qbit(url, username,
                                                  password), f"{str(torrent['name'])} Moving to Temp folder...")
                    total_uploading += 1
                    try:
                        info_hash = moving_to_temp_folder(
                            Qbit(url, username, password), torrent, temp_folder)
                        working_torrent_info_hash.append(info_hash)
                        log.uploaded()
                    except FileNotFoundError as error:
                        printing(movie_uploaded, Qbit(url, username, password),
                                 f"{error}.. Deleting Torrent from qbit..")
                        log.deleted()
                        Qbit(url, username, password).delete_torrent(
                            torrent["hash"])

                elif torrent["progress"] != 1 and total_added_days(torrent["added_on"]) >= 3:
                    Qbit(url, username, password).delete_torrent(
                        torrent["hash"])
                    log.deleted()
                    printing(movie_uploaded, Qbit(url, username, password),
                             f"Added Time {str(torrent['name'])} {total_added_days(torrent['added_on'])} days. Still downloading.. So deleting the torrent..")
        if len(working_torrent_info_hash) != 0:
            printing(movie_uploaded, Qbit(url, username, password),
                     f"Renaming All movies...")
            for folder in glob.glob(glob.escape(temp_folder)+"/*", recursive=True):
                rename_full_folder(folder)
            printing(movie_uploaded, Qbit(url, username, password),
                     f"Renaming Done...")

            printing(movie_uploaded, Qbit(url, username, password),
                     f"uploading {total_uploading} movies...")
            upload(temp_folder, upload_location)
            for info_hash in working_torrent_info_hash:
                Qbit(url, username, password).delete_torrent(info_hash)
                movie_uploaded += 1
            shutil.rmtree(temp_folder)
            printing(movie_uploaded, Qbit(
                url, username, password), "uploading Done...")
        printing(movie_uploaded, Qbit(url, username, password),
                 "Checking For new Movie to complete..")
        log.save()
        sleep(300)


if __name__ == "__main__":
    error_time = 0
    while True:
        try:
            movie_management()
        except Exception as ex:
            error_time += 1
            printing("", "", f"{ex}. script restarted{error_time}..")
            sleep(100)
