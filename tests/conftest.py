import pytest


@pytest.fixture
def sample_data_gbce():
    stocks_of_market = {
        "TEA": {
            "Type": "COMMON",
            "last_dividend": 0,
            "fixed_dividend": None,
            "Par Value": 100
            },
        "POP": {
            "Type": "COMMON",
            "last_dividend": 8,
            "fixed_dividend": None,
            "Par Value": 100
            },
        "ALE": {
            "Type": "COMMON",
            "last_dividend": 23,
            "fixed_dividend": None,
            "Par Value": 60
        },
        "GIN": {
            "Type": "PREFERRED",
            "last_dividend": 8,
            "fixed_dividend": 0.02,
            "Par Value": 100
        },
        "JOE": {
            "Type": "COMMON",
            "last_dividend": 13,
            "fixed_dividend": None,
            "par_value": 250
        }
    }
    return stocks_of_market
