import os

import secrets

dir = os.path.dirname(__file__)


LAST_FM = {
    "API_URL": "http://ws.audioscrobbler.com/2.0/?",
    "API_KEY": secrets.LAST_FM_API_KEY,
    "API_METHODS": [
        'method=user.gettopalbums',
        'method=user.gettopartists',
        'method=user.gettoptags',
        'method=user.gettoptracks',
    ],
    'LIMIT': 'limit=500',
    'FORMAT': 'format=json',
}

SPOTIFY = {
    "API_URL": "https://api.spotify.com/v1/",
    "CLIENT_ID": "af9cb4f497cb4b52a6a9ec851f22caa5",
    "CLIENT_SECRET": "a9df8a86bd9b43b0b00bb2c0b253023f",
    "ACCESS_TOKEN": ""
}


def read_sp_token():
    with open(os.path.join(dir, "./spotify_access_token.txt"), "r") as f:
        token = f.read()
        SPOTIFY["ACCESS_TOKEN"] = token
        return token


def set_access_token(token):
    SPOTIFY["ACCESS_TOKEN"] = token


read_sp_token()
