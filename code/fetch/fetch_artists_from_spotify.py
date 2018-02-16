import os
import sys
import json
import re
import urllib2

import helpers

dir = os.path.dirname(__file__)
reload(sys)
sys.setdefaultencoding('utf8')
covered_artists_file_path = os.path.join(
    dir, "../../data/assist/covered_artists.txt")
artist_info_file_path = os.path.join(
    dir, "../../data/prepared/artist_info.txt")
artists_file_path = os.path.join(
    dir, "../../data/prepared/artists.txt")
helpers.create_file_if_not_exists(covered_artists_file_path)
helpers.create_file_if_not_exists(artist_info_file_path)

artist_amount = 10000
counter = 0

covered_artists = helpers.read_lines_from_file(covered_artists_file_path)
artist_names = helpers.read_lines_from_file(artists_file_path)

covered_artists_file = open(covered_artists_file_path, "a")
artist_info_file = open(artist_info_file_path, "a")

covered_artists_amount = len(covered_artists)
found_artists_amount = helpers.file_len(artist_info_file_path)

helpers.startProgress(
    "  Fetching next {0} Artists ".format(artist_amount),
    "  Artists covered: " + str(covered_artists_amount),
    "  Artists found: " + str(found_artists_amount))

for artist in artist_names:
    if counter >= artist_amount:
        break
    if artist in covered_artists:
        covered_artists.remove(artist)
        continue
    artist = artist.strip()
    query = artist.replace(" ", "+")
    query = urllib2.quote(query, safe='/')
    url = helpers.get_spotify_api_url(
        "search", query=query, query_type="artist", limit="10")
    raw = helpers.make_spotify_api_call(url)
    if not raw:
        break
    elif type(raw) == type(123):
        print "Error: " + str(raw)
        break

    data = json.loads(raw.read())["artists"]["items"]
    possible_matches = []
    found_match = {}

    # If exactly one artist is returned, take that one
    if len(data) == 1:
        found_match = data[0]
    else:
        for a in data:
            if a["name"].lower() == artist.lower():
                possible_matches.append(a)

        cleaned_matches = []

        # If there is only one artist which matches lowercase name, take that one
        if len(possible_matches) == 1:
            found_match = possible_matches[0]
        # Are there more than one?
        elif len(possible_matches) > 1:
            for possible_match in possible_matches:
                # Get rid of all artists with no genres
                if len(possible_match["genres"]) > 0:
                    cleaned_matches.append(possible_match)
            # If only one left, take that one
            if len(cleaned_matches) == 1:
                found_match = cleaned_matches[0]
            # If there are more, select the one with higher popularity
            elif len(cleaned_matches) == 0:
                best_match = {}
                for a in possible_matches:
                    if best_match == {}:
                        best_match = a
                    elif a["popularity"] > best_match["popularity"]:
                        best_match = a
                found_match = best_match
                # print "best match: " + best_match["name"]
        else:
            covered_artists_file.write("%s\n" % artist)
            # print "none: " + artist

    if found_match != {}:
        write_obj = {
            'name': found_match["name"],
            'id': found_match["id"],
            'genres': found_match["genres"],
            'popularity': found_match["popularity"]
        }
        artist_info_file.write("%s\n" % write_obj)
        covered_artists_file.write("%s\n" % artist)
        found_artists_amount += 1
    counter += 1

    progress = ((counter + 0.0) / artist_amount) * 100
    helpers.progress(progress)

covered_artists_amount += counter

helpers.endProgress("  Artists covered: " + str(covered_artists_amount))
