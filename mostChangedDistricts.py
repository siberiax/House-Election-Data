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

for dist in data16:
    curr = data16[dist]
    if len(curr) == 1:
        party = curr[0][0]
        if (party == 'D'):
            data16[dist] = -1 * curr[0][1]
        else:
            data16[dist] = curr[0][1]
    else:
        rep = 0
        dem = 0
        for party in curr:
            if party[0] == 'D':
                dem = party[1]
            else:
                rep = party[1]
        data16[dist] = rep - dem

for dist in data18:
    curr = data18[dist]
    if len(curr) == 1:
        party = curr[0][0]
        if (party == 'D'):
            data18[dist] = -1 * curr[0][1]
        else:
            data18[dist] = curr[0][1]
    else:
        rep = 0
        dem = 0
        for party in curr:
            if party[0] == 'D':
                dem = party[1]
            else:
                rep = party[1]
        data18[dist] = rep - dem


palette = ["#ff0000", "#ff7f7f", "#0000ff", "#7f7fff", "#8a2be2", "#c71585", "#cccccc"]

svg = open('US_Congressional_districts.svg', 'r').read()
soup = BeautifulSoup(svg, features="html.parser")

paths = soup.findAll('path')
for p in paths:
    if p["id"] in data16 and "PA" not in p["id"]:
        rate16 = data16[p["id"]]
        rate18 = data18[p["id"]]
        diff = rate16 - rate18

        s = BeautifulSoup(features="html.parser")
        title = s.new_tag('title', id=p["id"])
        p.append(title)

        perc16 = abs(round(rate16*100,2))
        perc18 = abs(round(rate18*100,2))

        if rate16 < 0 and rate18 > 0:          # flipped red
            color_class = 5
            title.string = "{} flipped Red\n2016: Dem won by {}%\n2018: Rep won by {}%".format(p["id"],perc16,perc18)
        elif rate16 > 0 and rate18 < 0:        # flipped blue
            color_class = 4
            title.string = "{} flipped Blue\n2016: Rep won by {}%\n2018: Dem won by {}%".format(p["id"],perc16,perc18)
        else:
            if abs(diff) < .1:
                if rate16 > 0:
                    party = "Rep"
                else:
                    party = "Dem"
                title.string = "{} did not change much\n2016: {} won by {}%\n2018: {} won by {}%".format(p["id"],party,perc16,party,perc18)
                color_class = 6

            elif rate16 < 0 and rate18 < 0:       # stayed blue
                if rate18 < rate16:
                    color_class = 2             # more blue
                    title.string = "{} became more blue\n2016: Dem won by {}%\n2018: Dem won by {}%".format(p["id"],perc16,perc18)
                else:
                    color_class = 3            # less blue
                    title.string = "{} became less blue\n2016: Dem won by {}%\n2018: Dem won by {}%".format(p["id"],perc16,perc18)
            else:                               # stayed red
                if rate18 > rate16:
                    color_class = 0             # more red
                    title.string = "{} became more red\n2016: Rep won by {}%\n2018: Rep won by {}%".format(p["id"],perc16,perc18)
                else:
                    color_class = 1             # less red
                    title.string = "{} became less red\n2016: Rep won by {}%\n2018: Rep won by {}%".format(p["id"],perc16,perc18)

        p["style"] = "fill:{};stroke:#000000;stroke-width:0.333;stroke-opacity:1;fill-opacity:1".format(palette[color_class])
        p.append(title)

with open("Most_Changed_Districts.svg", "w") as out:
    out.write(soup.prettify())
