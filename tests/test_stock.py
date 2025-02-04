import math
import pytest
from hypothesis import given, strategies as st

from src.stock import stock_factory, CommonStock, PreferredStock


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


class TestStockCalculations:
    @given(st.text(min_size=1, max_size=5), st.floats(min_value=0, max_value=1000), st.floats(min_value=0, max_value=1000), st.floats(min_value=0, max_value=100))
    def test_base_stock_initialization(self, symbol, last_dividend, par_value, fixed_dividend):
        CommonStock(symbol, last_dividend, par_value)
        PreferredStock(symbol, last_dividend, par_value, fixed_dividend)

    @given(st.floats(min_value=0.001, max_value=1000))
    def test_common_stock_dividend_yield(self, price):
        stock = CommonStock("TEST", 10, 100)
        expected_yield = 10 / price
        assert stock.dividend_yield(price) == pytest.approx(expected_yield)

    @given(st.floats(min_value=0.001, max_value=1000), st.floats(min_value=0, max_value=100))
    def test_preferred_stock_dividend_yield(self, price, fixed_dividend):
        stock = PreferredStock("TEST", 10, 100, fixed_dividend)
        expected_yield = (100 * (fixed_dividend / 100)) / price
        assert stock.dividend_yield(price) == pytest.approx(expected_yield)

    @given(st.floats(min_value=0.001, max_value=1000))
    def test_common_stock_pe_ratio(self, price):
        stock = CommonStock("TEST", 10, 100)
        dividend = stock.dividend_yield(price) * price
        expected_pe = price / dividend if dividend > 0 else float('inf')
        assert stock.calculate_pe_ratio(price) == pytest.approx(expected_pe)

    @given(st.floats(min_value=0.001, max_value=1000), st.floats(min_value=0, max_value=100))
    def test_preferred_stock_pe_ratio(self, price, fixed_dividend):
        stock = PreferredStock("TEST", 10, 100, fixed_dividend)
        dividend = stock.dividend_yield(price) * price
        expected_pe = price / dividend if dividend > 0 else float('inf')
        assert stock.calculate_pe_ratio(price) == pytest.approx(expected_pe)

    @given(st.floats(max_value=0), st.floats(min_value=0, max_value=1000))
    def test_validate_price_raises_error(self, price, last_dividend):
        with pytest.raises(ValueError):
            CommonStock("TEST", last_dividend, 100).validate_price(price)

