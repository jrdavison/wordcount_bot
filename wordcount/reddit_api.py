# Libraries
import requests
import time

# Classes
from wordcount.counter import Counter

# Settings
from wordcount.settings import APP_ID
from wordcount.settings import APP_SECRET
from wordcount.settings import PASSWORD
from wordcount.settings import USERNAME

class Reddit_API:

	def __init__(self):
		self.__app_id = APP_ID
		self.__app_secret = APP_SECRET

		self.__username = USERNAME
		self.__password = PASSWORD

		self.post_id_list = []

		self.authorized = self.authorize()

	def authorize(self):
		auth_endpoint = 'https://www.reddit.com/api/v1/access_token'

		client_auth = requests.auth.HTTPBasicAuth(self.__app_id, self.__app_secret)
		post_data = {'grant_type': 'password', 'username': self.__username, 'password': self.__password}
		headers = {'User-Agent': 'WordcountBot/1.1.0 by jmsrdvsn@gmail.com'}
		response = requests.post(auth_endpoint, auth=client_auth, data=post_data, headers=headers)

		deserialized_data = response.json()
		if response.status_code is 200 and 'access_token' in deserialized_data:
			self.__auth_token = deserialized_data['access_token']
			return True

		return False

	def get_subreddit_posts(self, num_posts, counter_obj):
		""" Gets the top 'num_posts' from a subreddit

		Creates an object of class Post and adds them to a list of posts

		Args:
			num_posts (int): number of posts to analyze from subreddit
			counter_obj (Counter): object that receives text data and parses it
		"""
		post_output = str(num_posts) + ' posts'
		if num_posts == 1:
			post_output = 'post'

		print('\nAnalyzing the top ' + post_output + ' from ' + self.subreddit)

		endpoint = 'https://oauth.reddit.com' + self.subreddit + '/top' 
		headers = {'Authorization': 'bearer ' + self.__auth_token, 'User-Agent': 'WordcountBot/1.0 by jmsrdvsn@gmail.com'}
		params = {'limit': num_posts, 't': 'all'}
		response = requests.get(endpoint, headers=headers, params=params)

		if response.status_code is 200:
			headers = response.headers
			if float(headers['X-Ratelimit-remaining']) < 1:
				time.sleep(int(headers['X-Ratelimit-Reset']))

			post_data = response.json()
			for post in post_data['data']['children']:
				counter_obj.count_words_in_str(post['data']['title'], is_comment=False)
				self.post_id_list.append(post['data']['id'])
		else:
			print('Error: could not get posts from the selected subreddit.')

	def get_post_comments(self, post_id, counter_obj):
		""" Gets all of the comments from a given post

		Args:
			post_id (string): post id used in the API endpoint URL
			counter_obj (string): object to receive text from each comment and parse it
		"""
		endpoint = 'https://oauth.reddit.com' + self.subreddit + '/comments/article'
		headers = {'Authorization': 'bearer ' + self.__auth_token, 'User-Agent': 'WordcountBot/1.0 by jmsrdvsn@gmail.com'}
		params = {'article': post_id, 'sort': 'top'}
		response = requests.get(endpoint, headers=headers, params=params)

		if response.status_code is 200:
			headers = response.headers
			if float(headers['X-Ratelimit-remaining']) < 1:
				time.sleep(int(headers['X-Ratelimit-Reset']))

			post_data = response.json()
			more_children = counter_obj.parse_response(post_data[1])

			for x in range(0, len(more_children), 500):
				if x + 500 <= len(more_children):
					child_list = ','.join(more_children[x:x + 500])
				else:
					child_list = ','.join(more_children[x:x + len(more_children)])

				self.get_post_children(post_id, child_list, counter_obj)
		else:
			print('Error: could not get comments from ' + self.subreddit + '.')

	def get_post_children(self, post_id, children, counter_obj):
		""" Gets all of the remaining child comments in a post

		Args:
			post_id (string): post id used to retreive comment trees
			children (list): list of children to retreive (max 20 children per API call)
			counter_obj (string): object to receive text from each comment and parse it
		"""
		endpoint = 'https://oauth.reddit.com/api/morechildren'
		headers = {'Authorization': 'bearer ' + self.__auth_token, 'User-Agent': 'WordcountBot/1.0 by jmsrdvsn@gmail.com'}
		params = {'link_id': 't3_' + post_id, 'children': children}
		response = requests.get(endpoint, headers=headers, params=params)

		if response.status_code is 200:
			headers = response.headers
			if float(headers['X-Ratelimit-remaining']) < 1:
				time.sleep(int(headers['X-Ratelimit-Reset']))

			child_data = response.json()
			#print(child_data)
			if len(child_data['jquery'][10][3][0]) != 0:
				for child in child_data['jquery'][10][3][0]:
					counter_obj.parse_response(child)
		else:
			print('Error: could not get child comments for the selected posts.')

	def get_all_comments(self, counter_obj):
		for post_id in self.post_id_list:
			self.get_post_comments(post_id, counter_obj)