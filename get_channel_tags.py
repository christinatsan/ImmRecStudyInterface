import json

ids = ['1306','1459','1301','1401','1402','1405','1406','1303','1304','1415','1416','1468','1469','1470','1305','1307','1417','1420','1421','1481','1309','1310','1311','1314','1438','1439','1440','1441','1444','1463','1464','1315','1477','1478','1479','1316','1456','1465','1466','1467','1318','1446','1448','1450','1480','1321','1410','1412','1413','1471','1472','1323','1404','1454','1455','1460','1461','1324','1302','1320','1443','1462','1325','1473','1474','1475','1476']
channelToTags = {}


for i in ids:
	data = None
	filename = 'podcasts/' + i + '.json'
	with open(filename) as json_data:
		data = json.load(json_data)	

	feed = data['feed']
	entries = feed['entry']
	
	for e in range(len(entries)):
		title = entry[e]['im:name']['label']
		genre = entry[e]['category']['attributes']['im:id']
		






fd = open('data' + '/' + 'ids.json', 'a+')
for i in itunes_ids:
	fd.write(i)
	fd.write('\n')

fd.close()