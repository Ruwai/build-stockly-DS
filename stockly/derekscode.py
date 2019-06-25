import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import requests
import os

ALPHAVANTAGE_API_KEY = os.environ['ALPHAVANTAGE_API_KEY']

def generate_df(ticker):

    macd = 'https://www.alphavantage.co/query?function=MACD&symbol=' + ticker + '&interval=daily&series_type=open&apikey=SXG08DL4S2EW8SKC'
    response1 = requests.get(macd)
    if "Note" in response1.json().keys():
        return (response1.json()["Note"])
    df_macd = pd.DataFrame.from_dict(response1.json()['Technical Analysis: MACD']).T

    stoch = 'https://www.alphavantage.co/query?function=STOCH&symbol=' + ticker + '&interval=daily&apikey=SXG08DL4S2EW8SKC'
    response2 = requests.get(stoch)
    if "Note" in response2.json().keys():
        return (response2.json()["Note"])
    df_stoch = pd.DataFrame.from_dict(response2.json()['Technical Analysis: STOCH']).T

    aroon = 'https://www.alphavantage.co/query?function=AROONOSC&symbol=' + ticker + '&interval=daily&time_period=10&apikey=SXG08DL4S2EW8SKC'
    response4 = requests.get(aroon)
    if "Note" in response4.json().keys():
        return (response4.json()["Note"])
    df_aroon = pd.DataFrame.from_dict(response4.json()['Technical Analysis: AROONOSC']).T

    dx = 'https://www.alphavantage.co/query?function=DX&symbol=' + ticker + '&interval=daily&time_period=10&apikey=SXG08DL4S2EW8SKC'
    response5 = requests.get(dx)
    if "Note" in response5.json().keys():
        return (response5.json()["Note"])
    df_dx = pd.DataFrame.from_dict(response5.json()['Technical Analysis: DX']).T

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&interval=5min&outputsize=full&apikey=SXG08DL4S2EW8SKC'
    response6 = requests.get(url)
    if "Note" in response6.json().keys():
        return (response6.json()["Note"])
    df = pd.DataFrame.from_dict(response6.json()['Time Series (Daily)']).T

    df = df.join(df_macd)
    df = df.join(df_stoch)
    df = df.join(df_aroon)
    df = df.join(df_dx)

    return df