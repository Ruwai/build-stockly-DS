import os
import time
import tweepy
from dotenv import load_dotenv
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect
from .tables import Tweets

load_dotenv()

HOST = os.environ['PG_HOSTNAME']
PORT = os.environ['PG_PORT']
USER = os.environ['PG_USERNAME']
PASS = os.environ['PG_PASSWORD']
NAME = os.environ['PG_DBNAME']
TABLE = 'tweets'

access_token = os.environ['ACCESS_TOKEN']
access_secret = os.environ['ACCESS_SECRET']
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

API = tweepy.API(auth)

postgres_params = dict(
            drivername='postgres',
            username=USER,
            password=PASS,
            host=HOST,
            port=PORT,
            database=NAME
)

def handler(symbol):

    url = URL(**postgres_params)
    print('>>> engine url created')
    engine = create_engine(url)
    print('>>> engine instantiated')
    Session = sessionmaker(bind=engine)
    print('>>> engine binded to sessionmaker')
    session = Session()
    print('>>> Session instantiated')

    if TABLE not in inspect(engine).get_table_names():
        raise Exception("Unable to find the table '%s' in '%s'".format(TABLE, url))
    else:
        print(">>> Inserting data into table : ",  TABLE)

    count = 0
    max_tweets = 200
    tweets = [status for status in tweepy.Cursor(API.search,
                                                 q=str(symbol),
                                                 result_type="recent",
                                                 tweet_mode="extended",
                                                 lang="en").items(max_tweets)]

    for tweet in tweets:
        row = Tweets(
            tweet_text=tweet.full_text,
            ticker=str(symbol)
        )
        session.add(row)
        N = 50
        count+=1
        if count % N == 0:
            print('>>> {} New rows are being inserted into table : {}'.format(count, TABLE))
            print('>>> Committing to table: ', TABLE)
            session.commit()

    session.close()
    engine.dispose()