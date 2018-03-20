from pandas_datareader import data
import pandas as pd
tickers = ['AAPL', 'MSFT', 'MMM', 'TSLA',
           'DE', 'HD', 'UNP', 'CAT', 'GS', 'COST']
data_source = 'morningstar'
start_date = '2017-01-01'
end_date = '2017-12-31'
panel_data = data.DataReader(tickers, data_source, start_date, end_date)
panel_data.to_csv("prices.csv")
