# Reddit Word Count Bot

Simple bot to count the most used words for a given subreddit.

>This program does not use PRAW, the common python wrapper for the Reddit API. The purpose of this project was to familiarize myself with HTTP requests in python and lexical analysis.

## Usage

### Installation

Create a reddit developer account. Instructions on how to set up that account can be found [here](https://github.com/reddit-archive/reddit/wiki/OAuth2).

Edit settings.py with information specific to your account

Clone the repository: `git clone https://github.com/jrdavison/wordcount-bot.git`

Install required packages: `pip install -r requirements.txt`

In the root of the repository run the wordcount.py file:
`python wordcount.py`
 
### Reference
- [Reddit API](https://www.reddit.com/dev/api/)
