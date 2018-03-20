import tweepy
from tweepy import AppAuthHandler
from sys import exit
from datetime import datetime
consumer_key = 'XXXX'
consumer_secret = 'XXXX'
auth = AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)
if (not api):
    print("Can't Authenticate")
    exit(-1)

start_date = datetime(2018, 3, 9)
end_date = datetime(2018, 3, 18)

tickers = ['AAPL', 'MSFT', 'MMM', 'TSLA',
           'DE', 'HD', 'UNP', 'CAT', 'GS', 'COST']

tickers_twitter = ['Apple', 'Microsoft',
                   '3M', 'Tesla', 'JohnDeere', 'HomeDepot', 'UnionPacific', 'CaterpillarInc', 'GoldmanSachs', 'Costco']

for ticker_twitter_account in tickers_twitter:
    cricTweet = tweepy.Cursor(
        api.user_timeline, ticker_twitter_account).items(5)
    for tweet in cricTweet:
        if tweet.created_at >= start_date and tweet.created_at <= end_date:
            print(tweet.created_at, tweet.text, tweet.lang,
                  tweet.retweet_count, tweet.favorite_count)
