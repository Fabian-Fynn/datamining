import os
import sys
import json
import urllib2
import ast

import helpers

dir = os.path.dirname(__file__)
reload(sys)
sys.setdefaultencoding('utf8')
covered_artists_file_path = os.path.join(
    dir, "../../data/assist/covered_artists_features.txt")
artist_tracks_features_file_path = os.path.join(
    dir, "../../data/prepared/artist_tracks_features.txt")
artists_with_fetched_tracks_file_path = os.path.join(
    dir, "../../data/prepared/artists_with_fetched_tracks.txt")

helpers.create_file_if_not_exists(covered_artists_file_path)
helpers.create_file_if_not_exists(artist_tracks_features_file_path)

artist_amount = 10000
counter = 0

covered_artists = helpers.read_lines_from_file(covered_artists_file_path)

covered_artists_file = open(covered_artists_file_path, "a")
artist_tracks_features_file = open(artist_tracks_features_file_path, "a")

# Get all artists + tracks
artists = helpers.read_lines_from_file(
    artists_with_fetched_tracks_file_path)

covered_artists_amount = len(covered_artists)

helpers.startProgress(
    "  Fetching audio features of next {0} Artists ".format(artist_amount), "  Artists covered so far: \033[36m{0}\033[0m".format(str(covered_artists_amount)))

# loop over artists
for artist in artists:
    if counter >= artist_amount:
        break
    artist = ast.literal_eval(artist)
    artist_name = artist["artist"]["name"]
    artist_id = artist["artist"]["id"]
    track_ids = []

    if artist_name in covered_artists:
        covered_artists.remove(artist_name)
        continue

    for track in artist["top-tracks"]:
        track_ids.append(track["id"])

    # fetch audio features of artists top tracks
    query = ','.join(track_ids)
    url = helpers.get_spotify_api_url(
        "audio-features", query=query)
    raw = helpers.make_spotify_api_call(url)

    if not raw:
        break
    elif type(raw) == type(123):
        print "Error: " + str(raw)
        break

    data = json.loads(raw.read())
    tracks = []
    if len(data["audio_features"]) > 0:
        for track in data["audio_features"]:
            parameters_to_remove = ('type', 'uri', 'track_href')
            for key in parameters_to_remove:
                if key in track:
                    del track[key]

            track_info = (item for item in artist["top-tracks"]
                          if item["id"] == track["id"]).next()
            track.update(track_info)
            tracks.append(track)

        artist_with_tracks = {
            "name": artist_name,
            "id": artist_id,
            "tracks": tracks
        }
        artist_tracks_features_file.write("%s\n" % artist_with_tracks)
    covered_artists_file.write("%s\n" % artist_name)
    counter += 1

    progress = ((counter + 0.0) / artist_amount) * 100
    helpers.progress(progress)

covered_artists_amount += counter
helpers.endProgress("  Artists covered: " +
                    "\033[36m" + str(covered_artists_amount) + "\033[0m")
