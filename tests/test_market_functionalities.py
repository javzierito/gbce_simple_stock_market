from __future__ import annotations
import math
import concurrent.futures
import random
from typing import List
from datetime import datetime
from decimal import Decimal

from src.market_calculations import GBCEShareIndex, TradingSystem
from src.stock import CommonStock, PreferredStock
from src.trade import BuySell


def test_calculation_of_gbce_shared_index(
    create_trading_system_with_logged_trades: TradingSystem, get_stock_instances: List[CommonStock | PreferredStock]
):
    trading_system = create_trading_system_with_logged_trades
    stocks = get_stock_instances
    ref_index_value = 29.28571429000001
    gbce_index = GBCEShareIndex(stocks, trading_system)
    index_value = gbce_index.calculate_index()
    assert math.isclose(ref_index_value, index_value, rel_tol=0.01)


def test_calculation_of_gbceindex_no_trades(get_stock_instances: List[CommonStock | PreferredStock]):
    trading_system = TradingSystem(workers=4)
    stocks = get_stock_instances
    gbce_index = GBCEShareIndex(stocks, trading_system)
    index_value = gbce_index.calculate_index()
    assert not index_value


def test_wrong_args_for_trading_system(get_stock_instances):
    trading_system = TradingSystem()
    stock = get_stock_instances[1]
    with pytest.raises(ValueError):
        trading_system.record_trade(Decimal(0), stock, BuySell.BUY, Decimal(30))
        trading_system.record_trade(Decimal(12), "stock", BuySell.BUY, Decimal(30))
        trading_system.record_trade(Decimal(2), stock, "george", Decimal(30))


def test_concurrent_store_of_trades(generate_trades_data):
    print("calc GBCE index value")
    start_time = datetime.now()
    print(f"Function started at: {start_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
    trades_data, stock_symbols, stock_instances = generate_trades_data
    trading_system = TradingSystem(workers=4)
    with trading_system.executor as executor:
        futures = []
        for trade_data in trades_data:
            future = executor.submit(trading_system.record_trade, *trade_data)
            futures.append(future)
        concurrent.futures.wait(futures)
    trades = trading_system.get_stock_trades(random.choice(stock_symbols))
    gbce_index = GBCEShareIndex(stock_instances, trading_system)
    index_value = gbce_index.calculate_index()

    end_time = datetime.now()
    duration = end_time - start_time
    print(f"Function ended at:   {end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
    print(f"Function execution time: {duration} secs")
    print("------------------------------------------------------------------")
    assert isinstance(index_value, float)
