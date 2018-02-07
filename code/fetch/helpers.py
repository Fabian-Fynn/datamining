import glob
import os
import urllib2

import config
dir = os.path.dirname(__file__)


def get_api_url(method, page="1", format="json", limit="500"):
    url = config.LAST_FM["API_URL"] + \
        "format=" + format + "&api_key=" + \
        config.LAST_FM["API_KEY"] + "&method=" + \
        method + "&page=" + page + "&limit=" + limit
    return url


def make_api_call(url):
    data = urllib2.urlopen(url)
    return data


def combine_fetched_artists():
    artists_file = open(os.path.join(
        dir, "../../data/fetched/artists_charts.txt"), "w")
    path = os.path.join(
        dir, "../../data/fetched/artists_charts/artists_charts_*.txt")
    count = 0
    for filename in glob.glob(path):
        with open(filename, 'r') as f:
            for line in f:
                artists_file.write(line)
                count += 1
    print "Artists total: " + str(count)
