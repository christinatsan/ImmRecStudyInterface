from flask import Flask, flash, redirect, render_template, request, session, abort, Response, jsonify, url_for
import json
#from flask.ext.session import Session
#from forms import LoginForm
#import flask_login
import flask
import numpy as np
from sklearn.neighbors import NearestNeighbors
from random import shuffle
import get_models_n
import get_models
from nltk.stem.porter import PorterStemmer
import pickle
import nltk
from random import shuffle
import math
from get_models_n import tokenize
from werkzeug.local import Local
from threading import Lock
import time
import ast
import operator


app = Flask(__name__, static_url_path='/static')
# loc = Local()
app.secret_key = 'super secret string'  # Change this!

topLevelTags = {'Food':'1306','Fashion & Beauty':'1459','Arts & Literature':'1301','Comedy':'1303','Education':'1304','Kids & Family':'1305','Health':'1307','TV & Film':'1309','Music':'1310','News & Politics':'1311','Religion & Spirituality':'1314','Science & Medicine':'1315','Sports & Recreation':'1316','Technology':'1318','Business':'1321','Games & Hobbies':'1323','Society & Culture':'1324','Government & Organizations':'1325'}

subLevelTagIDs = {'1306':[],'1459':[],'1301':['1401','1402','1405','1406'],'1303':[],'1304':['1415','1416','1468','1469','1470'],'1305':[],'1307':['1417','1420','1421','1481'],'1309':[],'1310':[],'1311':[],'1314':['1438','1439','1440','1441','1444','1463','1464'],'1315':['1477','1478','1479'],'1316':['1456','1465','1466','1467'],'1318':['1446','1448','1450','1480'],'1321':['1410','1412','1413','1471','1472'],'1323':['1404','1454','1455','1460','1461'],'1324':['1302','1320','1443','1462'],'1325':['1473','1474','1475','1476']}

subLevelTags = {'1401':'Literature','1402':'Design','1405':'Performing Arts','1406':'Visual Arts','1415':'K-12','1416':'Higher Education','1468':'Educational Technology','1469':'Language Courses','1470':'Training','1417':'Fitness & Nutrition','1420':'Self-Help','1421':'Sexuality','1481':'Alternative Health','1438':'Buddhism','1439':'Christianity','1440':'Islam','1441':'Judaism','1444':'Spirituality','1463':'Hinduism','1464':'Other','1477':'Natural Sciences','1478':'Medicine','1479':'Social Sciences','1456':'Outdoor','1465':'Professional','1466':'College & High School','1467':'Amateur','1446':'Gadgets','1448':'Tech News','1450':'Podcasting','1480':'Software How-To','1410':'Careers','1412':'Investing','1413':'Management & Marketing','1471':'Business News','1472':'Shopping','1404':'Video Games','1454':'Automotive','1455':'Aviation','1460':'Hobbies','1461':'Other Games','1302':'Personal Journals','1320':'Places & Travel','1443':'Philosophy','1462':'History','1473':'National','1474':'Regional','1475':'Local','1476':'Non-Profit'}


# levelNews_1 = ['Fintech','Technology','Travel','Entrepreneurship','Self','Management','Media','Personal','Education','Politics','Love','Health','World','Entertainment','Sports','Creative','Marketing','Design','Social','Writing','Leadership','Development','Improvement','Productivity','Lessons']
# firstLevelPod = ['Poetry','Poem', 'Life', 'Music', 'Sports', 'Writing', 'Books', 'Politics', 'Christianity', 'Love', 'Education', 'Health', 'Movies', 'Startup', 'Humor', 'Television', 'Food', 'Entrepreneurship', 'Photography', 'Art', 'Media', 'Business', 'Travel','Gaming','Comics']

lock = Lock()

aspirationTags = []
historyTags = []

aspirationTags2 = []
historyTags2 = []

# fullHistoryDict = {}
# fullAspirationDict = {}

errortext= ""




@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
	session.clear()	
	session['turkerid'] = request.form['turkerid']
	session['errortext'] = ""
	return redirect(url_for('consent1'))


@app.route('/consent1')
def consent1():
	return render_template('consent1.html')

@app.route('/consent2')
def consent2():
	return render_template('consent2.html')



# @app.route('/eligibility', methods=['POST'])
# def eligibility():
# 	# session['does_listen_podcast'] = request.form['podcast_or_radio']
# 	return redirect(url_for('categories_pod'))

@app.route('/history_likert_response', methods=['POST'])
def history_likert_response():
	# session['history_likert_response'] = request.form['history_likert_response']

	# print(session['history_likert_response'])

	return redirect(url_for('logout'))

@app.route('/eligibilityques')
def eligibilityques():
	return render_template('eligibility_questions.html')

@app.route('/channels/<items>')
def channels(items):
	channels = items.split('+')
	del channels[0]

	channelDict = {}

	userid = session['turkerid']
	channelDict[userid] = channels

	fd = open('data' + '/' + 'channels.json', 'a+')
	fd.write(json.dumps(channelDict))
	fd.write('\n')
	fd.close()



	return redirect(url_for('logout'))


@app.route('/user_channels/<userid>')
def user_channels(userid):

	resultfile = open('data/resultdata.json', 'wt')

	data = []
	with open('data/channels.json') as f:
		for line in f:
			data.append(json.loads(line))

	resultfile.write(json.dumps(data))
	resultfile.close()

	with open('data/resultdata.json') as json_data:
		d = json.load(json_data)


	channels = []
	for i in d:
		for key in i.keys():
			if key == userid:
				channels = i[key]


	return render_template('channels.html',channels=channels)






@app.route("/categories_pod")
def categories_pod():

	errortext = session['errortext']

	return render_template('categories_pod.html',categories = topLevelTags.keys(),errortext = errortext)


def checkVal(b):
	if (b):
		pass
	else:
		checkVal(b)



@app.route("/categories2_pod/<items>")
def categories2_pod(items):

	parts = items.split('+')
	
	hist = parts[0]
	asp = parts[1]

	aspParts = asp.split(',')

	aspirationTags = []

	for name in aspParts:
		if name in topLevelTags.keys():
			aspirationTags.append(name)

	aspirationDict = {}

	fullAspirationDict = {}
   
	if len(aspirationTags) >= 1:
        

		totalAspirationGenres = []      
		for tag in aspirationTags:
			genreID = topLevelTags[tag]
			subGenresIDs = subLevelTagIDs[genreID]
            
			subGenres = []
			for subGenreID in subGenresIDs:
				subGenre = subLevelTags[subGenreID]
				subGenres.append(subGenre)

			fullAspirationDict[tag] = subGenres

			if len(subGenres) > 0:
				aspirationDict[tag] = subGenres

		session['fullAspirationDict'] = fullAspirationDict

		savedAspirationDict = {}
		userid = session['turkerid'] + '-aspiration'
		savedAspirationDict[userid] = fullAspirationDict

		fd = open('data' + '/' + 'data.txt', 'a+')
		fd.write(json.dumps(savedAspirationDict))
		fd.write('\n')
		fd.close()

        
		return render_template('categories2_pod.html', aspirationCategories = aspirationDict)
    
	else:
		errortext = "Please choose 5 unique topics for each prompt"
		return redirect(url_for('categories_pod'))

@app.route("/recommendations_pop_200")
def recommendations_pop_200():
	titles = []
	descriptions = []
	imgs = []

	d = None
	with open('podcasts/top200.json') as json_data:
		d = json.load(json_data)

	s = None
	with open('podcasts/topSummaries.json') as json_summaries:
		s = json.load(json_summaries)	


	feed = d['feed']
	entry = feed['results']
	summaryFeed = s['summaries']


	for i in range(0,200):
		
		title = entry[i]['name']
		titles.append(title)
		
		summary = summaryFeed[i][title]
		descriptions.append(summary)
		
		img = entry[i]['artworkUrl100']
		imgs.append(img)
		
	return render_template('recommendations_pod.html',articles = titles, descriptions = descriptions, images = imgs)



@app.route("/recommendations_pop/")
def recommendations_pop():
	d = None
	with open('data/podcast_data.json') as pod_data:
		d = json.load(pod_data)

	channels = {}
	titles = []
	descriptions = []
	imgs = []

	with open('popular_channel_counts.txt') as file:
		for line in file:
			parts = line.split(',')
			channel_id = parts[0]
			print(type(channel_id))
			channel_ranking = parts[1].rstrip('\n')
			channels[channel_id] = int(channel_ranking)



	sorted_channels = sorted(channels.items(), key=operator.itemgetter(1), reverse = True)
	print(sorted_channels)
	
	for channel in sorted_channels:
		channel_id = channel[0]
		channel_data = d[channel_id]
		titles.append(channel_data['title'])
		# descriptions.append(channel_data['description'])
		imgs.append(channel_data['img'])



	return render_template('recommendations_pod.html',articles = titles, descriptions = descriptions, images = imgs)






@app.route("/recommendations_pod/<items>")
def recommendations_pod(items):

	parts = items.split('+')
	asp = parts[1]
	aspParts = asp.split(',')
	aspirationTags2 = []

	for name in aspParts:
		if name in subLevelTags.values():
			aspirationTags2.append(name)
	

	fullAspirationDict = session['fullAspirationDict']

	aspirationLevel1 = []
	aspirationLevel2 = []

	aspirationIDs = []
	aspirationTitles = []
	aspirationDescriptions = []
	aspirationImages = []
	aspirationGenre = []

	titleToGenreDict = {}

	d = None
	with open('podcasts/top200.json') as json_data:
		d = json.load(json_data)

	s = None
	with open('podcasts/topSummaries.json') as json_summaries:
		s = json.load(json_summaries)	


	feed = d['feed']
	entry = feed['results']
	summaryFeed = s['summaries']


	for i in range(0,200):
		
		title = entry[i]['name']
		aspirationTitles.append(title)
		
		summary = summaryFeed[i][title]
		aspirationDescriptions.append(summary)
		
		img = entry[i]['artworkUrl100']
		aspirationImages.append(img)
		
		genres = entry[i]['genres']
		genreIDs = []
		for g in genres:
			genreID = g['genreId']
			genreIDs.append(genreID)

		titleToGenreDict[title] = genreIDs


	
	
	
	for item in fullAspirationDict.keys():
		if len(fullAspirationDict[item]) == 0:
			aspirationLevel1.append(item)
		else:
			subItems = fullAspirationDict[item]
			s = [i for i in aspirationTags2 if i in subItems]
			if len(s) == 0:
				aspirationLevel1.append(item)
			else:
				aspirationLevel1.append(item)
				aspirationLevel2.append(s[0])


	print("fullAspDict")
	print(fullAspirationDict)
	print("asp1")
	print(aspirationLevel1)
	print("asp2")
	print(aspirationLevel2)

	genreToScoreDict = {}

	for a in aspirationLevel1:
		a_id = topLevelTags[a]
		genreToScoreDict[a_id] = 1

	for a in aspirationLevel2:
		a_id = list(subLevelTags.keys())[list(subLevelTags.values()).index(a)]
		genreToScoreDict[a_id] = 2


	rankedDescriptions = []
	rankedImgs = []
	finalRankedTitles = []

	titleToScoreDict = {}

	for title in titleToGenreDict.keys():
		titleScore = 0
		all_genres = titleToGenreDict[title]
		
		for genre in genreToScoreDict.keys():
			if genre in all_genres:
				titleScore += genreToScoreDict[genre]

		titleScore = titleScore / len(all_genres)
		titleToScoreDict[title] = titleScore


	rankedTitles = sorted(titleToScoreDict.items(), key=operator.itemgetter(1), reverse=True)

	for pair in rankedTitles:
		title = pair[0]
		finalRankedTitles.append(title)
		index = aspirationTitles.index(title)
		rankedDescriptions.append(aspirationDescriptions[index])
		rankedImgs.append(aspirationImages[index])


	# print(genreToScoreDict)



	# for genre in genreToScoreDict.keys():
	# 	if genreToScoreDict[genre] == 2:
	# 		for title in titleToGenreDict.keys():
	# 			if title not in rankedTitles1:
	# 				all_genres = titleToGenreDict[title]
	# 				if genre in all_genres:
	# 					rankedTitles1.append(title)
	# 	if genreToScoreDict[genre] == 1:
	# 		for title in titleToGenreDict.keys():
	# 			if (title not in rankedTitles1) and (title not in rankedTitles2):
	# 				all_genres = titleToGenreDict[title]
	# 				if genre in all_genres:
	# 					rankedTitles2.append(title)

	# for title in titleToGenreDict.keys():
	# 	if (title not in rankedTitles1) and (title not in rankedTitles2):
	# 		rankedTitles3.append(title)



	# shuffle(rankedTitles1)
	# shuffle(rankedTitles2)
	# shuffle(rankedTitles3)

	# finalRankedTitles = rankedTitles1 + rankedTitles2 + rankedTitles3

	# for f_title in finalRankedTitles:
	# 	index = aspirationTitles.index(f_title)
	# 	rankedDescriptions.append(aspirationDescriptions[index])
	# 	rankedImgs.append(aspirationImages[index])


	

	# for a in aspirationLevel1:
	# 	a_id = topLevelTags[a]
	# 	aspirationIDs.append(a_id)


	# for a in aspirationLevel2:
	# 	a_id = list(subLevelTags.keys())[list(subLevelTags.values()).index(a)]
	# 	aspirationIDs.append(a_id)

	titles = finalRankedTitles
	descriptions = rankedDescriptions
	imgs = rankedImgs

		
	# titles = []
	# descriptions = []
	# imgs = []



	return render_template('recommendations_pod.html',articles = titles, descriptions = descriptions, images = imgs)




@app.route('/postAspirationItems', methods = ['POST'])
def get_post_javascript_data_aspirationItems():
	jsdata = request.form['javascript_data']
	jsonData = json.loads(jsdata)

	aspirationTags = []
	for i in range(1,6):
		tag = jsonData[str(i)]['item']
		print(tag)
		aspirationTags.append(tag)

	session['aspirationTags'] = aspirationTags
	print(aspirationTags)
    	
	return jsonify(jsonData)

@app.route('/postHistoryItems', methods = ['POST'])
def get_post_javascript_data_historyItems():
	jsdata = request.form['javascript_data']
	jsonData = json.loads(jsdata)

	historyTags = []
	for i in range(1,6):
		tag = jsonData[str(i)]['item']
		historyTags.append(tag)

	session['historyTags'] = historyTags
    	
	return jsonify(jsonData)

@app.route('/postAspirationItems2', methods = ['POST'])
def get_post_javascript_data_aspirationItems2():
	jsdata = request.form['javascript_data']
	jsonData = json.loads(jsdata)

	aspirationTags2 = []
	for i in range(len(jsonData)):
		tag = jsonData[str(i)]['item']
		aspirationTags2.append(tag)

	session['aspirationTags2'] = aspirationTags2

	return jsonify(jsonData)

    	
	# return jsonify(jsonData)

@app.route('/postHistoryItems2', methods = ['POST'])
def get_post_javascript_data_historyItems2():
	jsdata = request.form['javascript_data']
	jsonData = json.loads(jsdata)

	historyTags2 = []
	for i in range(len(jsonData)):
		tag = jsonData[str(i)]['item']
		historyTags2.append(tag)


	session['historyTags2'] = historyTags2

    	
	return jsonify(jsonData)


@app.route("/logout")
def logout():
	# TODO - SAVE ALL SESSION INFO TO JSON - STORE ON SERVER/EMAIL TO ME

	session.clear()	

	# sessionData = {}
	# sessionData['turkerid'] = session['turkerid']
	# sessionData['does_listen_podcast'] = session['does_listen_podcast']



	# #sessionData['chosenTags3'] = session['tags3']
	# sessionData['final-recommendations'] = session['final-recommendations']

#	fd = open('data' + '/' + 'data.txt', 'a+')
#	fd.write(json.dumps(sessionData))
#	fd.write('\n')
#	fd.close()

	
	return redirect(url_for('home'))




if __name__ == "__main__":
	app.run(threaded=True)
