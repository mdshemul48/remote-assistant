from guessit import guessit


def full_name_to_onlyName_and_year(full_name):
    full_title = guessit(full_name)
    name, year = full_title["title"].lower().replace("_", " ").replace(
        ":", " ").replace(".", " "),  full_title["year"]
    return name, year
