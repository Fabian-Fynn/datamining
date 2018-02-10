import os
import sys
import json
import ast

import helpers

dir = os.path.dirname(__file__)
reload(sys)
sys.setdefaultencoding('utf8')

covered_top_tracks_artists_file_path = os.path.join(
    dir, "../../data/prepared/covered_top_tracks_artists.txt")
if not os.path.exists(covered_top_tracks_artists_file_path):
    open(covered_top_tracks_artists_file_path, 'a').close()
artists_with_fetched_tracks_file_path = os.path.join(
    dir, "../../data/prepared/artists_with_fetched_tracks.txt")
if not os.path.exists(artists_with_fetched_tracks_file_path):
    open(artists_with_fetched_tracks_file_path, 'a').close()

artist_amount = 2000
counter = 0
covered_artists = []
artists = []

covered_top_tracks_artists_file = open(
    covered_top_tracks_artists_file_path, 'r')
for line in covered_top_tracks_artists_file:
    covered_artists.append(line.strip())
covered_top_tracks_artists_file.close()
covered_top_tracks_artists_file = open(
    covered_top_tracks_artists_file_path, 'a')

artists_with_fetched_tracks_file = open(
    artists_with_fetched_tracks_file_path, 'a')

artist_info_file = open(os.path.join(
    dir, "../../data/prepared/artist_info.txt"), "r")
for line in artist_info_file:
    line = ast.literal_eval(line)
    artists.append({
        "name": line["name"],
        "id": line["id"]
    })
artist_info_file.close()

covered_artists_amount = len(covered_artists)

helpers.startProgress(
    "  Fetching top tracks of next {0} Artists ".format(artist_amount), "  Artists covered so far: {0}".format(str(covered_artists_amount)))

for artist in artists:
    if counter >= artist_amount:
        break

    artist_name = artist["name"]

    if artist["name"] in covered_artists:
        covered_artists.remove(artist["name"])
        continue
    artist_id = artist["id"]

    url = helpers.get_spotify_api_url(
        "artists", query=artist_id, query_type="top-tracks")

    raw = helpers.make_spotify_api_call(url)
    if not raw:
        break
    elif type(raw) == type(123):
        print "Error: " + str(raw)
        break

    data = json.loads(raw.read())
    tracks = []
    for track in data["tracks"]:
        condensed_track = {
            "name": track["name"],
            "popularity": track["popularity"],
            "explicit": track["explicit"],
            "id": track["id"]
        }
        tracks.append(condensed_track)

    artist_with_tracks = {
        "artist": {
            "name": artist_name,
            "id": artist_id
        },
        "top-tracks": tracks
    }

    artists_with_fetched_tracks_file.write("%s\n" % artist_with_tracks)
    covered_top_tracks_artists_file.write("%s\n" % artist_name)
    counter += 1

    progress = ((counter + 0.0) / artist_amount) * 100
    helpers.progress(progress)

covered_artists_amount += counter
helpers.endProgress("  Artists covered: " + str(covered_artists_amount))
