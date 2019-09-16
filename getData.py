from csv import reader as csvreader, writer as csvwriter
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

dists = {}

with open('cleaned.csv') as f:
    data = csvreader(f)
    for line in data:
        if line[0] == 'year':
            continue
        state = line[1]
        dist = line[3]

        if state[-1] != 's':
            state += "'s"
        else:
            state += "'"

        state = state.replace(' ', '_')

        if dist == '0':
            dist = 'At-Large'
        elif dist[-1] == '1' and dist != '11':
            dist += 'st'
        elif dist[-1] == '2' and dist != '12':
            dist += 'nd'
        elif dist[-1] == '3' and dist != '13':
            dist += 'rd'
        else:
            dist += 'th'

        if (state,dist) not in dists:
            dists[(state, dist)] = (line[2], line[3])

out = open('newData.csv', 'w')
out = csvwriter(out)

for dist in dists:
    r = requests.get("https://ballotpedia.org/{}_{}_Congressional_District_election,_2016".format(dist[0], dist[1]))
    if r.status_code != 200:
        print("{}: {}, {}".format("2016", dist, status_code))
        continue
    data = BeautifulSoup(r.text, features="html.parser")
    tabs = data.findAll("table")
    try:
        for tab in tabs:
            if "General Election, 2016" in tab.text:
                rows = tab.findAll("tr")
                parties = defaultdict(int)
                total_votes = 0
                for row in rows[2:-2]:
                    fields = row.text.split("\n")
                    party = fields[2]
                    votes = int(fields[-2].replace(',', ''))
                    if "Dem" in party:
                        parties['D'] += votes
                    elif "Rep" in party:
                        parties['R'] += votes
                    total_votes += votes

        abbr = dists[dist]
        for party in parties:
            to_write = ['2016', abbr[0], abbr[1], party, parties[party], total_votes]
            out.writerow(to_write)
    except:
        print("2016: {} error".format(dist))
        pass

    r = requests.get("https://ballotpedia.org/{}_{}_Congressional_District_election,_2018".format(dist[0], dist[1]))
    if r.status_code != 200:
        print("{}: {}, {}".format("2018", dist, status_code))
        continue
    data = BeautifulSoup(r.text, features="html.parser")
    rows = data.findAll("table")[0].findAll('tr')

    parties = defaultdict(int)
    total_votes = 0

    try:
        for row in rows[1:]:
            row = row.text.split('\xa0')
            party = row[1]
            votes = int(row[-1].strip().replace(',', ''))
            if party == '(D)':
                parties['D'] += votes
            elif party == '(R)':
                parties['R'] += votes
            total_votes += votes

        abbr = dists[dist]
        for party in parties:
            to_write = ['2018', abbr[0], abbr[1], party, parties[party], total_votes]
            out.writerow(to_write)
    except:
        print("2018: {} error".format(dist))
        pass


















    #
