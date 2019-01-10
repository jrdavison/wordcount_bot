# Libraries
from operator import itemgetter 
import re

# Settings
from wordcount.settings import IGNORED_WORDS

class Counter:

	def __init__(self):
		""" Initialize object that handles counting of words """
		self.word_count_dict = {}
		self.num_comments = 0
		self.num_words = 0

	def __str__(self):
		sorted_dict = sorted(self.word_count_dict.items(), key=itemgetter(1), reverse=True) 
		
		output = ''
		printed_count = 0
		for word, count in sorted_dict:
			if printed_count >= 15:
				break;

			if word not in IGNORED_WORDS:
				output += '{:<25s}{:>15d}\n'.format(word, count)
				printed_count += 1

		output += '\nTotal comments analayzed: ' + str(self.num_comments)
		output += '\nTotal words analayzed: ' + str(self.num_words)
		
		return output

	def parse_response(self, json_input):
		""" Recursive function to parse json object

		Args:
			json_input (dict): json object formatted as a python dict
		"""
		more_posts = [] # holds ids returned in the 'more posts' section
		if json_input['kind'] == 'Listing':
			for el in json_input['data']['children']:
				more_posts += self.parse_response(el)
		elif json_input['kind'] == 'more':
			more_posts += json_input['data']['children']
		else:
			if 'body' in json_input['data']:
				self.count_words_in_str(json_input['data']['body'], is_comment=True)

			if json_input['data']['replies'] != '':
				more_posts += self.parse_response(json_input['data']['replies'])

		return more_posts
		

	def count_words_in_str(self, input_str, is_comment):
		""" Count the unique words in the string, update word_count_dict

		Args:
			input_str (string): string to parse and count words
		"""

		if is_comment:
			self.num_comments += 1
			print('Found ' + str(self.num_comments) + ' comments', end='\r')

		word_lst = input_str.split(' ')
		for word in word_lst:
			word_strip = re.sub(r'[^0-9a-zA-Z]+', '', word).lower() # remove all non alpha numeric characters
			if word_strip != '':
				if word_strip not in self.word_count_dict.keys():
					self.word_count_dict[word_strip] = 1
				elif word_strip in self.word_count_dict.keys():
					self.word_count_dict[word_strip] += 1

				self.num_words += 1