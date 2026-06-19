import json
import requests
import os

from config import (
    TRAKT_CLIENT_ID,
    TRAKT_CLIENT_SECRET
)

TOKEN_FILE = "tokens.json"


def save_tokens(token_data):
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=4)


def load_tokens():
    try:
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def exchange_code_for_token(code):
    url = "https://api.trakt.tv/oauth/token"

    payload = {
        "code": code,
        "client_id": TRAKT_CLIENT_ID,
        "client_secret": TRAKT_CLIENT_SECRET,
        "redirect_uri": "http://localhost:8501",
        "grant_type": "authorization_code"
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        token_data = response.json()
        save_tokens(token_data)
        return token_data

    return None


def get_access_token():

    token = os.getenv(
        "TRAKT_ACCESS_TOKEN"
    )

    if token:
        return token

    tokens = load_tokens()

    if "access_token" in tokens:
        return tokens["access_token"]

    return None


def get_headers():
    token = get_access_token()

    return {
        "Content-Type": "application/json",
        "trakt-api-version": "2",
        "trakt-api-key": TRAKT_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }


def get_profile():
    response = requests.get(
        "https://api.trakt.tv/users/settings",
        headers=get_headers()
    )

    if response.status_code == 200:
        return response.json()

    return None


def get_user_stats():
    profile = get_profile()

    if not profile:
        return None

    username = profile["user"]["username"]

    response = requests.get(
        f"https://api.trakt.tv/users/{username}/stats",
        headers=get_headers()
    )

    if response.status_code == 200:
        return response.json()

    return None


def get_watch_history():
    all_items = []
    page = 1

    while True:

        response = requests.get(
            f"https://api.trakt.tv/sync/history?page={page}&limit=100",
            headers=get_headers()
        )

        if response.status_code != 200:
            break

        items = response.json()

        if not items:
            break

        all_items.extend(items)

        page += 1

    return all_items  


def get_ratings():
    all_items = []
    page = 1

    while True:

        response = requests.get(
            f"https://api.trakt.tv/sync/ratings?page={page}&limit=100",
            headers=get_headers()
        )

        if response.status_code != 200:
            break

        items = response.json()

        if not items:
            break

        all_items.extend(items)

        page += 1

    return all_items    


def get_watchlist():
    response = requests.get(
        "https://api.trakt.tv/sync/watchlist",
        headers=get_headers()
    )

    if response.status_code == 200:
        return response.json()

    return []