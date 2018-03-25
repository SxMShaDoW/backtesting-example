# Stock backtesting with twitter sentiment

## Pre-reqs

* Python 3.5.2 +
* pip 3+
* `pip3 install tweepy`
* `pip3 install pandas`

### Setup

1.  `git clone` this repo.
2.  Create a `secrets.py` file at the root
3.  Place your `consumer_key = 'XXXX'` in the `secrets.py`
4.  Place your `consumer_secret = 'XXX'` in the `secrets.py`
5.  Modify the `twitter_tickers.py` for all the stocks/twitter accounts you care about

### Run once

1.  `python twitter_tweets_retrieval.py` will retrieve pull all tweets from stock accounts and place them in individual .json files + csv (for backup).

### Running

1.  `python twitter_sentiment.py` will organize the tweets and calculate the twitter sentiment
2.  `python portfolio_calculator.py` will determine buy or sells and record the backtesting. Note: Portfolio starts at 1M and you can only buy/sell 100 shares of each stock at a given time
