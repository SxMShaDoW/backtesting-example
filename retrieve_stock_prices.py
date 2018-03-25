from pandas_datareader import data
import pandas as pd
from twitter_tickers import tickers
from config import folder

data_source = 'morningstar'
start_date = '2017-01-01'
end_date = '2017-12-31'

if __name__ == "__main__":
    """ try to retrieve the prices for each stock ticker """
    try:
        panel_data = data.DataReader(
            tickers, data_source, start_date, end_date)
        panel_data.to_csv(folder + "prices.csv")
    except Exception as e:
        print(e)
