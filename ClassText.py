#!/usr/bin/env python

from collections import Counter as count
from string import punctuation
from math import sqrt
import re


class ClassText(object):
	"""
	A class which handles the text I/O of the chat
	"""

	def __init__(self):
		"""
		The default greeting form the chat bot
		:return:    string
		"""
		self.text = "Hello! How are you?"

	def setText(self, newText):
		"""
		Set a new text message
		:param newText: string
		:return:        none
		"""
		self.text = newText

	def getText(self):
		"""
		Retrieve the text message
		:return:    string
		"""
		return self.text

	def getTextCount(self):
		"""
		Regular expression that will look for English words
		It returns a Count object with the word frequency
		:return:    object
		"""
		pattern = '(?:\w+|[' + re.escape(punctuation) + ']+)'
		# pattern = '\w+'
		regex = re.compile(pattern)
		words = regex.findall(self.getText().lower())

		return count(words).items()

	def getTextWeight(self):
		"""
		Calculate the weight of each word in the sentence
		It returns an dictionary representing each word's weight as float
		:return:    dictionary
		"""
		weights = {}
		words_len = sum([i * len(word) for word, i in self.getTextCount()])

		for word, i in self.getTextCount():
			weights[word] = sqrt(i * 1. / words_len)

		return weights




