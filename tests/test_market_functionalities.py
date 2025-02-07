import math
import pytest
from decimal import Decimal
from src.trade import BuySell

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


def test_wrong_args_for_trading_system(get_stock_instances):
    trading_system = TradingSystem()
    stock = get_stock_instances[1]
    with pytest.raise(ValueError):
        trading_system.record_trade(Decimal(0), stock, BuySell.BUY, Decimal(30))
        trading_system.record_trade(Decimal(12, "stock", BuySell.BUY, Decimal(30))
        trading_system.record_trade(Decimal(2), stock, "george", Decimal(30))
