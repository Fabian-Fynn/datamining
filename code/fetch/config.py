import secrets

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
