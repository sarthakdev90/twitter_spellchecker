from textblob import TextBlob, Word
from twitter_config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_KEY
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import json

crunched_words = 0
corrected = 0

class TwitterStreamListener(tweepy.StreamListener):
	'''
		Listener class which listens to the Streaming API
	'''

	def on_data(self, tweet):
	    t = json.loads(tweet).get('text').encode('utf-8')
            print "Tweet: ", t
	    if t:
	        sent = TextBlob(t)
	        words = sent.words
		for w in words:
		    global crunched_words, corrected
		    crunched_words += 1
		    wor = Word(w)
		    if len(wor.spellcheck()) != 1:
		        corrected += 1
		#Do something with the on_data
	    print "Crunched Words: ", crunched_words
	    print "Corrected: ", corrected

	def on_error(self, status):
		print "Error: ", status


if __name__ == '__main__':
	auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_TOKEN)
	
	l = TwitterStreamListener()
	streamer = Stream(auth, listener = l)
	streamer.filter(track = ['#mufc'])

