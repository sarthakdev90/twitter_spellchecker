from flask import Flask, render_template
from api import get_numbers, TwitterStreamListener
from twitter_config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_KEY
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    numbers = get_numbers()
    return render_template('index.html', numbers = numbers)


if __name__ =='__main__':
	try:
	    app.run()
   	    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	    auth.set_access_token(ACCESS_KEY, ACCESS_TOKEN)
		
	    l = TwitterStreamListener()
	    streamer = Stream(auth, listener = l)
	    streamer.filter(track = ['#mufc'])

	except Exception as e:
	    print traceback.format_exc(e)
    
