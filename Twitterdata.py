from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import io
import json

ACCESS_TOKEN = "3112185708-dOGIAGPvqrgs6nBTOSiqh5JygvWKIF9AzVmqf6H"
ACCESS_TOKEN_SECRET = "cZ08nrUL70BfwaJrqfwbYkJjIXbrSLCUflglBsbR6rNHe"
CONSUMER_KEY = "HU2wusYStZAznrJ1fedu87zm0"
CONSUMER_SECRET = "0kLc4RqWGqkxHNaYHBlIBAuaWT6VNurIZULms8loJET1SQBpVp"

class TwitterClient():
    def __init__(self, twitter_user,fetched_tweets_filename):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
        self.fetched_tweets_filename = fetched_tweets_filename

    def get_user_timeline_tweets(self,num_tweets):
        with io.open(fetched_tweets_filename, "w", encoding="utf-8") as tf:
            tf.write('[')
        oldest=''
        c=0
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(200):
            c+=1
            t=tweet._json
            with io.open(fetched_tweets_filename, "a", encoding="utf-8") as tf:
                json.dump(t,tf)
                if c<num_tweets:
                    tf.write(',')
            if c%200==0:
                oldest=tweet.id-1
            num_tweets-=1
            print(c)
            if num_tweets<=0:
                with io.open(fetched_tweets_filename, "a", encoding="utf-8") as tf:
                    tf.write(']')
                return True
        while(1):
            for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user,max_id=oldest).items(200):
                c+=1
                t=tweet._json
                with io.open(fetched_tweets_filename, "a", encoding="utf-8") as tf:
                    json.dump(t,tf)
                    if c<num_tweets:
                        tf.write(',')
                if c%200==0:
                    oldest=tweet.id-1
                num_tweets-=1
                print(c)
                if num_tweets<=0:
                    with io.open(fetched_tweets_filename, "a", encoding="utf-8") as tf:
                        tf.write(']')
                    return True
        return True


class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth



if __name__ == '__main__':
    fetched_tweets_filename = "tweets.json"
    num_tweets=int(input("Enter the number of tweets"))
    twitter_client = TwitterClient('PMOIndia',fetched_tweets_filename)
    print(twitter_client.get_user_timeline_tweets(num_tweets))
