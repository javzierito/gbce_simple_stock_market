import inspect
from typing import Union
from abc import ABC, abstractmethod
from pydantic import ValidationError
from pydantic.dataclasses import dataclass


@dataclass
class BaseStock(ABC):
    symbol: str
    last_dividend: float
    par_value: float

    @staticmethod
    def validate_price(price: float) -> None:
        if price <= 0:
            raise ValueError("Price must be greater than 0 for dividend yield calculation.")

    @abstractmethod
    def _calculate_dividend_yield(self, price: float) -> float:
        pass

    def dividend_yield(self, price: float) -> float:
        self.validate_price(price)
        return self._calculate_dividend_yield(price)

    def calculate_pe_ratio(self, price: float) -> float:
        dividend = self.dividend_yield(price) * price
        return price / dividend if dividend > 0 else float("inf")


@dataclass
class PreferredStock(BaseStock):
    fixed_dividend: float

    def _calculate_dividend_yield(self, price: float) -> float:
        fix_dividend = self.fixed_dividend / 100
        return self.par_value * fix_dividend / price


@dataclass
class CommonStock(BaseStock):
    def _calculate_dividend_yield(self, price: float) -> float:
        return self.last_dividend / price


stock_type_vs_class = {
    "COMMON": CommonStock,
    "PREFERRED": PreferredStock,
}


def filter_stock_attrs(stock_attrs: dict, stock_klass: BaseStock):
    potential_klass_attrs = inspect.signature(stock_klass.__init__)
    klass_members = potential_klass_attrs.parameters.keys()
    return {key: stock_attrs[key] for key in klass_members if key != "self"}


def stock_factory(stock_type: str, stock_attrs: dict) -> Union[PreferredStock, CommonStock, None]:
    stock_klass = stock_type_vs_class.get(stock_type, "")
    stock_instance = None
    if not stock_klass:
        raise ValueError(f"That stock type {stock_type} is not implemented")
    try:
        filtered_stock_attrs = filter_stock_attrs(stock_attrs, stock_klass)
        stock_instance = stock_klass(**filtered_stock_attrs)
    except ValidationError as e:
        print(e.errors())
    except TypeError as e:
        print(e)
    return stock_instance

