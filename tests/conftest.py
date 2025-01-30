import pytest

from src.stock import Stock


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
