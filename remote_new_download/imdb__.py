
from imdb import IMDb


def get_language(id_, ia=IMDb()):
    the_matrix = ia.get_movie(id_)
    return the_matrix['language'][0]


def get_poster(id_, ia=IMDb()):
    try:
        poster = ia.get_movie(id_)['cover url']
        return poster.split("._", 1)[0]+"._V1_.jpg"
    except:
        return "https://images-na.ssl-images-amazon.com/images/I/61ZYf7b266L._AC_SY741_.jpg"


def get_genres(id_, ia=IMDb()):
    try:
        series = ia.get_movie(id_)
        genre = series.data['genres']
        genres = ""
        for i in genre:
            genres = f"{i},{genres}"
        return genres
    except:
        return ""
