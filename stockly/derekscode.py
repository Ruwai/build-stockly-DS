import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from sklearn.preprocessing import StandardScaler
from pathlib import Path
import requests
import pickle
import os

ALPHAVANTAGE_API_KEY = os.environ['ALPHAVANTAGE_API_KEY']

def generate_df(ticker):

    macd = 'https://www.alphavantage.co/query?function=MACD&symbol=' + ticker + '&interval=daily&series_type=open&apikey=SXG08DL4S2EW8SKC'
    response1 = requests.get(macd)
    df_macd = pd.DataFrame.from_dict(response1.json()['Technical Analysis: MACD']).T

    stoch = 'https://www.alphavantage.co/query?function=STOCH&symbol=' + ticker + '&interval=daily&apikey=SXG08DL4S2EW8SKC'
    response2 = requests.get(stoch)
    df_stoch = pd.DataFrame.from_dict(response2.json()['Technical Analysis: STOCH']).T

    aroon = 'https://www.alphavantage.co/query?function=AROONOSC&symbol=' + ticker + '&interval=daily&time_period=10&apikey=SXG08DL4S2EW8SKC'
    response4 = requests.get(aroon)
    df_aroon = pd.DataFrame.from_dict(response4.json()['Technical Analysis: AROONOSC']).T

    dx = 'https://www.alphavantage.co/query?function=DX&symbol=' + ticker + '&interval=daily&time_period=10&apikey=SXG08DL4S2EW8SKC'
    response5 = requests.get(dx)
    df_dx = pd.DataFrame.from_dict(response5.json()['Technical Analysis: DX']).T

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&interval=5min&outputsize=full&apikey=SXG08DL4S2EW8SKC'
    response6 = requests.get(url)
    df = pd.DataFrame.from_dict(response6.json()['Time Series (Daily)']).T

    df = df.join(df_macd)
    df = df.join(df_stoch)
    df = df.join(df_aroon)
    df = df.join(df_dx)

    return df

def predict_technical(ticker):

    model_path = Path(__file__).parent.resolve()
    model = pickle.load(open(os.path.join(model_path, "new_model.p"), "rb"))

    market_df = generate_df(ticker)
    market_df = market_df.dropna()
    X = market_df[['5. volume', 'MACD', 'AROONOSC','MACD_Hist', 'MACD_Signal', 'DX', 'SlowD', 'SlowK']]
    sc = StandardScaler()
    X = sc.fit_transform(X)
    y_prebro = model.predict_proba(X[0].reshape(1, -1))

    return y_prebro