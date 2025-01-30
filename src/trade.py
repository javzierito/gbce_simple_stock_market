from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from stock import Stock


class BuySell(Enum):
  BUY = "BUY"
  SELL = "SELL"


@dataclass
class Trade:
    quantity: int
    stock: Stock
    buysell: BuySell
    timestamp: datetime.now()
    price: float

    def __post_init__(self):
        if self.buysell not in BuySell:
            raise ValueError("Incorrect trade type must be 'BUY' or 'SELL'")
