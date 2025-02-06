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
    # IMPROVEMENT javier: we can have a gui easily if i move attr to
    quantity: Decimal
    stock: BaseStock
    buysell: BuySell
    price: Decimal
    timestamp: datetime = datetime.now()
