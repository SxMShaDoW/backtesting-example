import jsonpickle
import os
import json
import csv

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


""" Read the daily data and store it with the buy_or_sell """
try:
    with open('prices.csv', 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',',  quotechar='|')
        all_prices = [{'ticker': row[0], 'date': row[1],
                       'price': row[2]} for row in reader]
except Exception as e:
    print(e)

"""
Reads the daily data and determines a sentiment score and buy/sell, then stores it
"""
for ticker_twitter_account in tickers_twitter:
    days = {}
    # price = 'NA'
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
                for item in all_prices:
                    if item['ticker'] == ticker_twitter_map[ticker_twitter_account] and item['date'] == day:
                        price = item['price']
                days[day] = {
                    'sentiment_score': sentiment_score,
                    'buy_or_sell': buy_or_sell_str,
                    'price': price
                }
            # print(days)
        with open(ticker_twitter_account + '_buy_or_sell' + '.json', 'w') as data_set:
            data_set.write(jsonpickle.encode(days))
    except Exception as e:
        print(e)
        continue
