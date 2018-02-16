import json
import os
import sys

import config
import helpers

dir = os.path.dirname(__file__)
reload(sys)
sys.setdefaultencoding('utf8')

artist_file_path = os.path.join(
    dir, "../../data/fetched/artists_from_charts.txt")
artist_fetch_last_page_file_path = os.path.join(
    dir, "../../data/assist/artist_fetch_last_page_file.txt")
helpers.create_file_if_not_exists(artist_file_path)
helpers.create_file_if_not_exists(artist_fetch_last_page_file_path)

artist_file = open(artist_file_path, "r")

covered_artists = helpers.read_lines_from_file(artist_file)
artist_file.close()
covered_artists_amount = len(covered_artists)

with open(artist_fetch_last_page_file_path, 'r') as f:
    last_page = f.readline()

if last_page == "":
    last_page = 0
else:
    last_page = int(last_page)

page = last_page
pages = 500
limit = 10


helpers.startProgress(
    "  Fetching next {0}k Artists from Last FM Charts".format(pages),
    "  Artists covered so far: {0}".format(str(covered_artists_amount)),
)

artist_file = open(artist_file_path, "a")


while True:
    if page >= last_page + pages:
        break

    page += 1
    url = helpers.get_last_fm_api_url(
        "chart.gettopartists", page=str(page), limit=str(limit))
    raw = helpers.make_api_call(url).read()
    data = json.loads(raw)
    artists = data["artists"]["artist"]
    for artist in artists:
        artist_file.write("%s\n" % artist["name"])
        covered_artists_amount += 1

    # progress = ((page - last_page + 0.0) / pages) * 100
    # helpers.progress(progress)

helpers.endProgress("  Artists covered: " + str(covered_artists_amount))

with open(artist_fetch_last_page_file_path, 'w') as f:
    f.write(str(page))
