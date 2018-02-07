import os
dir = os.path.dirname(__file__)

genre_artist_file = open(os.path.join(
    dir, "../../data/initial/genres+artists.txt"), "r")
artists_file = open(os.path.join(dir, "../../data/initial/artists.txt"), "w")

artists = []

for line in genre_artist_file:
    line = line.rstrip()
    text = line.split(':')
    artists.append(text[1])
    print>>artists_file, text[1]
