from __future__ import annotations
from typing import List
import pytest
from datetime import datetime

from src.stock import CommonStock, PreferredStock
from src.trade import Trade, BuySell


def test_ill_defining_trade_instance(get_stock_instances: List[CommonStock | PreferredStock]):
    with pytest.raises(ValueError):
        Trade(quantity=2, stock=get_stock_instances[2], buysell="BUY", price=23, timestamp=datetime.now())
        Trade(quantity=2, stock=get_stock_instances[2], buysell="iordan", price=23)
    Trade(quantity=2, stock=get_stock_instances[2], buysell=BuySell.BUY, price=23)
