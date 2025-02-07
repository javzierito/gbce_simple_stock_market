from datetime import datetime
from enum import Enum
from decimal import Decimal
from pydantic.dataclasses import dataclass

from src.stock import BaseStock


class BuySell(Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass
class Trade:
    quantity: Decimal
    stock: BaseStock
    buysell: BuySell
    price: Decimal
    timestamp: datetime
