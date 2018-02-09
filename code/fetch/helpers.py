import glob
import os
import sys
import urllib
import urllib2
import time
import base64
import json

import config
dir = os.path.dirname(__file__)


def get_new_access_token():
    with open(os.path.join(dir, "./spotify_refresh_token.txt"), "r") as f:
        refresh_token = f.read()

    unencoded_str = config.SPOTIFY["CLIENT_ID"] + \
        ":" + config.SPOTIFY["CLIENT_SECRET"]
    encoded_str = "Basic " + base64.b64encode(unencoded_str.encode('utf-8'))

    body = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    body = urllib.urlencode(body)

    data = urllib2.urlopen(
        urllib2.Request("https://accounts.spotify.com/api/token", body, headers={"Authorization": encoded_str}))

    data = json.loads(data.read())
    # print json.dumps(data.read(), indent=2)
    access_token = data["access_token"]
    with open(os.path.join(dir, "spotify_access_token.txt"), "w") as f:
        f.write("Bearer " + access_token)

    config.set_access_token(access_token)
    config.SPOTIFY["ACCESS_TOKEN"] = access_token

    return access_token


def get_last_fm_api_url(method, page="1", format="json", limit="500"):
    url = config.LAST_FM["API_URL"] + \
        "format=" + format + "&api_key=" + \
        config.LAST_FM["API_KEY"] + "&method=" + \
        method + "&page=" + page + "&limit=" + limit
    return url


def get_spotify_api_url(method, query_type, query, offset="1", limit="50"):
    if method == "search":
        url = config.SPOTIFY["API_URL"] + \
            method + "?q=" + query + "&type=" + query_type + "&limit=" + limit
    else:
        url = config.SPOTIFY["API_URL"] + \
            method + "/" + query + "/" + query_type + "?country=AT"
    return url


def make_api_call(url):
    data = urllib2.urlopen(url)
    return data


def make_spotify_api_call(url, max_retries=5):
    error = False
    for i in range(max_retries):
        access_token = config.SPOTIFY["ACCESS_TOKEN"]
        try:
            req = urllib2.Request(url, headers={'Authorization': access_token})
            data = urllib2.urlopen(req)
            return data
        except urllib2.HTTPError as e:
            if e.code == 401:
                print 'Access token expired!'
                # raw_input('Refresh token in Client and Press Enter')
                print 'Refreshing Access token'
                access_token = get_new_access_token()
                continue
            elif e.code == 502:
                print '502'
                continue
            elif e.code == 429:
                print 'too many requests'
                print e.headers["Retry-After"]
                time.sleep(int(e.headers["Retry-After"]) + 1)
                continue
            else:
                error = e.code
                continue
    else:
        print 'API call failed - too many retries'
        return error


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
    print("Artists total: " + str(count))


def file_len(fname):
    i = -1
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def startProgress(msg1, msg2="", msg3=""):
    print "##############################################"
    print msg1
    if not msg2 == "":
        print msg2
    if not msg3 == "":
        print msg3
    print "##############################################"
    global progress_x
    sys.stdout.write("[" + "-" * 40 + "]" + chr(8) * 41)
    sys.stdout.flush()
    progress_x = 0


def progress(x):
    global progress_x
    x = int(x * 40 // 100)
    sys.stdout.write("#" * (x - progress_x))
    sys.stdout.flush()
    progress_x = x


def endProgress(msg):
    sys.stdout.write("#" * (40 - progress_x) + "]\n")
    sys.stdout.flush()
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    print(msg)
    print('##############################################')
