import imdb
from difflib import SequenceMatcher

class Imdb_search:
    ia = imdb.IMDb()

    def __init__(self,movie_name, movie_year: str):
        search = self.ia.search_movie(movie_name)
        for movie in search:
            searched_name = str(movie)
            searched_year = str(movie["year"])
            if int(SequenceMatcher(None, movie_name+" "+movie_year, searched_name+" "+searched_year).ratio()*100) >= 70:
                if movie_year == searched_year:
                    self.searched_id = movie.movieID
                    self.raw_poster_link = movie['cover url']
                    break

    def get_genres(self):
        try:
            series = self.ia.get_movie(self.searched_id)
            genre = series.data['genres']
            genres = ""
            for i in genre:
                genres = f"{i},{genres}"
            return genres
        except AttributeError:
            return "Genres Not Found in IMDB"
    
    def get_poster(self):
        try:
            final_poster = self.raw_poster_link.split("._", 1)[0]+ "._V1_.jpg"
            return final_poster
        except AttributeError:
            return "Poster Not Found in IMDB"


if __name__ == '__main__':
    api = Imdb_search("Deadpool", "2016")
    print(api.get_genres(), api.get_poster())
