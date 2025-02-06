import math
import concurrent.futures
import random
import string
from datetime import datetime, timedelta
from hypothesis import given, strategies as st

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


def test_concurrent_store_of_trades(generate_trades_data):
    trades_data, stock_symbols = generate_trades_data
    trading_system = TradingSystem()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for trade_data in trades_data:
            future = executor.submit(trading_system.record_trade, *trade_data)
            futures.append(future)
        concurrent.futures.wait(futures)
    trades = trading_system.get_stock_trades(random.choice(stock_symbols))


def generate_stock_symbols(num_symbols=50):
    symbols = set()
    while len(symbols) < num_symbols:
        symbol_length = random.randint(3, 5)
        symbol = ''.join(random.choices(string.ascii_uppercase, k=symbol_length))
        symbols.add(symbol)
    return list(symbols)


@given(st.lists(st.tuples(
    st.sampled_from(generate_stock_symbols(50)),  # Use the stock_symbols fixture
    st.integers(min_value=1, max_value=10000),
    st.sampled_from(["BUY", "SELL"]),
    st.decimals(min_value=0.01, max_value=1000.00),
    st.datetimes(min_value=datetime.now() - timedelta(minutes=5), max_value=datetime.now())
), min_size=10))  # Generate at least 100 trades
def test_concurrent_store_of_trades_10_million(trades_data):
    trading_system = TradingSystem()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for trade_data in trades_data:
            future = executor.submit(trading_system.record_trade, *trade_data)
            futures.append(future)
        concurrent.futures.wait(futures)
        print(trading_system)
