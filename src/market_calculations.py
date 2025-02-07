import threading
from datetime import timedelta, datetime
from statistics import geometric_mean
from typing import Dict
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from src.trade import Trade, BuySell
from src.stock import BaseStock


class TradingSystem:
    def __init__(self, workers: int = 4):
        self.trades: Dict[str, Queue] = {}
        self.lock_trading = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=workers)

    def record_trade(self, quantity: int, stock: BaseStock, operation_type: BuySell, price: float, timestamp: datetime):
        with self.lock_trading:
            if stock.symbol not in self.trades:
                self.trades[stock.symbol] = Queue()
        self.executor.submit(self._record_trade, quantity, stock, operation_type, price, timestamp)

    def _record_trade(
        self, quantity: int, stock: BaseStock, operation_type: BuySell, price: float, timestamp: datetime
    ):
        try:
            trade_instance = Trade(quantity, stock, operation_type, price, timestamp)
            self.trades[stock.symbol].put(trade_instance)
        except Exception as e:
            msg = f"problems recording trade for stock {stock}, operation {operation_type}, price {price}"
            print(msg)

    def get_stock_trades(self, symbol: str):
        if symbol not in self.trades:
            return []

        with self.lock_trading:
            queue = self.trades[symbol]
            trades = []

            while not queue.empty():
                trades.append(queue.get())

            for trade in trades:
                queue.put(trade)
            return trades


class GBCEShareIndex:
    def __init__(self, stocks: list[BaseStock], trade_system: TradingSystem):
        self.stocks = stocks
        self.trading_system = trade_system

    def calculate_index(self) -> float:
        weighted_values = []
        for stock in self.stocks:
            weighted_stock_price = self.calculate_volume_weighted_stock_price(stock.symbol, 5)
            if weighted_stock_price:
                weighted_values.append(weighted_stock_price)
        if weighted_values:
            return geometric_mean(weighted_values)

    def calculate_volume_weighted_stock_price(self, stock_symbol: str, timespan: float) -> float:
        stock_trades = self.trading_system.get_stock_trades(stock_symbol)
        allowed_timespan = datetime.now() - timedelta(minutes=timespan)
        trades_in_time = [trade for trade in stock_trades if trade.timestamp >= allowed_timespan]
        total_quantity = sum(trade.quantity for trade in trades_in_time)
        total_price_quantity = sum(trade.price * trade.quantity for trade in trades_in_time)
        if total_quantity > 0:
            return total_price_quantity / total_quantity
