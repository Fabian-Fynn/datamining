artist_file = open("../data/fetched/artists_charts.txt", "r")

counter = 0

for line in artist_file:
    counter += 1

print counter
