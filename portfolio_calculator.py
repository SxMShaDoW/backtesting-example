from datetime import datetime
import sys
import os
import json
from collections import OrderedDict

# all the important tickers.
from twitter_tickers import tickers_twitter
from config import folder

num_buy_shares = 100
num_sell_shares = 100
portfolio_value = 100000


def daily_portfolio_organizer():
    """
    Reads the buy sell for each and organizes the data per day, then stores it
    """
    day_record = {}
    for ticker_twitter_account in tickers_twitter:
        try:
            with open(folder + ticker_twitter_account + '_buy_or_sell' + '.json',  encoding='utf-8') as read_file:
                data = json.loads(read_file.read())
                for day in data:
                    daily_buy_or_sell = data[day]['buy_or_sell']
                    daily_price = data[day]['price']
                    day_record.setdefault(day, []).append(
                        {ticker_twitter_account: {
                            'buy_or_sell': daily_buy_or_sell,
                            'price': daily_price
                        }
                        }
                    )
                # print(days)
            with open(folder + 'daily_portfolio.json', 'w') as data_set:
                data_set.write(json.dumps(day_record, sort_keys=True))
        except Exception as e:
            print(e)
            continue


def portfolio_calculator():
    """
    Reads the buy sell for each and updates portfolio accordingly, then stores it
    """
    record_keeping = {
        'final_portfolio': 1000000,
        'num_of_buys': 0,
        'num_of_sells': 0
    }
    # set all the tickers as a record
    for ticker in tickers_twitter:
        record_keeping[ticker] = 0
    try:
        with open(folder + 'daily_portfolio.json',  encoding='utf-8') as read_file:
            data = json.loads(read_file.read(), object_pairs_hook=OrderedDict)
            for day, value in data.items():
                daily_value = 0
                daily_count_sells = 0
                daily_count_buys = 0
                for account in value:
                    account_name = list(account.keys())[0]
                    for item in account.values():
                        buy_or_sell = item['buy_or_sell']
                        price = item['price']
                        bought_shares = float(price) * num_buy_shares
                        if buy_or_sell == 'BUY' and (record_keeping['final_portfolio'] - bought_shares >= 0) and (record_keeping[account_name] == 0):
                            record_keeping['final_portfolio'] = record_keeping['final_portfolio'] - bought_shares
                            daily_count_buys += 1
                            record_keeping['num_of_buys'] = record_keeping['num_of_buys'] + 1
                            daily_value = record_keeping['final_portfolio']
                            record_keeping[account_name] = num_buy_shares
                        elif buy_or_sell == 'SELL' and (record_keeping[account_name] == 100):
                            sold_shares = float(price) * num_sell_shares
                            record_keeping['final_portfolio'] = record_keeping['final_portfolio'] + sold_shares
                            daily_count_sells += 1
                            record_keeping['num_of_sells'] = record_keeping['num_of_sells'] + 1
                            daily_value = record_keeping['final_portfolio']
                            record_keeping[account_name] = 0
                        daily_value = record_keeping['final_portfolio']
                    record_keeping.setdefault(day, {})
                    record_keeping[day] = {
                        'daily_value': daily_value,
                        'daily_sells': daily_count_sells,
                        'daily_buys': daily_count_buys
                    }
        with open(folder + 'portfolio_balance.json', 'w') as data_set:
            data_set.write(json.dumps(record_keeping, sort_keys=True))
    except Exception as e:
        print(e)
    print(json.dumps(record_keeping, sort_keys=True))


if __name__ == "__main__":
    daily_portfolio_organizer()
    portfolio_calculator()
