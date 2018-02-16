import glob
import os
import sys
import urllib
import urllib2
import time
import base64
import json

dir = os.path.dirname(__file__)


def file_len(fname):
    i = -1
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def create_file_if_not_exists(path):
    if not os.path.exists(path):
        open(path, 'a').close()


def read_lines_from_file(path):
    file = open(path, "r")
    array = []
    for line in file:
        array.append(line.strip())
    file.close()
    return array


def startProgress(msg1, msg2="", msg3=""):
    print "#" * 48
    print "\033[36m" + msg1 + "\033[0m"
    if not msg2 == "":
        print msg2
    if not msg3 == "":
        print msg3
    print "#" * 48
    global progress_x
    sys.stdout.write("[" + "-" * 40 + "]" + chr(8) * 41)
    sys.stdout.flush()
    progress_x = 0


def progress(x):
    global progress_x
    x = int(x * 40 // 100)
    sys.stdout.write("\033[36m#\033[0m" * (x - progress_x))
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
    print "#" * 48
