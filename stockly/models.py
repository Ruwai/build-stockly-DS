from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class Tweets(DB.Model):
    """Tweets."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    ticker = DB.Column(DB.String)