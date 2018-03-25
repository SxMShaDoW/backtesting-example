import sys
import os
import json
from collections import OrderedDict
from config import folder, portfolio_value
from datetime import datetime
import logging
# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def valid_date(datestring):
    """ Determine if something is a valid date """
    try:
        datetime.strptime(datestring, '%Y-%m-%d')
        return True
    except ValueError as e:
        logger.info('not a valid date: ' + e)
        return False


def portfolio_value_on_date(date):
    """ Retrieve the total portfolio value on a given data """
    if valid_date(date):
        try:
            with open(folder + 'portfolio_balance.json',  encoding='utf-8') as read_file:
                data = json.loads(read_file.read(),
                                  object_pairs_hook=OrderedDict)
                return data[date]['daily_value']
        except Exception:
            logger.critical('couldnt read portfolio.json')
            return 'something went horribly wrong trying to open the portfolio.json'
    else:
        return 'error on date format or date not in range'


def net_gain_loss_percentage():
    """ Retrieve the net gain percentage in total value of portfolio at the end of the backtest """
    try:
        with open(folder + 'portfolio_balance.json',  encoding='utf-8') as read_file:
            data = json.loads(read_file.read(),
                              object_pairs_hook=OrderedDict)
            net_gain_loss = data['final_portfolio'] / portfolio_value
            logger.info('net gain loss is ' + net_gain_loss)
            if net_gain_loss > 0:
                return 'Your net gain is ' + str(net_gain_loss) + '%'
            elif net_gain_loss == 0:
                return 'You broke even'
            else:
                return 'Your net loss is ' + str(net_gain_loss) + '%'
    except Exception:
        logger.critical('couldnt read portfolio.json')
        return 'something went horribly wrong trying to open the portfolio.json'


def max_drawdown():
    """ Maximum percentage drawdown experienced in the backtest """
    try:
        with open(folder + 'portfolio_balance.json',  encoding='utf-8') as read_file:
            data = json.loads(read_file.read(),
                              object_pairs_hook=OrderedDict)

            def daily_price():
                """ Record daily volume in a generator """
                for item in data:
                    if valid_date(item):
                        yield data[item]['daily_value']

            # since the daily portfolio is already a running tally
            # we just need to find the max and the min between them
            max_price = max(daily_price())
            min_price = min(daily_price())
            draw = max_price / min_price
            logger.info('draw percent: ' + draw)
            return 'Max Drawdown is ' + str(draw) + '%'
    except Exception:
        logger.critical('couldnt read portfolio.json')
        return 'something went horribly wrong trying to open the portfolio.json'
