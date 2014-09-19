from textblob import TextBlob, Word
from twitter_config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_KEY
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import tweepy, redis
import json, traceback
from collections import Counter

numbers_db = redis.Redis(db = 10)
incorrect_words_db = redis.Redis(db = 11)

class TwitterStreamListener(tweepy.StreamListener):
	'''
		Listener class which listens to the Streaming API
	'''

	def on_data(self, tweet):
		try:
		    t = json.loads(tweet).get('text').encode('utf-8')
	            print "Tweet: ", t
		    numbers_db.incr("tweets")
		    if t:
		        sent = TextBlob(t)
		        words = sent.words
			for w in words:
			    numbers_db.incr("words")
			    wor = Word(w)
			    if len(wor.spellcheck()) != 1:
			        incorrect_words_db.rpush("words", w)
			        numbers_db.incr("mistakes")
			#Do something with the on_data
		    mistakes = incorrect_words_db.lrange("words", 0, -1)
		    counter = Counter(mistakes)
		    
		    print "Crunched Tweets: ", numbers_db.get("tweets")
		    print "Crunched Words: ", numbers_db.get("words") 
		    print "Corrected: ", numbers_db.get("mistakes")
		    print "Most common: ", counter.most_common()[0][0]
		except Exception as e:
			print traceback.format_exc()

	def on_error(self, status):
		print "Error: ", status


if __name__ == '__main__':
	try:
		auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_TOKEN)
		
		l = TwitterStreamListener()
		streamer = Stream(auth, listener = l)
		streamer.filter(track = ['#mufc'])

	except Exception as e:
		print traceback.format_exc(e)

