from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class BuySell(Enum):
  BUY = "BUY"
  SELL = "SELL"


@dataclass
class Trade:
    quantity: int
    price: float
    stock_symbol: str
    buysell: BuySell
    timestamp: datetime.now()

    def __post_init__(self):
        if self.buysell not in BuySell:
            raise ValueError("Incorrect trade type must be 'BUY' or 'SELL'")
