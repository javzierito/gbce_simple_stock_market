from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from src.stock import Stock


class BuySell(Enum):
  BUY = "BUY"
  SELL = "SELL"


@dataclass
class Trade:
    quantity: int
    stock: Stock
    buysell: BuySell
    price: float
    timestamp = datetime.now()

    def __post_init__(self):
        if not isinstance(self.buysell, BuySell):
            raise ValueError(f"Incorrect trade type: {self.buysell}. Must be 'BUY' or 'SELL'")