import os
import sys
import json
import ast

import helpers

dir = os.path.dirname(__file__)
reload(sys)
sys.setdefaultencoding('utf8')

# Filepaths
fetched_artists_from_lastfm_file_path = os.path.join(
    dir, "../data/prepared/artists.txt")
fetched_artists_from_spotify_file_path = os.path.join(
    dir, "../data/prepared/artist_info.txt")
fetched_top_tracks_artists_file_path = os.path.join(
    dir, "../data/assist/covered_top_tracks_artists.txt")
fetched_artists_features_file_path = os.path.join(
    dir, "../data/assist/covered_artists_features.txt")
cleaned_artists_file_path = os.path.join(
    dir, "../data/prepared/cleaned_artists.txt")

# Read amounts
fetched_artists_last_fm = helpers.file_len(
    fetched_artists_from_lastfm_file_path)
artists_spotify = helpers.file_len(fetched_artists_from_spotify_file_path)
artists_top_tracks = helpers.file_len(fetched_top_tracks_artists_file_path)
artists_tracks_features = helpers.file_len(fetched_artists_features_file_path)
artists_cleaned = helpers.file_len(cleaned_artists_file_path)

print "#" * 60
print ""

print " " * 23 + "\033[1;36m STATISTICS \033[0;0m"
print ""
print "  Fetched Artists from Last FM Charts: \033[0;36m{0}\033[0;0m".format(fetched_artists_last_fm)
print "  Fetched Artists from Spotify (from last FM Charts + related): \033[0;36m{0}\033[0;0m".format(artists_spotify)
print "  Cleaned Artists from Spotify: \033[0;36m{0}\033[0;0m".format(artists_cleaned)
print "  Fetched Top Tracks of \033[0;36m{0}\033[0;0m Artists".format(artists_top_tracks)
print "  Fetched Audio Features of Top Tracks for \033[0;36m{0}\033[0;0m Artists".format(artists_tracks_features)
print ""
print "#" * 60
