#!flask/bin/python
from flask import Flask, jsonify
from query import portfolio_value_on_date, net_gain_loss_percentage, max_drawdown
import logging
# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


@app.route('/backtesting/api/v1.0/results/portfolio_balance/<string:date>', methods=['GET'])
def get_portfolio_value(date):
    portfolio_value = portfolio_value_on_date(date)
    return jsonify({'portfolio_value': portfolio_value})


@app.route('/backtesting/api/v1.0/results/portfolio_balance/netgainloss', methods=['GET'])
def get_net_gain_loss():
    net_gain_loss = net_gain_loss_percentage()
    return jsonify({'net_gain_loss': net_gain_loss})


@app.route('/backtesting/api/v1.0/results/portfolio_balance/maxdrawdown', methods=['GET'])
def get_max_drawdown():
    max_drawdown_percentage = max_drawdown()
    return jsonify({'Max Drawdown': max_drawdown_percentage})


if __name__ == '__main__':
    app.run(debug=True)
