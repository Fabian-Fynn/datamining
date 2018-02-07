import os
dir = os.path.dirname(__file__)

artists = []

with open(os.path.join(dir, "../../data/fetched/artists_charts.txt")) as f:
    artists.append(f.read().splitlines())

with open(os.path.join(dir, "../../data/initial/artists.txt")) as f:
    artists.append(f.read().splitlines())

combined = artists[0] + artists[1]
combined = filter(None, combined)  # Remove empty strings
unique = list(set(combined))

print "Unique Artists: " + str(len(unique))

cleaned_artists_file = open(os.path.join(
    dir, "../../data/prepared/artists.txt"), "w")

for item in unique:
    cleaned_artists_file.write("%s\n" % item)

cleaned_artists_file.close()
