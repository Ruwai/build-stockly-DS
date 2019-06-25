from __future__ import unicode_literals
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dotenv import load_dotenv
from .tweetsDB import handler, postgres_params
from .tables import Tweets
from sqlalchemy import create_engine, select, or_, Column, Integer, String
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
import pandas as pd
import numpy as np
import os
import tweepy
import nltk

load_dotenv()

class TS(object):
    '''
        TwitterSentiment object wth one parameter being the stock ticker to search for.
    '''
    def __init__(self, ticker):
        # tweepy setup
        access_token = os.environ['ACCESS_TOKEN']
        access_secret = os.environ['ACCESS_SECRET']
        consumer_key = os.environ['CONSUMER_KEY']
        consumer_secret = os.environ['CONSUMER_SECRET']

        auth = tweepy.OAuthHandler(consumer_key,
                                   consumer_secret)
        auth.set_access_token(access_token,
                              access_secret)

        self.api = tweepy.API(auth)
        self.ticker = ticker.upper()

    def make_df_with_magic(self):
        api = self.api
        symbol = self.ticker
        sid = SentimentIntensityAnalyzer()
        max_tweets = 200

        tweets = [status for status in tweepy.Cursor(api.search,
                                                     q=str(symbol),
                                                     result_type="recent",
                                                     tweet_mode="extended",
                                                     lang="en").items(max_tweets)]

        data = pd.DataFrame(data=[tweet.full_text for tweet in tweets], columns = ['Tweets'])
        n_list = []

        for index, row in data.iterrows():
            s_pol = sid.polarity_scores(row['Tweets'])
            n_list.append(s_pol)

        series = pd.Series(n_list)
        data['polarity'] = series.values

        return data

    def add_stock_tweets_to_db(self):
        api = self.api
        symbol = self.ticker

        handler(symbol)
        print('New {} Tweets added to Database'.format(symbol))

    def make_df_from_db(self):
        api = self.api
        symbol = self.ticker
        sid = SentimentIntensityAnalyzer()
        DB_uri = URL(**postgres_params)
        engine = create_engine(DB_uri)
        Session = sessionmaker(bind=engine)
        session = Session()
        select_statement = session.query(Tweets).filter_by(ticker=symbol).statement
        data = pd.read_sql(select_statement, session.bind)

        n_list = []

        for index, row in data.iterrows():
            s_pol = sid.polarity_scores(row['tweet_text'])
            n_list.append(s_pol)

        series = pd.Series(n_list)
        data['polarity'] = series.values

        return data

    def output_twitter(self):
        data = self.make_df_from_db()

        neg = []
        neu = []
        pos = []
        compound = []

        pol = data['polarity']

        for i in range(0, len(pol)):
            neg.append(pol[i]['neg'])
            neu.append(pol[i]['neu'])
            pos.append(pol[i]['pos'])
            compound.append(pol[i]['compound'])

        def softmax(x):
            """Compute softmax values for each sets of scores in x."""
            e_x = np.exp(x - np.max(x))
            return e_x / e_x.sum(axis=0)

        sell = sum(neg)
        buy = sum(pos)
        comp = sum(compound)

        scores = [sell, comp, buy]
        values = softmax(scores)
        keys = ['Sell', 'Hold', 'Buy']

        twitter_sentiment_analysis = dict(zip(keys, values))

        return twitter_sentiment_analysis