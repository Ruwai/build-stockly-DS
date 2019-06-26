from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from .tweetsDB import handler, postgres_params
from .tables import Tweets

def ticker_exists_in_DB(symbol):
    url = URL(**postgres_params)
    print('>>> engine url created')
    engine = create_engine(url)
    print('>>> engine instantiated')
    Session = sessionmaker(bind=engine)
    print('>>> engine binded to sessionmaker')
    session = Session()
    print('>>> Session instantiated')

    if session.query(Tweets).filter(Tweets.ticker == symbol).first() is None:
        handler(symbol)

    else:
        pass