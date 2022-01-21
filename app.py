from flask import Flask
from flask import request
from flask_cors import CORS
from guessit import guessit
from movie_poster import Imdb_search
import math

app = Flask(__name__, static_url_path="/static")

CORS(app)


@app.route("/")
def home():
    return "you are good to go."


@app.route("/movieCode")
def movie_code():
    code = '[fluid-player video="-_-" vast_file="vast.xml"  vtt_file="thumbs.vtt" vtt_sprite="thumbs.jpg" layout="default"]\n<hr />\n<a class="alignnone" title="-_-" href="-_-"><img class="aligncenter wp-image-244 size-medium" src="http://circleftp.net/download.png" alt="Dwn Ico" width="300" height="64" /></a>'
    return code


@app.route("/TvSeires")
def tv_series():
    try:
        tv_series_name = request.args.get("name")
        tv_series_seasonfrom = int(request.args.get("seasonfrom"))
        tv_series_seasonto = int(request.args.get("tv_series_seasonto"))
        tv_series_EpisodeParSeason = int(request.args.get("tvEpisodeParSeason"))
        series_pub_code = "[su_tabs]"
        for season in range(tv_series_seasonfrom, tv_series_seasonto + 1):
            series_pub_code += f'\n[su_tab title="Season {str(season)}" disabled="no" anchor="" url="" target="blank" class="btnplayvid"]'
            series_pub_code += f'\n<table style="height: 247px;" width="459">'
            series_pub_code += f"\n<tr><th>Episode</th><th>Download URL</th></tr>"
            for Episode in range(1, tv_series_EpisodeParSeason + 1):
                series_pub_code += f"\n<tr><td>{tv_series_name.title()}.S{str(season)}.Episode:{str(Episode)}</td><td>Download</td></tr>"
            series_pub_code += f"\n</tbody></table>"
            series_pub_code += f"\n[/su_tab]"
        series_pub_code += f"\n[/su_tabs]"
        return series_pub_code
    except ValueError:
        return "kaj hoybona.. ke input decan? ai massage delete kore abar balo kore daika sob dan.. "


def get_keywords(title, year=""):
    keywords = ""
    for key in title.split(" "):
        keywords += key + ","
    keywords += title.replace("a", "e", 2) + ","
    keywords += title + " " + str(year) + ","
    keywords += title.replace("e", "a", 2) + ","
    keywords += title.replace(" ", "-") + ","
    keywords += title.replace(",", " ") + ","
    return keywords


@app.route("/GetTag")
def GetTag():
    try:
        movie_full_title = request.args.get("title")
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
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@app.route("/start", methods=["GET"])
def start():
    start_server()
    return "Starting the Server!"


@app.route("/imdb")
def imdb_search():
    try:
        movie_title = request.args["title"]
        movie_name, movie_year = (
            guessit(movie_title)["title"],
            guessit(movie_title)["year"],
        )
        search = Imdb_search(movie_name, str(movie_year))
        poster_and_genres = {
            "poster": search.get_poster(),
            "genres": search.get_genres(),
        }
        return poster_and_genres
    except:
        poster_and_genres = {
            "poster": "Movie Title required for this",
            "genres": "Movie Title required for this",
        }
        return poster_and_genres


app.run(host="0.0.0.0", port=5555, debug=True)
