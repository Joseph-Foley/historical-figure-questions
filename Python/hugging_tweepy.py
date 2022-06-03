# -*- coding: utf-8 -*-
"""
combines hugging face AI and twitter API (tweepy)
https://huggingface.co/deepset/roberta-base-squad2
https://towardsdatascience.com/my-first-twitter-app-1115a327349e
@AureliusRespon1
"""
# =============================================================================
# IMPORTS
# =============================================================================
import tweepy
import yaml
from transformers import pipeline #,TFAutoModelForQuestionAnswering, AutoTokenizer


# =============================================================================
# CONSTANTS
# =============================================================================
MODEL = "deepset/roberta-base-squad2"

# =============================================================================
# FUNCTIONS
# =============================================================================
# Setup access to API
def connect_to_twitter_OAuth(CONSUMER_KEY, CONSUMER_SECRET,\
                             ACCESS_TOKEN, ACCESS_SECRET):
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth)
    return api

# =============================================================================
# EXECUTE
# =============================================================================
#load model
nlp = pipeline('question-answering', model=MODEL, tokenizer=MODEL)

#load the context document
with open(r'C:\Users\JF\Desktop\git_projects\historical-figure-questions\Docs\Marcus_Aurelius.txt') as f:
    context = f.read()

context = context.replace('\n', ' ')

#load API creds
with open(r'C:\Users\JF\Desktop\git_projects\historical-figure-questions\Docs\twitter_creds_MA.yml', 'r') as file:
    twitter_creds =  yaml.safe_load(file)
    
##Variables that contains the credentials to access Twitter API
ACCESS_TOKEN = twitter_creds['ACCESS_TOKEN']
ACCESS_SECRET = twitter_creds['ACCESS_SECRET']
CONSUMER_KEY = twitter_creds['CONSUMER_KEY']
CONSUMER_SECRET = twitter_creds['CONSUMER_SECRET']

#Create API object
api = connect_to_twitter_OAuth()

#Get tweets from mentions
public_tweets = api.mentions_timeline()#since_id='1508117636026142727')#count=25)
tweet_texts = []
links = []
for tweet in public_tweets:
    print('\n-----', tweet.text)
    tweet_texts.append(tweet.text)
    
    #form url
    link = f'https://twitter.com/{tweet.author.screen_name}/status/{tweet.id_str}'
    print(link)
    links.append(link)
    
#For each tweet, generate a response and reply to them
for tweet in public_tweets:
    #get question
    question = tweet.text.strip('@AureliusRespon1 ')
    
    #generate a response
    QA_input = {'question': question, 'context': context}
    response = nlp(QA_input)
    print('Response generated')
    
    #reply
    link = f'https://twitter.com/{tweet.author.screen_name}/status/{tweet.id_str}'
    tweet_reply = api.update_status(status=f'@{tweet.author.screen_name} : ' +\
                                           response['answer'],\
                                    attachment_url=link)
        
    #log that this was replied to