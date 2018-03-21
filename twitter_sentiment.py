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

tickers_twitter = ['AppleSupport', 'Microsoft', '3M', 'Tesla', 'JohnDeere',
                   'HomeDepot', 'UnionPacific', 'CaterpillarInc', 'GoldmanSachs', 'Costcocanada']

# tickers_twitter = ['ApplePodcasts']

all_tweets = []


"""
Calls twitters API and stores all tweets from a given start and end date
TO DO: Error handling and logging. clean up write array functionality and make into generators
"""
# for ticker_twitter_account in tickers_twitter:
#     with open(ticker_twitter_account + '.json', 'w') as f:
#         cricTweet = tweepy.Cursor(
#             api.user_timeline, ticker_twitter_account, count=200, include_rts=False).items()
#         # add all tweets to the tweets probably should use a generator
#         all_tweets.extend(cricTweet)

#         # save the oldest
#         oldest = all_tweets[-1].id - 1

#         print(len(all_tweets))
#         while cricTweet.num_tweets > 0:
#             print('getting tweets before', oldest)
#             try:
#                 new_tweets = api.user_timeline(
#                     ticker_twitter_account, count=200, max_id=oldest, include_rts=False).items()
#                 all_tweets.extend(cricTweet)
#                 oldest = all_tweets[-1].id - 1
#                 print("tweets downloaded so far", len(all_tweets))
#             except Exception:
#                 print('no more new tweets')
#                 break

#         outtweets = [[tweet.id_str, tweet.created_at.strftime('%Y-%m-%d'),
#                       tweet.text.encode("utf-8"), tweet.favorite_count, tweet.retweet_count] for tweet in all_tweets if tweet.created_at >= start_date and tweet.created_at <= end_date]
#         # write the csv
#         with open(ticker_twitter_account + '.csv', 'w') as csv_f:
#             writer = csv.writer(csv_f)
#             writer.writerow(["id", "created_at", "text",
#                              "favorite_count", "retweet_count"])
#             writer.writerows(outtweets)

#         saved_dict = []
#         for tweet in all_tweets:
#             if tweet.created_at >= start_date and tweet.created_at <= end_date:
#                 important_info = {
#                     'twitter_account': tweet.user.name,
#                     'timestamp': tweet.created_at.strftime('%Y-%m-%d'),
#                     'text': tweet.text,
#                     'retweet_count': tweet.retweet_count,
#                     'favorited_count': tweet.favorite_count
#                 }
#                 saved_dict.append(important_info)
#         f.write(jsonpickle.encode(saved_dict))

"""
Reads all the tweets from each twitter accounts and writes a daily tweet data file
TO DO: Error handling and logging. clean up the check if daily data exists
"""
# for ticker_twitter_account in tickers_twitter:
#     try:
#         with open(ticker_twitter_account + '.json', encoding='utf-8') as data_file:
#             data = json.loads(data_file.read())
#             data_store = {}
#             for issue in data:
#                 timestamp = issue['timestamp']
#                 favorite_count = issue['favorited_count']
#                 retweet_count = issue['retweet_count']
#                 if timestamp not in data_store:
#                     data_store[timestamp] = {
#                         'daily_favorited_count': favorite_count, 'daily_retweet_count': retweet_count}
#                 else:
#                     data_store[timestamp
#                                ]['daily_favorited_count'] = data_store[timestamp]['daily_favorited_count'] + favorite_count
#                     data_store[timestamp]['daily_retweet_count'] = data_store[timestamp
#                                                                               ]['daily_retweet_count'] + retweet_count
#             # print(data_store)
#             with open(ticker_twitter_account + '_daily_data' + '.json', 'w') as data_set:
#                 data_set.write(jsonpickle.encode(data_store))
#     except Exception:
#         continue


def buy_or_sell(sentiment_score):
    if sentiment_score <= 0.22:
        return 'BUY'
    else:
        return 'SELL'


"""
Reads the daily data and determines a sentiment score and buy/sell, then stores it
"""
for ticker_twitter_account in tickers_twitter:
    days = {}
    try:
        with open(ticker_twitter_account + '_daily_data' + '.json',  encoding='utf-8') as read_file:
            data = json.loads(read_file.read())
            for day in data:
                daily_favorited_count = data[day]['daily_favorited_count']
                daily_retweet_count = data[day]['daily_retweet_count']
                # print(daily_favorited_count)
                if daily_favorited_count == 0 or daily_retweet_count == 0:
                    sentiment_score = 0
                    buy_or_sell_str = 'SELL'
                else:
                    sentiment_score = daily_retweet_count / daily_favorited_count
                    buy_or_sell_str = buy_or_sell(sentiment_score)
                days[day] = {
                    'sentiment_score': sentiment_score,
                    'buy_or_sell': buy_or_sell_str
                }
            # print(days)
        with open(ticker_twitter_account + '_buy_or_sell' + '.json', 'w') as data_set:
            data_set.write(jsonpickle.encode(days))
    except Exception as e:
        print(e)
        continue
