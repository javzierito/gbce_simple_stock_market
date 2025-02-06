from __future__ import annotations
import pytest
import string
import random
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, Any, List
import concurrent.futures

from src.stock import stock_factory, CommonStock, PreferredStock
from src.trade import BuySell
from src.market_calculations import TradingSystem


@pytest.fixture
def stocks_sample_data() -> Dict[str, Dict[str, Any]]:
    return {
        "TEA": {"type": "COMMON", "last_dividend": Decimal(0), "fixed_dividend": None, "par_value": Decimal(100)},
        "POP": {"type": "COMMON", "last_dividend": Decimal(8), "fixed_dividend": None, "par_value": Decimal(100)},
        "ALE": {"type": "COMMON", "last_dividend": Decimal(23), "fixed_dividend": None, "par_value": Decimal(60)},
        "GIN": {
            "type": "PREFERRED",
            "last_dividend": Decimal(8),
            "fixed_dividend": Decimal(2),
            "par_value": Decimal(100),
        },
        "JOE": {"type": "COMMON", "last_dividend": Decimal(13), "fixed_dividend": None, "par_value": Decimal(250)},
    }


@pytest.fixture
def get_stock_instances(stocks_sample_data: Dict[str, Dict[str, Any]]) -> List[CommonStock | PreferredStock]:
    stocks = []
    for key, values in stocks_sample_data.items():
        stock_type = values.pop("type")
        values["symbol"] = key
        stock_instance = stock_factory(stock_type.upper(), values)
        if stock_instance:
            stocks.append(stock_instance)
    return stocks


# IMPROVE javier: find a better way to generate data for the tests
@pytest.fixture
def create_trading_system_with_logged_trades(get_stock_instances):
    trading_system = TradingSystem(workers=4)
    with trading_system.executor as executor:
        futures = []
        for stock in get_stock_instances:
            for quantity, price, operation in zip([3, 4], [15, 40], [BuySell.BUY, BuySell.SELL]):
                trade_data = (quantity, stock, operation, price)
                future = executor.submit(trading_system.record_trade, *trade_data)
                futures.append(future)
        concurrent.futures.wait(futures)
    return trading_system


@pytest.fixture(autouse=True)
def setup_precision():
    import decimal

    decimal.getcontext().prec = 10
    return


def generate_stock_symbols(num_symbols: int=50) -> list[str]:
    symbols = set()
    while len(symbols) < num_symbols:
        symbol_length = random.randint(3, 5)
        symbol = "".join(random.choices(string.ascii_uppercase, k=symbol_length))
        symbols.add(symbol)
    return list(symbols)


def generate_random_stock():


@pytest.fixture(params=[100, 10e5, 10e7])
def generate_trades_data(request):
    num_trades = request.param
    stock_symbols = generate_stock_symbols(50)
    print(f"Generating {num_trades} trades for this test...")

    trades_with_datetime = []
    for _ in range(num_trades):
        symbol = random.choice(stock_symbols)
        quantity = random.randint(1, 10000)
        buy_sell = random.choice(["BUY", "SELL"])
        price = Decimal(random.uniform(0.01, 1000.00)).quantize(Decimal("0.01"))
        timestamp = datetime.fromtimestamp(
            random.randint(int((datetime.now() - timedelta(minutes=130)).timestamp()), int(datetime.now().timestamp()))
        )
        trades_with_datetime.append((symbol, quantity, buy_sell, price, timestamp))
    return trades_with_datetime, stock_symbols
