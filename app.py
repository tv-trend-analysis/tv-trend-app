import pandas as pd
import tweepy
import re
import hidden
import string
from textblob import TextBlob
import textpre
 
#Twitter credentials for the app
consumer_key = hidden.key[0]
consumer_secret = hidden.key[1]
access_key= hidden.key[2]
access_secret = hidden.key[3]
 
#pass twitter credentials to tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
 

#columns of the csv file
COLS = ['id', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'place', 'place_coord_boundaries']
 
 
#method write_tweets()
def write_tweets(keyword, file):
    df = pd.DataFrame(columns=COLS)
    #page attribute in tweepy.cursor and iteration
    for page in tweepy.Cursor(api.search, q=keyword,
                              count=10, include_rts=False).pages(50):
        for status in page:
            new_entry = []
            status = status._json
 
            ## check whether the tweet is in english or skip to the next tweet
            if status['lang'] != 'en':
                continue
 

 
 
            #preprocessing
            filtered_tweet=textpre.clean_tweets(status['text'])
 
            #pass textBlob method for sentiment calculations
            blob = TextBlob(filtered_tweet)
            Sentiment = blob.sentiment
 
            #seperate polarity and subjectivity in to two variables
            polarity = Sentiment.polarity
            subjectivity = Sentiment.subjectivity
 
            #new entry append
            new_entry += [status['id'], status['text'],filtered_tweet, Sentiment,polarity,subjectivity, status['lang']]
  
            #get location of the tweet if possible
            try:
                location = status['user']['location']
            except TypeError:
                location = ''
            new_entry.append(location)
 
            try:
                coordinates = [coord for loc in status['place']['bounding_box']['coordinates'] for coord in loc]
            except TypeError:
                coordinates = None
            new_entry.append(coordinates)
 
            single_tweet_df = pd.DataFrame([new_entry], columns=COLS)
            df = df.append(single_tweet_df, ignore_index=True)
    csvFile = open(file, 'a' ,encoding='utf-8')
    df.to_csv(csvFile, mode='a', columns=COLS, index=False, encoding="utf-8")
 
#declare keywords as a query
querykeyword=input("Enter Query: ")
store_tweets = "data/"+querykeyword+".csv"
#call main method passing keywords and file path
write_tweets(querykeyword,store_tweets)