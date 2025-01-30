from datetime import timedelta, datetime
from statistics import geometric_mean

from trade import Trade


def calculate_gbce_shared_index(volume_weighted_stocks: list[float]) -> float:
    return geometric_mean(volume_weighted_stocks)


def calculate_volume_weighted_stock_price(same_stock_trades: list[Trade], timespan: float) -> float:
    allowed_timespan = datetime.now() - timedelta(minutes=timespan)
    trades_in_time = [trade for trade in same_stock_trades if trade.timestamp >= allowed_timespan]
    total_quantity = sum(trade.quantity for trade in trades_in_time)
    total_price_quantity = sum(trade.price * trade.quantity for trade in trades_in_time)
    return total_quantity / total_price_quantity
