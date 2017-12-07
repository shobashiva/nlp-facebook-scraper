# from __future__ import division
import nltk, re, pprint

# from nltk import nltk

import sys
import json
import os
import codecs
import math

SOURCE_FILE_DIR = 'YOUR_DIR_HERE' # replace with your folder
TRANSFORM_FILE_DIR = 'YOUR_DIR_HERE' # replace with your folder

data = ''

def get_percent(total_tokens, denominator):
	return int(math.floor(total_tokens/denominator))

def main():
	with codecs.open(SOURCE_FILE_DIR + 'YOUR_FILE_NAME', encoding='utf-8') as fi:
		data = fi.read()

	tokens = nltk.word_tokenize(data)

	text = nltk.Text(tokens)

	fdist = nltk.FreqDist(text)
	vocabulary = fdist.keys()
	percent = get_percent(len(tokens), 10000)


	relevant = [w for w in vocabulary if len(w) > 7 and fdist[w] > percent]
	relevant = nltk.pos_tag(relevant)
	summary = [s for s in relevant if s[1] != 'NNP']
	summary = [s[0] for s in summary]
	print(summary)
	print(text.concordance('experience')) #husband, wife
	print(text.similar('experience'))
	print(text.common_contexts(['experience', 'love']))
	print(text.collocations())

main()