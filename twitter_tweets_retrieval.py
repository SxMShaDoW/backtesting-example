import tweepy
from tweepy import AppAuthHandler
from datetime import datetime
import sys
import jsonpickle
import os
import json
import csv
consumer_key = 'XX'
consumer_secret = 'XX'
auth = AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)
if (not api):
    print("Can't Authenticate")
    sys.exit(-1)

start_date = datetime(2017, 1, 1)
end_date = datetime(2017, 12, 31)
file_name = 'tweets.json'

tickers = ['AAPL', 'MSFT', 'MMM', 'TSLA',
           'DE', 'HD', 'UNP', 'CAT', 'GS', 'COST']

tickers_twitter = ['ApplePodcasts', 'Microsoft', '3M', 'Tesla', 'JohnDeere',
                   'HomeDepot', 'UnionPacific', 'CaterpillarInc', 'GoldmanSachs', 'Costcocanada']

ticker_twitter_map = {
    'ApplePodcasts': 'AAPL',
    'Microsoft': 'MSFT',
    '3M': 'MMM',
    'Tesla': 'TSLA',
    'JohnDeere': 'DE',
    'HomeDepot': 'HD',
    'UnionPacific': 'UNP',
    'CaterpillarInc': 'CAT',
    'GoldmanSachs': 'GS',
    'Costcocanada': 'COST'
}

all_tweets = []


"""
Calls twitters API and stores all tweets from a given start and end date
TO DO: Error handling and logging. clean up write array functionality and make into generators
"""
for ticker_twitter_account in tickers_twitter:
    with open(ticker_twitter_account + '.json', 'w') as f:
        cricTweet = tweepy.Cursor(
            api.user_timeline, ticker_twitter_account, count=200, include_rts=False).items()
        # add all tweets to the tweets probably should use a generator
        all_tweets.extend(cricTweet)

        # save the oldest
        oldest = all_tweets[-1].id - 1

        print(len(all_tweets))
        while cricTweet.num_tweets > 0:
            print('getting tweets before', oldest)
            try:
                new_tweets = api.user_timeline(
                    ticker_twitter_account, count=200, max_id=oldest, include_rts=False).items()
                all_tweets.extend(cricTweet)
                oldest = all_tweets[-1].id - 1
                print("tweets downloaded so far", len(all_tweets))
            except Exception:
                print('no more new tweets')
                break

        outtweets = [[tweet.id_str, tweet.created_at.strftime('%Y-%m-%d'),
                      tweet.text.encode("utf-8"), tweet.favorite_count, tweet.retweet_count] for tweet in all_tweets if tweet.created_at >= start_date and tweet.created_at <= end_date]
        # write the csv
        with open(ticker_twitter_account + '.csv', 'w') as csv_f:
            writer = csv.writer(csv_f)
            writer.writerow(["id", "created_at", "text",
                             "favorite_count", "retweet_count"])
            writer.writerows(outtweets)

        saved_dict = []
        for tweet in all_tweets:
            if tweet.created_at >= start_date and tweet.created_at <= end_date:
                important_info = {
                    'twitter_account': tweet.user.name,
                    'timestamp': tweet.created_at.strftime('%Y-%m-%d'),
                    'text': tweet.text,
                    'retweet_count': tweet.retweet_count,
                    'favorited_count': tweet.favorite_count
                }
                saved_dict.append(important_info)
        f.write(jsonpickle.encode(saved_dict))
