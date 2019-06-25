from flask import Flask, request
import json
import pickle
import os
from sklearn.preprocessing import StandardScaler
from pathlib import Path
from .preprocess import Magic
from .sentiment import TS
from .derekscode import generate_df
from dotenv import load_dotenv

load_dotenv()

def create_app():
    APP = Flask(__name__)
    APP.config['ALPHAVANTAGE_API_KEY'] = os.environ['ALPHAVANTAGE_API_KEY']
    APP.config['ACCESS_TOKEN'] = os.environ['ACCESS_TOKEN']
    APP.config['ACCESS_SECRET'] = os.environ['ACCESS_SECRET']
    APP.config['CONSUMER_KEY'] = os.environ['CONSUMER_KEY']
    APP.config['CONSUMER_SECRET'] = os.environ['CONSUMER_SECRET']
    APP.config['PG_HOSTNAME'] = os.environ['PG_HOSTNAME']
    APP.config['PG_PORT'] = os.environ['PG_PORT']
    APP.config['PG_USERNAME'] = os.environ['PG_USERNAME']
    APP.config['PG_PASSWORD'] = os.environ['PG_PASSWORD']
    APP.config['PG_DBNAME'] = os.environ['PG_DBNAME']

    @APP.route('/')
    @APP.route('/api', methods=['GET','POST'])
    def functionality():
        model_path = Path(__file__).parent.resolve()
        model = pickle.load(open(os.path.join(model_path, "new_model.p"), "rb"))

        inp = 'FB'
        if request.method == 'POST':
            inp = request.values['ticker']
        market_df = generate_df(inp)

        market_df = market_df.dropna()
        X = market_df[['5. volume', 'MACD', 'AROONOSC','MACD_Hist', 'MACD_Signal', 'DX', 'SlowD', 'SlowK']]
        sc = StandardScaler()
        X = sc.fit_transform(X)
        y_prebro = model.predict_proba(X[0].reshape(1, -1))

        twitter = TS(inp)
        sentiment = twitter.output_twitter()

        magik = Magic(inp)
        historical = magik.output_historical()
        future = magik.output_future()

        json_obj = {'TA': {'sell':y_prebro[0][0], 'hold':y_prebro[0][1], 'buy':y_prebro[0][2]},
                    'Sentiment': {'sell':sentiment['Sell'], 'hold':sentiment['Hold'], 'buy':sentiment['Buy']},
                    'Historical': {'sell':historical['Sell'], 'hold':historical['Hold'], 'buy':historical['Buy']},
                    'Future': {'sell':future['Sell'], 'hold':future['Hold'], 'buy':future['Buy']}
                    }

        response = json.dumps(json_obj)
        return response

    return APP