import json
import datetime
from os import path


def entry(name, language, poster_link, genres, id_, search_results):
    today = datetime.datetime.now().strftime('%d-%m-%Y')
    file_name = r"D:\shimul\Remote Assistant\remote_new_download\json_log"+"\\"+ f"{str(today)}.json"
    if path.exists(file_name) is False:
        file = open(file_name, "w")
        file.write("[]")
        file.close()
    file = json.load(open(file_name))
    file.append({"name": name, "language": language,
                 "poster_link": poster_link, "genres": genres, "id": id_, "search_results": search_results})
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(file, f, ensure_ascii=False, indent=4)


def downloaded(title):
    file_name = r"D:\shimul\Remote Assistant\remote_new_download\downloaded.json"
    if path.exists(file_name) is False:
        file = open(file_name, "w")
        file.write("[]")
        file.close()
    file = json.load(open(file_name))

    file.append(title)

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(file, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    entry("name", 'language', "poster_link", 'genres', 'id_')
