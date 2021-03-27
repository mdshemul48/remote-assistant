import json
from guessit import guessit
import datetime
from bs4 import BeautifulSoup
import requests
from difflib import SequenceMatcher
import re
from threading import Thread
from time import sleep


def search_movies(movie, year):
    search_movies = requests.get(
        "http://circleftp.net", params={"s": movie}).content
    soup = BeautifulSoup(search_movies,  "html.parser")
    all_articles = soup.findAll("article")
    data_of_all_movie_or_tv = []
    for article in all_articles:
        name = article.find(
            "h3", class_="entry-title").text.strip()

        link = article.find(
            "h3", class_="entry-title").find("a").get("href")

        try:
            title = guessit(name)
        except:
            continue
        try:
            title_name = title["title"]
            try:
                title_year = title["year"]
            except:
                continue

            data_of_all_movie_or_tv[f"{title_name.lower()} {title_year}"] = {
                name: link}
        except:
            continue

        match_ratio = SequenceMatcher(None, title_name, movie).ratio() * 100
        if match_ratio >= 50:
            if title_year == year:
                return "found"
            else:
                data_of_all_movie_or_tv.append({"name": name, "link": link})
    return data_of_all_movie_or_tv


if __name__ == "__main__":
    bal = search_movies("kick", 2043)
    if type(bal) == str:
        print("movie found")
    elif type(bal) == list:
        print(bal)
        print("movie not found")
