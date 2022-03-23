# -*- coding: utf-8 -*-
"""
sandbox for tweepy lib
https://towardsdatascience.com/my-first-twitter-app-1115a327349e

"""
import tweepy
import yaml
#load details
with open(r'C:\Users\JF\Desktop\git_projects\historical-figure-questions\Docs\twitter_creds.yml', 'r') as file:
    twitter_creds =  yaml.safe_load(file)


# Variables that contains the credentials to access Twitter API
ACCESS_TOKEN = twitter_creds['ACCESS_TOKEN']
ACCESS_SECRET = twitter_creds['ACCESS_SECRET']
CONSUMER_KEY = twitter_creds['CONSUMER_KEY']
CONSUMER_SECRET = twitter_creds['CONSUMER_SECRET']


# Setup access to API
def connect_to_twitter_OAuth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth)
    return api


# Create API object
api = connect_to_twitter_OAuth()


# tweets from my stream
public_tweets = api.home_timeline()
tweet_text = []
for tweet in public_tweets:
    print('\n-----', tweet.text)
    tweet_text.append(tweet.text)
    
#replying to a tweet
#https://docs.tweepy.org/en/stable/api.html#post-retrieve-and-engage-with-tweets
#API.update_status
#api.update_status(status='Just testing out the tweepy library to interact with the twitter API')
api.update_status(status='@CryptoWhale Dats Rite!',
                  in_reply_to_status_id='1506711629618159616')


import yaml
