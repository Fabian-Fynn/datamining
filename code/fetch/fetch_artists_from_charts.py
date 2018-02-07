import json
import os
import sys

import config
import helpers

dir = os.path.dirname(__file__)
reload(sys)
sys.setdefaultencoding('utf8')


amount_in_thousand = 10
amount_fetched = 0

for thousand in range(amount_in_thousand):
    page = str(thousand + 1)

    if (thousand + 1) < 10:
        filename_suffix = "0" + page
    else:
        filename_suffix = page

    artists_file = open(
        os.path.join(
            dir, "../../data/fetched/artists_charts/artists_charts_" + filename_suffix + ".txt"), "w")
    url = helpers.get_api_url(
        "chart.gettopartists", page=page, limit="1000")
    raw = helpers.make_api_call(url).read()
    data = json.loads(raw)

    if "error" in data:
        print "## ERROR ##"
        print data["message"]
        print "###########"

    else:
        artists = data["artists"]["artist"]
        amount_fetched += len(artists)
        print "Fetched: " + str(amount_fetched) + " Artists"

        for artist in artists:
            print>>artists_file, artist["name"]

    artists_file.close()

helpers.combine_fetched_artists()
