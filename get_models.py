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

tags = []
titles = []
#nltk.download('punkt')

global tfidf

podcast_dict = {}

def load():
	tags = pickle.load(open('tagEpisodesList.pkl', 'rb'))
	titles = pickle.load(open('titleEpisodesList.pkl', 'rb'))

	for i in range(len(titles)):
		tagStr = " ".join(tags[i])
		podcast_dict[titles[i]] = tagStr

stemmer = PorterStemmer()

def stem_words(words_list, stemmer):
	return [stemmer.stem(word) for word in words_list]

def tokenize(text):
	tokens = nltk.word_tokenize(text)
	stems = stem_words(tokens, stemmer)
	return stems


def train():
	global tfidf
	tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
	tfs = tfidf.fit_transform(podcast_dict.values())



	model_tf_idf = NearestNeighbors(metric='cosine', algorithm='brute')
	model_tf_idf.fit(tfs)


# filename = 'pod_model.sav'
# pickle.dump(model_tf_idf, open(filename, 'wb'))
# pickle.dump(tfidf, open("pod_vectorizer.pk", "wb"))


