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
def loadRecords(records_path='../Docs/reply_records.csv',\
                backup_path='../Docs/reply_records_BACKUP.csv'):
    '''
    load records of previously recorded tweets so that we dont respond to 
    tweets where we already did so
    '''
    #load records
    records = pd.read_csv(records_path)
    
    #save a backup (as records will later be overwritten)
    records.to_csv(backup_path)
    
    return records

def loadModelObjects(source=MODEL, context_path='../Docs/Marcus_Aurelius.txt'):
    '''
    Gets model from huggingface (first time run of this function will require
    a download >1Gb.) Load context for the model to draw from.

    Parameters
    ----------
    source : str, optional
        The default is MODEL. 
        Question Answering NLP model to pull from huggingface.
    context_path : str, optional
        The default is '../Docs/Marcus_Aurelius.txt'. 
        Path to the context for model to draw from.

    Returns
    -------
    qa_model : model object
        model to answer tweets
    context : str
        text for model to draw from
    '''
    #load model
    qa_model = pipeline('question-answering', model=source, tokenizer=source)
    
    #load the context document
    with open(context_path) as f:
        context = f.read()
    
    context = context.replace('\n', ' ')
    
    return qa_model, context
    
def connectTwitter(yml_path='../Docs/twitter_creds_MA.yml'):
    '''
    Connects to twitter api (v1.1) using user provided credentials (yaml)

    Parameters
    ----------
    yml_path : str, optional
        The default is '../Docs/twitter_creds_MA.yml'.
        path to yaml file containing credentials needed to access twitter api
        
    Returns
    -------
    api : api object
        object used to interact with twitte
    '''
    #load API creds
    with open(yml_path, 'r') as file:
        twitter_creds =  yaml.safe_load(file)
        
    #Variables that contains the credentials to access Twitter API
    ACCESS_TOKEN = twitter_creds['ACCESS_TOKEN']
    ACCESS_SECRET = twitter_creds['ACCESS_SECRET']
    CONSUMER_KEY = twitter_creds['CONSUMER_KEY']
    CONSUMER_SECRET = twitter_creds['CONSUMER_SECRET']
    
    #authenticate
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    
    #return api object
    api = tweepy.API(auth)
    
    return api



# =============================================================================
# EXECUTE
# =============================================================================
if __name__ =='__main__':
    #load recorded tweets
    records = loadRecords()
    
    #load model and context
    qa_model, context = loadModelObjects()
    
    #connect to twitter api
    api = connectTwitter()
    
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
        response = qa_model(QA_input)
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