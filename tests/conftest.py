import pytest

from src.stock import Stock
from src.trade import BuySell
from src.market_calculations import TradingSystem


@pytest.fixture
def sample_data_gbce():
    stocks_of_market = {
        "TEA": {
            "type": "COMMON",
            "last_dividend": 0,
            "fixed_dividend": None,
            "par_value": 100
            },
        "POP": {
            "type": "COMMON",
            "last_dividend": 8,
            "fixed_dividend": None,
            "par_value": 100
            },
        "ALE": {
            "type": "COMMON",
            "last_dividend": 23,
            "fixed_dividend": None,
            "par_value": 60
        },
        "GIN": {
            "type": "PREFERRED",
            "last_dividend": 8,
            "fixed_dividend": 0.02,
            "par_value": 100
        },
        "JOE": {
            "type": "COMMON",
            "last_dividend": 13,
            "fixed_dividend": None,
            "par_value": 250
        }
    }
    return stocks_of_market


@pytest.fixture
def get_stock_instances(sample_data_gbce):
    stocks = []
    for key, values in sample_data_gbce.items():
        stock_instance = Stock(symbol=key, **values)
        stocks.append(stock_instance)
    return stocks


# IMPROVE javier: find a better way to generate data for the tests
@pytest.fixture
def create_trading_system_with_logged_trades(get_stock_instances):
    trading_sys = TradingSystem()
    for stock in get_stock_instances:
        for quantity, price, operation in zip([3, 4], [15, 40], [BuySell.BUY, BuySell.SELL]):
            trading_sys.record_trade(quantity, stock, operation, price)
    return trading_sys
