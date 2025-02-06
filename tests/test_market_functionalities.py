import math

from src.market_calculations import GBCEShareIndex, TradingSystem


def test_calculation_of_gbce_shared_index(create_trading_system_with_logged_trades, get_stock_instances):
    trading_system = create_trading_system_with_logged_trades
    stocks = get_stock_instances
    ref_index_value = 29.28571429000001
    gbce_index = GBCEShareIndex(stocks, trading_system)
    index_value = gbce_index.calculate_index()
    assert math.isclose(ref_index_value, index_value)


def test_calculation_of_gbceindex_no_trades(get_stock_instances):
    trading_system = TradingSystem()
    stocks = get_stock_instances
    gbce_index = GBCEShareIndex(stocks, trading_system)
    index_value = gbce_index.calculate_index()
    assert not index_value
