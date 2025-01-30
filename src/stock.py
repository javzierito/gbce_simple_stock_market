from dataclasses import dataclass
from enum import Enum


class StockType(Enum):
  COMMON = "COMMON"
  PREFERRED = "PREFERRED"


@dataclass
class Stock:
    symbol: str
    type: StockType
    last_dividend: float
    fixed_dividend: float
    par_value: float

    def dividend_yield(self, price: float) -> float:
        if price <= 0:
            raise ValueError("with a price of 0 or inferior the div yields loses its meaning")
        if self.type == "COMMON":
            return self.last_dividend / price
        else:
            return self.par_value * self.fixed_dividend / price

    def pe_ratio(self, price: float) -> float:
        dividend = self.dividend_yield(price) * price
        return price / dividend if dividend > 0 else float("inf")

