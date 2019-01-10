# Classes
from wordcount.reddit_api import Reddit_API
from wordcount.counter import Counter

# Settings
from wordcount.settings import BANNER

class Shell:
	""" shell for user to choose a sub and number of posts to analyze """

	def __init__(self):
		self.connection = Reddit_API()

		if self.connection.authorized:
			self.run()
		else:
			print('\nError: Could not connect to the Reddit API')

	def run(self):
		print(BANNER)

		while 1:
			command = input('Choose a subreddit to analyze (leave blank to search all subreddits):\n/r/')

			if command == '':
				self.connection.subreddit = '/r/all'
			else:
				self.connection.subreddit = '/r/' + command.strip()

			valid_input = False
			num_posts = 25 # default value
			while not valid_input:
				num_posts = input('Number of posts to be analyzed from ' + self.connection.subreddit + ' (default: 25, maximum: 100): ')

				try:
					num_posts = int(num_posts.strip())

					if int(num_posts) > 100:
						print('Error: cannot collect more than 100 posts at a time.')
					elif int(num_posts) < 1:
						print('Error: number of posts to analyze must be at least 1.')
					else:
						valid_input = True
				
				except ValueError:
					if len(num_posts) == 0:
						num_posts = 25
						valid_input = True
					else:
						print('Error: please enter a number.')
			
			self.counter = Counter()
			
			self.connection.get_subreddit_posts(num_posts, self.counter)
			self.connection.get_all_comments(self.counter)

			print('-' * 40)
			print('{:^40s}'.format('Top 15 words'))
			print('-' * 40)
			print(self.counter)
			print()
