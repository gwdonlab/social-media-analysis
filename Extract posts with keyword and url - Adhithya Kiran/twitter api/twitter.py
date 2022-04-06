
#%%
#from tweepy import *
from credentials import *

import tweepy
from time import sleep
 
import pandas as pd
import csv
import re 
import string
import preprocessor as p

#%%
 
consumer_key = 'xSh8QKijNpCVCAz8SfC0vAax3'
consumer_secret = 'eAnkQQhCbm7LbGZzJZ4bjykNdpQ31ygvzpML9fquDE490avfhA'
access_key= '1505336309065424908-CJx9O2IEukeycT3Nm2cet1eY89R6tj'
access_secret = 'wnoq7Eh81nDVfeadY0zzfAGrJ0dTOn1rcD2vUbTJlLPb8'
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
 
api = tweepy.API(auth,wait_on_rate_limit=True)
 
csvFile = open('file-name', 'a')
csvWriter = csv.writer(csvFile)
 
search_words = "kill putin http://"      # enter your words
new_search = search_words + " -filter:retweets"
 
for tweet in tweepy.Cursor(api.search_tweets,q=new_search,count=1000,
                           lang="en",
                           since_id=0).items():
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8'),tweet.user.screen_name.encode('utf-8'), tweet.user.location.encode('utf-8')])



# %%
