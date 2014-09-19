from textblob import TextBlob, Word
from twitter_config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_KEY
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import json
#from tweepy.streaming import StreamHandler

# api = twitter.Api(
# 	consumer_key = CONSUMER_KEY,
# 	cosumer_secret = CONSUMER_SECRET,
# 	access_token_key = ACCESS_KEY,
# 	access_token_secret = ACCESS_TOKEN
# 	)

class TwitterStreamListener(tweepy.StreamListener):
	'''
		Listener class which listens to the Streaming API
	'''

	def on_data(self, tweet):
	    t = json.loads(tweet)
            print "Tweet: ", t.get('text')
		#Do something with the on_data

	def on_error(self, status):
		print "Error: ", status


if __name__ == '__main__':
	auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_TOKEN)
	
	l = TwitterStreamListener()
	streamer = Stream(auth, listener = l)
	streamer.filter(track = ['#python'])

