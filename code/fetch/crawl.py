import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import config
dir = os.path.dirname(__file__)

client_id = "af9cb4f497cb4b52a6a9ec851f22caa5"
client_secret = "a9df8a86bd9b43b0b00bb2c0b253023f"
grant_type = 'client_credentials'

with open(os.path.join(dir, "../../data/fetched/artists_charts.txt")) as f:
    access_token = f.read()

# body_params = {'grant_type': grant_type}
# url = 'https://api.spotify.com/v1/search?q=tania%20bowra&type=artist'

# response=requests.post(url, data=body_params, auth = (client_id, client_secret))
# print response

# name = "Metallica"

spotify = spotipy.Spotify()

# client_credentials_manager = SpotifyClientCredentials()
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# playlists = sp.user_playlists('spotify')
# while playlists:
#     for i, playlist in enumerate(playlists['items']):
#         print("%4d %s %s" %
#               (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#     if playlists['next']:
#         playlists = sp.next(playlists)
#     else:
#         playlists = None

# results = spotify.search(q='artist:' + name, type='artist')
result = spotify.search('Radiohead')

print result
