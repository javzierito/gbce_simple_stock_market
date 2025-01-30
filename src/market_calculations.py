from datetime import timedelta, datetime
from statistics import geometric_mean

from src.trade import Trade, BuySell
from src.stock import Stock


class TradingSystem:
    def __init__(self):
        self.trades = {}

    def record_trade(self, quantity: int, stock: Stock, operation_type: BuySell, price: float):
        if stock.symbol not in self.trades:
            self.trades[stock.symbol] = []
        instance_to_append = Trade(quantity, stock, operation_type, price)
        self.trades[stock.symbol] = instance_to_append

    def get_stock_trades(self, symbol):
        return list(self.trades.get(symbol, []))


class GBCEShareIndex:
    def __init__(self, stocks: list[Stock], trade_system: TradingSystem):
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
            return total_quantity / total_price_quantity
