#!flask/bin/python
from flask import Flask, jsonify
from query import portfolio_value_on_date, net_gain_loss_percentage, max_drawdown

app = Flask(__name__)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/backtesting/api/v1.0/results', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


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
