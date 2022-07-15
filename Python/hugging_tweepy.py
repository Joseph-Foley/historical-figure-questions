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
import pandas as pd
from transformers import pipeline 

pd.set_option('display.max_columns', 14)
pd.set_option('display.expand_frame_repr', False)

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
#load records
records = pd.read_csv('../Docs/reply_records.csv')
records.to_csv('../Docs/reply_records_BACKUP.csv')

#load model
nlp = pipeline('question-answering', model=MODEL, tokenizer=MODEL)

#load the context document
with open('../Docs/Marcus_Aurelius.txt') as f:
    context = f.read()

context = context.replace('\n', ' ')

#load API creds
with open('../Docs/twitter_creds_MA.yml', 'r') as file:
    twitter_creds =  yaml.safe_load(file)
    
##Variables that contains the credentials to access Twitter API
ACCESS_TOKEN = twitter_creds['ACCESS_TOKEN']
ACCESS_SECRET = twitter_creds['ACCESS_SECRET']
CONSUMER_KEY = twitter_creds['CONSUMER_KEY']
CONSUMER_SECRET = twitter_creds['CONSUMER_SECRET']

#Create API object
api = connect_to_twitter_OAuth(CONSUMER_KEY, CONSUMER_SECRET,\
                               ACCESS_TOKEN, ACCESS_SECRET)

#Get tweets from mentions
public_tweets = api.mentions_timeline()
tweet_texts = []
links = []
for tweet in public_tweets:
    print('\n-----', tweet.text)
    tweet_texts.append(tweet.text)
    
    #form url
    link = f'https://twitter.com/{tweet.author.screen_name}/status/{tweet.id_str}'
    print(link)
    links.append(link)

new_records = []   
#For each tweet, generate a response and reply to them
for tweet in public_tweets:
    #get question and link
    question = tweet.text.strip('@AureliusRespon1 ')
    link = f'https://twitter.com/{tweet.author.screen_name}/status/{tweet.id_str}'
    
    #do not respond if already done so
    if link in records['Link'].values:
        print(f'\nAlready Answered: {question}')
        continue
        
    else:
        print(f'Question: {question}')
    
    #generate a response
    QA_input = {'question': question, 'context': context}
    response = nlp(QA_input)
    print(f'Response generated: {response["answer"]}')
    
    #reply
    tweet_reply = api.update_status(status=f'@{tweet.author.screen_name} : ' +\
                                           response['answer'],\
                                    attachment_url=link)
        
    #log that this was replied to
    new_records.append([tweet.author.screen_name, question, response['answer'], link])
    
#save log
records = pd.concat([records,
                     pd.DataFrame(new_records, columns=records.columns)])

records.to_csv('../Docs/reply_records.csv', index=False)