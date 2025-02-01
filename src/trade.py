from datetime import datetime
from enum import Enum
from pydantic.dataclasses import dataclass

from src.stock import BaseStock


class BuySell(Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass
class Trade:
    # IMPROVEMENT javier: we can have a gui easily if i move attr to
    quantity: int
    stock: BaseStock
    buysell: BuySell
    price: float
    timestamp: datetime = datetime.now()
