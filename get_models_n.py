from __future__ import division
import json
import re
import nltk
from nltk.corpus import stopwords
import time
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.neighbors import NearestNeighbors
from sklearn.externals import joblib

titles = []
tags  = []
tagStrArr = []

global tfidf

#podcast_dict = {}

def load():
	tags = pickle.load(open('tagNewsList.pkl', 'rb'))
	titles = pickle.load(open('titleNewsList.pkl', 'rb'))

	for i in range(len(titles)):
		tagStr = " ".join(tags[i])
		tagStrArr.append(tagStr)
#       podcast_dict[titles[i]] = tagStr

#print(titles)
stemmer = PorterStemmer()

def stem_words(words_list, stemmer):
       return [stemmer.stem(word) for word in words_list]

def tokenize(text):
       tokens = nltk.word_tokenize(text)
       stems = stem_words(tokens, stemmer)
       return stems

def learn():
	global tfidf
	tfidf = TfidfVectorizer()
	#tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
	tfs = tfidf.fit_transform(tagStrArr)



	model_tf_idf = NearestNeighbors(metric='cosine', algorithm='brute')
	model_tf_idf.fit(tfs)

filename = 'news_model.sav'

