from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Tweets(Base):
    __tablename__ = 'tweets'

    tweet_text = Column(String, primary_key=True)
    ticker = Column(String)