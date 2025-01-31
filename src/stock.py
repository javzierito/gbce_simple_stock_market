from dataclasses import dataclass
from enum import Enum
from typing import Union


class StockType(Enum):
    COMMON = "COMMON"
    PREFERRED = "PREFERRED"


@dataclass
class Stock:
    symbol: str
    type: StockType
    last_dividend: float
    fixed_dividend: Union[str, None]
    par_value: float

    def dividend_yield(self, price: float) -> float:
        if price <= 0:
            raise ValueError("with a price of 0 or inferior the div yields loses its meaning")
        if self.type == StockType.COMMON.value:
            return self.last_dividend / price
        elif self.type == StockType.PREFERRED.value:
            fix_dividend = float(self.fixed_dividend.replace('%', '')) / 100
            return self.par_value * fix_dividend / price
        else:
            raise ValueError(f"Invalid stock type: {self.type}")

    def pe_ratio(self, price: float) -> float:
        dividend = self.dividend_yield(price) * price
        return price / dividend if dividend > 0 else float("inf")

