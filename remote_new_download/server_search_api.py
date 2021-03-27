import glob
from guessit import guessit
from tqdm import tqdm
from difflib import get_close_matches


def scan_our_movie_dir(list_of_movie_dir):
    our_movies = {}
    for movie_dir in list_of_movie_dir:
        for movies_year in glob.glob(glob.escape(movie_dir) + r"\*", recursive=True):
            for movies in glob.glob(glob.escape(movies_year) + r"\*", recursive=True):
                movie = movies.replace(movies_year, "").replace("\\", "")
                movie_info_with_guessit = guessit(movie)
                try:
                    movie_name = movie_info_with_guessit["title"]
                except:
                    continue
                try:
                    movie_year = movie_info_with_guessit["year"]
                except:
                    continue
                our_movies[movie_name.lower()+" "+str(movie_year)
                           ] = {"name": movie_name, "year": movie_year, "full_title": movie}
    return our_movies


def search_movie(our_movies, movie_name, movie_year):
    search = movie_name.lower()+" "+str(movie_year)
    if search in our_movies:
        return False
    else:
        all_the_close_matches_movie = get_close_matches(
            search, our_movies.keys(), n=3, cutoff=0.7)
        for movie in all_the_close_matches_movie:
            if str(our_movies[movie]["year"]) == str(movie_year):
                return False
            else:
                return True
    return True


def check_movie_in_server(our_movies, new_movie):
    for movie in new_movie:
        movie_details = guessit(movie)
        try:
            movie_title = movie_details["title"]
        except:
            continue
        try:
            movie_year = movie_details["year"]
        except:
            continue
        if search_movie(our_movies, movie_title, movie_year) and new_movie[movie]["size"] < 5.0:
            print(movie_title, movie_year, search_movie(our_movies,
                                                        movie_title, movie_year),  new_movie[movie]["size"])


if __name__ == '__main__':
    list_of_movie_dir = [r"V:\English & Foreign Dubbed Movies",
                         r"V:\English Movies",
                         r"V:\Foreign Language Movies",
                         r"W:\Animation Movies",
                         r"X:\Hindi Movies",
                         r"X:\Tamil Telugu & Others", ]
    our_movies = scan_our_movie_dir(list_of_movie_dir)
