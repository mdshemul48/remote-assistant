from flask import Flask, render_template
from flask import request
from flask_cors import CORS
from guessit import guessit
from movie_poster import Imdb_search
import json
from datetime import date, timedelta
from qbittorrent import Client
import glob
import math

app = Flask(__name__, static_url_path="/static")

CORS(app)


def convert_sizes(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s%s" % (s, size_name[i])


@app.route('/movieCode')
def movie_code():
    code = '[fluid-player video="-_-" vast_file="vast.xml"  vtt_file="thumbs.vtt" vtt_sprite="thumbs.jpg" layout="default"]\n<hr />\n<a class="alignnone" title="-_-" href="-_-"><img class="aligncenter wp-image-244 size-medium" src="http://circleftp.net/download.png" alt="Dwn Ico" width="300" height="64" /></a>'
    return code


@app.route('/TvSeires')
def tv_series():
    try:
        tv_series_name = request.args.get('name')
        tv_series_seasonfrom = int(request.args.get('seasonfrom'))
        tv_series_seasonto = int(request.args.get('tv_series_seasonto'))
        tv_series_EpisodeParSeason = int(
            request.args.get('tvEpisodeParSeason'))
        series_pub_code = "[su_tabs]"
        for season in range(tv_series_seasonfrom, tv_series_seasonto+1):
            series_pub_code += f'\n[su_tab title="Season {str(season)}" disabled="no" anchor="" url="" target="blank" class="btnplayvid"]'
            series_pub_code += f'\n<table style="height: 247px;" width="459">'
            series_pub_code += f'\n<tr><th>Episode</th><th>Download URL</th></tr>'
            for Episode in range(1, tv_series_EpisodeParSeason+1):
                series_pub_code += f'\n<tr><td>{tv_series_name.title()}.S{str(season)}.Episode:{str(Episode)}</td><td>Download</td></tr>'
            series_pub_code += f"\n</tbody></table>"
            series_pub_code += f"\n[/su_tab]"
        series_pub_code += f"\n[/su_tabs]"
        return series_pub_code
    except ValueError:
        return "kaj hoybona.. ke input decan? ai massage delete kore abar balo kore daika sob dan.. "


def get_keywords(title, year=""):
    keywords = ""
    for key in title.split(' '):
        keywords += key+","
    keywords += title.replace("a", "e", 2)+","
    keywords += title+" "+str(year)+","
    keywords += title.replace("e", "a", 2)+","
    keywords += title.replace(" ", "-")+","
    keywords += title.replace(",", " ")+","
    return keywords


@app.route('/GetTag')
def GetTag():
    try:
        movie_full_title = request.args.get('title')
        title = guessit(movie_full_title)["title"]
        year = guessit(movie_full_title)["year"]
        keywords = get_keywords(title, year)
        return keywords
    except:
        return "Title deya ni.. ai massage remove kore title deya then add tag a click koran.."


@app.route("/filecode")
def filecode():
    code = '<hr />\n<a class="alignnone" title="-_-" href="-_-"><img class="aligncenter wp-image-244 size-medium" src="http://circleftp.net/download.png" alt="Dwn Ico" width="300" height="64" /></a>'
    return code


def start_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/start', methods=['GET'])
def start():
    start_server()
    return 'Starting the Server!'


@app.route('/imdb')
def imdb_search():
    try:
        movie_title = request.args["title"]
        movie_name, movie_year = guessit(
            movie_title)["title"], guessit(movie_title)["year"]
        search = Imdb_search(movie_name, str(movie_year))
        poster_and_genras = {
            "poster": search.get_poster(), "genres": search.get_genres()}
        return poster_and_genras
    except:
        poster_and_genras = {"poster": "Movie Title required for this",
                             "genres": "Movie Title required for this"}
        return poster_and_genras


def get_upload_data():
    file = json.load(open("data.json"))
    today = date.today().strftime("%d/%m/%Y")
    try:
        today_uploaded = file["daily_report"][today]["uploaded"]
    except:
        today_uploaded = 0

    yesterday = (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")
    try:
        yesterday_uploaded = file["daily_report"][yesterday]["uploaded"]
    except:
        yesterday_uploaded = 0

    all_uploaded = 0
    all_deleted = 0

    for day in file["daily_report"]:
        all_uploaded += file["daily_report"][day]["uploaded"]
        all_deleted += file["daily_report"][day]["deleted"]
    all_downloading = []
    try:
        now_downloading = Client(
            "http://202.136.91.166:8080/")
        now_downloading.login("Awesome", "Awesome")
        torrents = now_downloading.torrents()
        now_downloading = 0
        block_list = ["Mohsin", "", "WWE", "Not Listed", ".Awesome"]
        for torrent in torrents:
            if torrent["category"] not in block_list:
                title = torrent["name"]
                lenguage = torrent["category"]
                progress = int(torrent["progress"]*100)
                status = torrent["state"]
                size = convert_sizes(torrent["size"])
                speed = convert_sizes(torrent["dlspeed"])
                all_downloading.append(
                    {"title": title, "lenguage": lenguage, "progress": progress, "status": status, "size": size, "speed": speed})
                now_downloading += 1

    except:
        now_downloading = 0
    return {"today_uploaded": today_uploaded, "yesterday_uploaded": yesterday_uploaded, "all_uploaded": all_uploaded, "all_deleted": all_deleted, "now_downloading": now_downloading, "all_downloading": all_downloading}


@app.route('/', methods=['GET'])
def log():

    file = open("log.txt", "r")
    all_log = file.read().split("\n")
    logs = []
    if len(all_log) >= 100:
        lenth = len(all_log)-100
        index = len(all_log)
    else:
        lenth = 0
        index = len(all_log)

    while lenth != index:
        logs.append(all_log[index-1])
        index -= 1

    return render_template("index.html", data={"logs": logs, "upload_data": get_upload_data()})


@app.route('/downloads')
def download_history():
    try:
        file_title = request.args.get('view')
        file_path = r"D:\shimul\Remote Assistant\remote_new_download\json_log" + \
            "\\"+file_title+".json"
        deta = json.load(open(file_path))

        return render_template("json_report.html", data=deta, title=file_title)
    except:
        path = r"D:\shimul\Remote Assistant\remote_new_download\json_log"
        all_downloads = []
        for downloads in glob.glob(
                glob.escape(path)+"\*", recursive=True):
            length = len(json.load(open(downloads)))
            file_title = downloads.replace(
                path, "").replace("\\", "").split(".")[0]
            all_downloads.append({"title": file_title, "length": length})

        return render_template("Report.html", data=all_downloads)


app.run(host='0.0.0.0', port=5555, debug=True)
