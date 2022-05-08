import tweepy
import configparser
import pandas as pd

from modules import *

#key_assignment
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

#authentication 
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

#extracting data
api = tweepy.API(auth)

def getData():

    keywords = '@iamsrk'
    tweets = tweepy.Cursor(api.search_tweets, q=keywords, count=10, tweet_mode='extended').items(10)

    data = []
    # col = ['Time Created', 'User', 'Tweet', 'Sentiments', 'Reliability']

    # tweets_collection = api.home_timeline()
    for tweet in tweets:
        text = tweet.user.screen_name + ". " + tweet.full_text
        res = predict(preprocess("", text))
        res = "Real" if res == 1 else "Not Real"
        nested_list = [tweet.user.screen_name, tweet.created_at, tweet.full_text,  sentimentPrediction(text), res]
        data.append(nested_list)
        
    # df = pd.DataFrame(data, columns=col)
    return data

class Listener(tweepy.Stream):

    tweets = []
    limit = 1

    def on_status(self, status):
        if not status.truncated:
            self.tweets.append([status.user.screen_name, status.created_at, status.text])
        else:
            self.tweets.append([status.user.screen_name, status.created_at, status.extended_tweet['full_text']])
        # print(status.user.screen_name + ": " + status.text)
        if len(self.tweets) == self.limit:
            self.disconnect()
        
stream_tweet = Listener(api_key, api_key_secret, access_token, access_token_secret)

# stream by kewords
keywords = ['covid', 'news', 'bjp', 'congress', 'india', 'politics']
stream_tweet.filter(track=keywords)

print(stream_tweet.tweets)