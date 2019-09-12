import csv
from collections import defaultdict
from bs4 import BeautifulSoup

data16 = defaultdict(list)
data18 = defaultdict(list)

with open('cleaned.csv') as f:
    data = csv.reader(f)
    for line in data:
        if line[0] == 'year':
            continue
        year = line[0]
        state = line[2]
        dist = line[3] if line[3] != '0' else 'AL'
        if dist.isdigit() and int(dist) < 10:
            dist = "0" + dist
        party = line[4]
        votes = int(line[5])
        total_votes = int(line[6])
        if year == "2016":
            data16["{}-{}".format(state, dist)].append((party[0], votes/total_votes))
        else:
            data18["{}-{}".format(state, dist)].append((party[0], votes/total_votes))

ratios = {}

for dist in data18:
    curr = data18[dist]
    if len(curr) == 2:
        vals = [curr[0][1],curr[1][1]]
        rat = min(vals)/max(vals)
        ratios[dist] = rat
    else:
        ratios[dist] = 1-curr[0][1]

palette = ["#3c1361", "#52307c", "#7c5295", "#b491c8", "#bac0dc"]

svg = open('Most_even_districts.svg', 'r').read()
soup = BeautifulSoup(svg, features="html.parser")

paths = soup.findAll('path')
for p in paths:
    if "Dividing_line" not in p["id"]:
        rate = ratios[p["id"]]
        if rate > .9:
            color_class = 0
        elif rate > .7:
            color_class = 1
        elif rate > .4:
            color_class = 2
        elif rate > .1:
            color_class = 3
        else:
            color_class = 4

        p["style"] = "fill:{};stroke:#000000;stroke-width:0.333;stroke-opacity:1;fill-opacity:1".format(palette[color_class])

print (soup.prettify())
