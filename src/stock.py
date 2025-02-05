import inspect
from typing import Union
from abc import ABC, abstractmethod
from pydantic import ValidationError
from pydantic.dataclasses import dataclass
from decimal import Decimal


class StockValidationError(Exception):
    pass


class NotImplementedStockError(Exception):
    pass


class StockCreationError(Exception):
    pass


@dataclass
class BaseStock(ABC):
    symbol: str
    last_dividend: Decimal
    par_value: Decimal

    @staticmethod
    def validate_price(price: Decimal) -> None:
        if price <= Decimal(0):
            raise ValueError("Price must be greater than 0")

    @abstractmethod
    def _calculate_dividend_yield(self, price: Decimal) -> Decimal:
        pass

    def dividend_yield(self, price: Decimal) -> Decimal:
        self.validate_price(price)
        return self._calculate_dividend_yield(price)

    def calculate_pe_ratio(self, price: Decimal) -> Decimal:
        dividend = self.dividend_yield(price) * price
        return price / dividend if dividend > 0 else Decimal("inf")


@dataclass
class PreferredStock(BaseStock):
    fixed_dividend: Decimal

    def _calculate_dividend_yield(self, price: Decimal) -> Decimal:
        fix_dividend = self.fixed_dividend / 100
        return self.par_value * fix_dividend / price


@dataclass
class CommonStock(BaseStock):
    def _calculate_dividend_yield(self, price: Decimal) -> Decimal:
        return self.last_dividend / price


stock_type_vs_class = {
    "COMMON": CommonStock,
    "PREFERRED": PreferredStock,
}


def filter_stock_attrs(stock_attrs: dict, stock_klass: BaseStock) -> dict:
    potential_klass_attrs = inspect.signature(stock_klass.__init__)
    klass_members = potential_klass_attrs.parameters.keys()
    return {key: stock_attrs[key] for key in klass_members if key != "self"}


def stock_factory(stock_type: str, stock_attrs: dict) -> Union[PreferredStock, CommonStock, None]:
    stock_klass = stock_type_vs_class.get(stock_type, "")
    if not stock_klass:
        raise NotImplementedStockError(f"Stock type:{stock_type} not implemented yet")
    try:
        filtered_stock_attrs = filter_stock_attrs(stock_attrs, stock_klass)
        stock_instance = stock_klass(**filtered_stock_attrs)
    except ValidationError as e:
        print(e.errors())
        raise StockValidationError(f"Invalid stock paramereters:{stock_type},\n check data: {filtered_stock_attrs}")
    except (ValueError, TypeError) as e:
        print(e)
        raise StockCreationError(f"Failed to create stock: {str(e)}") from e
    return stock_instance
