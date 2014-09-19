from textblob import TextBlob, Word
from twitter_config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_KEY
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import tweepy, redis
import json, traceback, re
from collections import Counter

numbers_db = redis.Redis(db = 10)
incorrect_words_db = redis.Redis(db = 11)

class TwitterStreamListener(tweepy.StreamListener):
	'''
		Listener class which listens to the Streaming API
	'''
	
	def process(self, tweet):
		'''
			Function to process a tweet.
		'''
		try:
		    t = json.loads(tweet).get('text').encode('utf-8')
	            print "Tweet: ", t
		    numbers_db.incr("tweets")
		    if t:
		        sent = TextBlob(t)
		        words = [i for i in sent.words if i != 'RT' and not i.startswith('@') and not self.is_link(i)]
		        print "Words: ", words
			for w in words:
			    numbers_db.incr("words")
			    wor = Word(w)
			    checks = [i[0] for i in wor.spellcheck()] 
			    if w not in checks:
			        incorrect_words_db.rpush("mistakes", w)
			return True
			
		except Exception as e:
			print traceback.format_exc(e)
			return False
			
	def is_link(self, token):
		'''
			Function to check whether the given token is a link or not
		'''
		return re.match('http(s){0,1}://.+\..+', token, re.I) is not None
			
			
	def on_data(self, tweet):
		'''
			This function gets called whenever the Streaming API finds data
		'''
		try:
		    self.process(tweet)
		    mistakes = incorrect_words_db.lrange("mistakes", 0, -1)
		    counter = Counter(mistakes)
		    
		    print "Crunched Tweets: ", numbers_db.get("tweets")
		    print "Crunched Words: ", numbers_db.get("words") 
		    print "Corrected: ", incorrect_words_db.llen("mistakes")
		    print "Most common: ", counter.most_common()[0][0]
		    
		except Exception as e:
			print traceback.format_exc()

	def on_error(self, status):
		'''
			This function gets called whenever the Streaming API encounters an error
		'''
		print "Error: ", status

def get_numbers():
	try:
	    mistakes = incorrect_words_db.lrange("mistakes", 0, -1)
	    counter = Counter(mistakes)
	    
	    numbers = {
		    "tweets" : numbers_db.get("tweets"),
		    "words" : numbers_db.get("words"), 
		    "corrected" : incorrect_words_db.llen("mistakes"),
		    "most_common": counter.most_common()[0][0]
			}
		return numbers
	except Exception as e:
		print traceback.format_exc()

if __name__ == '__main__':
	try:
		auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_TOKEN)
		
		l = TwitterStreamListener()
		streamer = Stream(auth, listener = l)
		streamer.filter(track = ['#mufc'])

	except Exception as e:
		print traceback.format_exc(e)

