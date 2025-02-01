from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

from src.stock import BaseStock


class BuySell(Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass
class Trade(BaseModel):
    # IMPROVEMENT javier: we can have a gui easily if i move attr to
    quantity: int
    stock: BaseStock
    buysell: BuySell
    price: float
    timestamp: datetime = datetime.now()

    def __post_init__(self):
        if not isinstance(self.buysell, BuySell):
            raise ValueError(f"Incorrect trade type: {self.buysell}. Must be 'BUY' or 'SELL'")