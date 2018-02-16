import os
import ast

import prepare_helpers

dir = os.path.dirname(__file__)
artist_info_file_path = os.path.join(
    dir, "../../data/prepared/artist_info.txt")

artists = []
counter = 0

current_artist_amount = prepare_helpers.file_len(artist_info_file_path)
artist_info_file = open(artist_info_file_path, 'r')

prepare_helpers.startProgress(
    "  Cleaning Artists",
    "  Total Artists: {0}".format(current_artist_amount)
)

for line in artist_info_file:
    artist = ast.literal_eval(line.strip())
    # print artist["name"]
    if not any(d["name"] == artist["name"] for d in artists):
        artists.append(artist)
        # print 'new'
    # else:
    #     print artist["name"]
    #     print 'exists'
    counter += 1
    progress = ((counter + 0.0) / current_artist_amount) * 100

    prepare_helpers.progress(progress)

print len(artists)
prepare_helpers.endProgress("  Artists remaining: {0}".format(len(artists)))
