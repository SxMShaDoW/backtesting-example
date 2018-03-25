# Stock backtesting with twitter sentiment

## Pre-reqs

* Python 3.5.2 +
* pip 3+
* virtualenv (optional, but recommended)
* `pip3 install tweepy`
* `pip3 install pandas`
* `pip3 install flask`

### Setup

1.  `git clone` this repo.
2.  Create a `secrets.py` file at the root
3.  Place your `consumer_key = 'XXXX'` in the `secrets.py`
4.  Place your `consumer_secret = 'XXX'` in the `secrets.py`
5.  Modify the `twitter_tickers.py` for all the stocks/twitter accounts you care about

### Run once

1.  `python twitter_tweets_retrieval.py` will retrieve pull all tweets from stock accounts and place them in individual .json files + csv (for backup).
2.  `python retrieve_stock_prices.py` will pull the stock prices from morningstar and store it in `datasets/prices.csv`

### Running

1.  `python twitter_sentiment.py` will organize the tweets and calculate the twitter sentiment
2.  `python portfolio_calculator.py` will determine buy or sells and record the backtesting. Note: Portfolio starts at 1M and you can only buy/sell 100 shares of each stock at a given time
3.  `python query_app.py` will run a simple REST-based flask micro webservice on `127.0.0.1:5000` utilizing the `query.py` module

#### REST Endpoints when server is running

1.  `http://127.0.0.1:5000/backtesting/api/v1.0/results/portfolio_balance/maxdrawdown` will calculate the max drawdown percentage
2.  `http://127.0.0.1:5000/backtesting/api/v1.0/results/portfolio_balance/netgainloss` will calculate the net/gain loss percentage
3.  `http://127.0.0.1:5000/backtesting/api/v1.0/results/portfolio_balance/YYYY-MM-DD` will calculate the balance on a given date
