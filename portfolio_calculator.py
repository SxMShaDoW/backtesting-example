from datetime import datetime
import sys
import os
import json

tickers_twitter = ['ApplePodcasts', 'Microsoft', '3M', 'Tesla', 'JohnDeere',
                   'HomeDepot', 'UnionPacific', 'CaterpillarInc', 'GoldmanSachs', 'Costcocanada']

num_buy_shares = 100
num_sell_shares = 100
capital = 100000

"""
Reads the buy sell for each and updates portfolio accordingly, then stores it
"""
record_keeping = {}
for ticker_twitter_account in tickers_twitter:
    try:
        with open(ticker_twitter_account + '_buy_or_sell' + '.json',  encoding='utf-8') as read_file:
            data = json.loads(read_file.read())
            for day in data:
                daily_buy_or_sell = data[day]['buy_or_sell']
                daily_price = data[day]['price']
                bought_shares = float(daily_price) * num_buy_shares
                if daily_buy_or_sell == 'SELL':
                    sold_shares = float(daily_price) * num_sell_shares
                    capital += sold_shares
                elif daily_buy_or_sell == 'BUY' and (capital - bought_shares >= 0):
                    capital -= bought_shares
                record_keeping.setdefault(day, []).append(
                    {ticker_twitter_account: {
                        'current_capital': capital
                    }
                    }
                )
            # print(days)
        # with open(ticker_twitter_account + '_buy_or_sell' + '.json', 'w') as data_set:
        #     data_set.write(jsonpickle.encode(days))
    except Exception as e:
        print(e)
        continue

print(json.dumps(record_keeping, sort_keys=True))
