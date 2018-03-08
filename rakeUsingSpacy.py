from __future__ import unicode_literals
from os import listdir
from os.path import isfile, join
import spacy
import numpy as np
nlp=spacy.load("en")

import re
import operator

def is_number(s):
	try:
		float(s) if '.' in s else int(s)
		return True
	except ValueError:
		return False


def generate_candidate_keywords(sentence_list):
	phrase_list=[]
	stopword_regex_list=[]
	for s in sentence_list:
		doc=nlp(s.decode('utf-8'))
		print "Doc",doc
		for token in doc:
			print token.text 
			if token.is_stop or token.text=='good':   ######################################
				print token.text
				word_regex='\\b'+token.text+'\\b'
				stopword_regex_list.append(word_regex)
		pattern=re.compile('|'.join(stopword_regex_list),re.IGNORECASE)
		temp=re.sub(pattern, '|',s.strip())
		phrases=temp.split("|")
		'''
		print token.text
		s=s.replace(token.text,"|",1)
		print s
		phrases=s.split("|")
		'''
		for phrase in phrases:
			phrase=phrase.strip().lower()
			if phrase!="":
				phrase_list.append(phrase)
				print phrase
	return phrase_list

def calculate_word_scores(phraseList):
	word_frequency={}
	word_degree={}
	
	for phrase in phraseList:
		word_list=[]
		phrase=nlp(phrase.decode('utf-8'))
		for token in phrase:
			word_list.append(token.text)
		word_list_length=len(word_list)
		word_list_degree=word_list_length - 1
		for word in word_list:
			word_frequency.setdefault(word,0)
			word_frequency[word]+=1 
			word_degree.setdefault(word, 0)
			word_degree[word]+= word_list_degree

	for item in word_frequency:
		word_degree[item]= word_degree[item]+word_frequency[item]
	word_score = {}
	for item in word_frequency:
		word_score.setdefault(item, 0)
		word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)  #orig.
	#word_score[item] = word_frequency[item]/(word_degree[item] * 1.0) #exp.
	return word_score

def generate_candidate_keyword_scores(phrase_list, word_score):
    keyword_candidates = {}
    for phrase in phrase_list:
    	word_list=[]
        keyword_candidates.setdefault(phrase, 0)
        phrase=nlp(phrase.decode('utf-8'))
        for token in phrase:
        	word_list.append(token.text)
        candidate_score = 0
        for word in word_list:
            candidate_score += word_score[word]
        keyword_candidates[phrase] = candidate_score
    return keyword_candidates

class Rake(object):
	
	def run(self,text):
		text=nlp(text.decode('utf-8'))
		sentence_list=[]
		for sent in text.sents:
			sentence_list.append(sent.text.encode('ascii','ignore'))
		print type(sentence_list[0])
		phrase_list = generate_candidate_keywords(sentence_list)
		word_scores=calculate_word_scores(phrase_list)
		keyword_candidates=generate_candidate_keyword_scores(phrase_list,word_scores)
		sorted_keywords= sorted(keyword_candidates.iteritems(), key=operator.itemgetter(1), reverse=True)
		return sorted_keywords



'''


from __future__ import unicode_literals
from os import listdir
from os.path import isfile, join
import spacy
import numpy as np
nlp=spacy.load("en")

data_path='/home/login/Scapy Intent Detection'
labels = [f for f in listdir(data_path) if isfile(join(data_path, f))]
for label in labels:
    x_file = open('/home/login/Scapy Intent Detection/'+label.split('.')[0]+'.txt')
    #print x_file
    x_sents = x_file.readlines()
	for x_sent in x_sents:
		if len(x_sent>0):
			x_doc = nlp(x_sent.decode('utf-8'))
'''			            