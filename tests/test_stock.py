import math
import pytest

from src.stock import stock_factory


def test_negative_and_zero_price_value(get_stock_instances):
    second_stock = get_stock_instances[1]
    with pytest.raises(ValueError):
        second_stock.dividend_yield(0)
        second_stock.dividend_yield(-20)


def test_unknown_stocktype(stocks_sample_data):
    for key, values in stocks_sample_data.items():
        stock_type = "DERIVATES"
        values["symbol"] = key
        with pytest.raises(ValueError):
            stock_factory(stock_type.upper(), values)


def test_pe_ratio_normal_values(get_stock_instances):
    stock_prices = [20, 23, 34, 50, 40]
    resultant_dividend_and_pr = [
        [0.0, float('inf')],
        [0.34782608695652173, 2.875],
        [0.6764705882352942, 1.4782608695652173],
        [0.04, 25.0], [0.325, 3.076923076923077]
    ]
    dividend_and_pr = []
    for price, stock in zip(stock_prices, get_stock_instances):
        dividend_and_pr.append(
            [stock.dividend_yield(price), stock.calculate_pe_ratio(price)]
        )
    assert all([[math.isclose(result, calculation) for result, calculation in zip(result_list, calc_list)]
               for result_list, calc_list in zip(resultant_dividend_and_pr, dividend_and_pr)])
