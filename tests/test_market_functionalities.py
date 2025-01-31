import math

from src.market_calculations import GBCEShareIndex


def test_calculation_of_gbce_shared_index(create_trading_system_with_logged_trades, get_stock_instances):
    trading_system = create_trading_system_with_logged_trades
    stocks = get_stock_instances
    ref_index_value = 0.034146341463414616
    gbce_index = GBCEShareIndex(stocks, trading_system)
    index_value = gbce_index.calculate_index()
    assert math.isclose(ref_index_value, index_value)
