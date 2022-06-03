# -*- coding: utf-8 -*-
"""
sandbox for tweepy lib
https://towardsdatascience.com/my-first-twitter-app-1115a327349e
@AureliusRespon1
"""
import tweepy
import yaml
#load details
with open(r'C:\Users\JF\Desktop\git_projects\historical-figure-questions\Docs\twitter_creds_MA.yml', 'r') as file:
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
public_tweets = api.home_timeline()#since_id='1508117636026142727')#count=25)
tweet_text = []
links = []
for tweet in public_tweets:
    print('\n-----', tweet.text)
    tweet_text.append(tweet.text)
    
    #form url
    link = f'https://twitter.com/{tweet.author.screen_name}/status/{tweet.id_str}'
    print(link)
    links.append(link)
    
#replying to a tweet
#https://docs.tweepy.org/en/stable/api.html#post-retrieve-and-engage-with-tweets
#API.update_status
#api.update_status(status='Just testing out the tweepy library to interact with the twitter API')
api.update_status(status='@CryptoWhale Dats Rite!',
                  in_reply_to_status_id='1506711629618159616')


#show tweet and reply (actual thing should include their @ handle)
url = r'https://twitter.com/CryptoWhale/status/1506711629618159616'
api.update_status(status='Correct!',
                  attachment_url=url)

# =============================================================================
# WAS DEFAULT BUT NOW IT IS NOT, WILL USE V1.1 INSTEAD
# #V2 API
# BEARER_TOKEN = twitter_creds['BEARER_TOKEN']
# 
# client = tweepy.Client(BEARER_TOKEN, CONSUMER_KEY, CONSUMER_SECRET,\
#                        ACCESS_TOKEN, ACCESS_SECRET)
#     
#     
# public_tweets = client.get_home_timeline(tweet_fields=['author_id'])
# 
# tweet_text = []
# links = []
# for tweet in public_tweets[0]:
#     print('\n-----', tweet)
#     tweet_text.append(tweet.text)
#     
#     #form url
#     link = f'https://twitter.com/{tweet.author_id}/status/{tweet.id}'
#     print(link)
#     links.append(link)
#     
#     
# client.create_tweet(text='Indeed')#, quote_tweet_id=1530188537324240899)
#     
# =============================================================================
    