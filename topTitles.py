import json


aspirationTitles = []

with open('podcasts/top200.json') as json_data:
	d = json.load(json_data)

	feed = d['feed']
	entry = feed['results']
	for i in range(0,200):
		title = entry[i]['name']
		aspirationTitles.append(title)

fd = open('podcasts/topTitles.txt', 'a+')
for i in aspirationTitles:
	fd.write(i)
	fd.write('\n')


fd.close()	


