import json

ids = ['1306','1459','1301','1401','1402','1405','1406','1303','1304','1415','1416','1468','1469','1470','1305','1307','1417','1420','1421','1481','1309','1310','1311','1314','1438','1439','1440','1441','1444','1463','1464','1315','1477','1478','1479','1316','1456','1465','1466','1467','1318','1446','1448','1450','1480','1321','1410','1412','1413','1471','1472','1323','1404','1454','1455','1460','1461','1324','1302','1320','1443','1462','1325','1473','1474','1475','1476']
itunes_ids = []
itunes_titles = []
itunes_descriptions = []

podcast_data = {}

for i in ids:
	data = None
	filename = 'podcasts_final/' + i + '.json'
	with open(filename) as json_data:
		data = json.load(json_data)	

	# feed = data['feed']
	entries = data['results']
	
	for e in range(len(entries)):
		itunes_id = entries[e]['trackId']
		itunes_title = entries[e]['trackName']
		# itunes_description = entries[e]['summary']['label']
		itunes_img = entries[e]['artworkUrl60']


		tempDict = {}
		tempDict['title'] = itunes_title
		# tempDict['description'] = itunes_description
		tempDict['img'] = itunes_img
		podcast_data[itunes_id] = tempDict


		# itunes_titles.append(itunes_title)
		# itunes_descriptions.append(itunes_description)

# itunes = list(set(itunes_ids))

fd = open('data' + '/' + 'podcast_data.json', 'a+')
fd.write(json.dumps(podcast_data))
fd.write('\n')

fd.close()





