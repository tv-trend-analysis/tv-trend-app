import pandas as pd
import tweepy
import hidden
from textblob import TextBlob
import textpre  #user defined library for text preprocessing
import trans  # google translate library

returnlist=[]

# Twitter credentials for the app
consumer_key = hidden.key[0]
consumer_secret = hidden.key[1]
access_key = hidden.key[2]
access_secret = hidden.key[3]

# pass twitter credentials to tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# columns of the csv file
COLS = ['id', 'original_text', 'clean_text', 'sentiment', 'polarity', 'subjectivity', 'lang', 'place',
        'place_coord_boundaries']

total_polarity = 0
total_subjectivity = 0


# method write_tweets()
def write_tweets(keyword, file):
    global total_polarity, total_subjectivity
    q = keyword + ' -filter:retweets'
    df = pd.DataFrame(columns=COLS)
    # page attribute in tweepy.cursor and iteration
    for page in tweepy.Cursor(api.search, q, count=5, include_rts=False).pages(5):

        for status in page:
            new_entry = []
            status = status._json

            # preprocessing
            filtered_tweet = textpre.clean_tweets(status['text'])

            # check whether the tweet is in english or skip to the next tweet
            if status['lang'] != 'en':
                filtered_tweet = trans.trans(filtered_tweet)

            # pass textBlob method for sentiment calculations
            blob = TextBlob(filtered_tweet)
            Sentiment = blob.sentiment

            # seperate polarity and subjectivity in to two variables
            polarity = Sentiment.polarity
            subjectivity = Sentiment.subjectivity

            # new entry append
            new_entry += [status['id'], status['text'], filtered_tweet, Sentiment, polarity, subjectivity,
                          status['lang']]

            # calculating total polarity
            total_polarity += polarity

            # calculating total subjectivity
            total_subjectivity += subjectivity

            # get location of the tweet if possible
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
    df["polarity"] = pd.to_numeric(df["polarity"], errors='coerce')
    df["subjectivity"] = pd.to_numeric(df["subjectivity"], errors='coerce')
    csvFile = open(file, 'a', encoding='utf-8')
    df.to_csv(csvFile, mode='a', columns=COLS, index=False, encoding="utf-8")
    no_of_rows=len(df)
    returnlist.append(str(no_of_rows))
    avgpol=total_polarity/no_of_rows
    returnlist.append(str(avgpol))
    avgsub= total_subjectivity/no_of_rows
    returnlist.append(str(avgsub))
    if avgpol>0:
        returnlist.append('Positive')
    elif avgpol==0:
        returnlist.append('Neutral')
    else:
        returnlist.append('Negative')


def main(query):
    querykeyword = query
    store_tweets = "data/" + querykeyword + ".csv"
    # call main method passing keywords and file path
    write_tweets(querykeyword, store_tweets)
    return returnlist
