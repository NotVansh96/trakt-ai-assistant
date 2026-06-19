import requests

from config import OMDB_API_KEY


def get_poster(imdb_id):

    try:

        response = requests.get(
            "https://www.omdbapi.com/",
            params={
                "apikey": OMDB_API_KEY,
                "i": imdb_id
            },
            timeout=10
        )

        data = response.json()

        poster = data.get("Poster")

        if not poster or poster == "N/A":
            return None

        return poster

    except Exception:
        return None
    

def get_poster_by_title(title):

    url = "https://www.omdbapi.com/"

    params = {
        "apikey": OMDB_API_KEY,
        "t": title
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        if data.get("Poster") and data["Poster"] != "N/A":
            return data["Poster"]

    except Exception:
        pass

    return None