from csv import reader as csvreader
from collections import defaultdict
from bs4 import BeautifulSoup

data16 = defaultdict(list)
data18 = defaultdict(list)

with open('data.csv') as f:
    data = csvreader(f)
    for line in data:
        if line[0] == 'year':
            continue
        year = line[0]
        state = line[1]
        dist = line[2] if line[2] != '0' else 'AL'
        if dist.isdigit() and int(dist) < 10:
            dist = "0" + dist
        party = line[3]
        votes = int(line[4])
        total_votes = int(line[5])
        if year == "2016":
            data16["{}-{}".format(state, dist)].append((party, votes/total_votes))
        else:
            data18["{}-{}".format(state, dist)].append((party, votes/total_votes))

ratios = defaultdict(float)

for dist in data18:
    curr = data18[dist]
    if len(curr) == 2:
        vals = [curr[0][1],curr[1][1]]
        rat = min(vals)/max(vals)
        ratios[dist] = rat
    else:
        ratios[dist] = 1-curr[0][1]

palette = ["#3c1361", "#52307c", "#7c5295", "#b491c8", "#bac0dc"]

svg = open('US_Congressional_districts.svg', 'r').read()
soup = BeautifulSoup(svg, features="html.parser")

paths = soup.findAll('path')
for p in paths:
    if p["id"] in ratios and "PA" not in p["id"]:
        rate = ratios[p["id"]]
        if rate > .9:
            color_class = 0
        elif rate > .8:
            color_class = 1
        elif rate > .7:
            color_class = 2
        elif rate > .6:
            color_class = 3
        elif rate > .5:
            color_class = 4
        else:
            continue

        p["style"] = "fill:{};stroke:#000000;stroke-width:0.333;stroke-opacity:1;fill-opacity:1".format(palette[color_class])

with open("Most_Even_Districts.svg", "w") as out:
    out.write(soup.prettify())
