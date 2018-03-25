from query import portfolio_value_on_date
import os


def test_portfolio_value_on_date():
    """ test reading from portfolio.json on a given valid date if a number is returned """
    result = portfolio_value_on_date('2017-01-02')
    assert isinstance(result, (int, float, complex))
    result_invalid_date = portfolio_value_on_date('2017-000-02')
    assert result_invalid_date == 'error on date format or date not in range'
    # rename a file to throw an error
    os.rename('datasets/portfolio_balance.json',
              'datasets/portfolio_balance_e.json')
    assert portfolio_value_on_date(
        '2017-01-02') == 'something went horribly wrong trying to open the portfolio.json'
    # put it back to original state
    os.rename('datasets/portfolio_balance_e.json',
              'datasets/portfolio_balance.json')
