from flask import Flask, request
from dotenv import load_dotenv
from .derekscode import predict_technical
from .preprocess import Magic
from .sentiment import TS
import json
import os
from redis import Redis
from rq import Queue, Connection
from rq.worker import HerokuWorker as Worker

load_dotenv()

# EXAMPLE LAYOUT FOR RQ
# queue = rq.Queue('task-name', connection=conn)
# job = queue.enqueue('app.{module_name}.{function_name}', **args('{any_arguments_to_function}'))
# job.get_id()

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
    APP.config['REDISTOGO_URL'] = os.environ['REDISTOGO_URL']

    @APP.route('/')
    @APP.route('/api', methods=['GET', 'POST'])
    def functionality():
        # default to Facebook
        if request.method == 'POST':
            inp = request.values['ticker']
        elif request.method == 'GET':
            inp = request.values['ticker']
        else:
            inp = 'FB'

        # derek's technical analysis part
        y_prebro = predict_technical(inp)

        # twitter sentiment analysis
        twitter = TS(inp)
        sentiment = twitter.output_twitter()

        # facebook prophet + historical analysis
        magik = Magic(inp)
        historical = magik.output_historical()
        future = magik.output_future()

        json_obj = {'TA': {'sell': y_prebro[0][0], 'hold': y_prebro[0][1], 'buy': y_prebro[0][2]},
                    'Sentiment': {'sell': sentiment['Sell'], 'hold': sentiment['Hold'], 'buy': sentiment['Buy']},
                    'Historical': {'sell': historical['Sell'], 'hold': historical['Hold'], 'buy': historical['Buy']},
                    'Future': {'sell': future['Sell'], 'hold': future['Hold'], 'buy': future['Buy']}
        }
        response = json.dumps(json_obj)
        
        return response

    return APP