import pytest

from src.trade import Trade, BuySell


def test_ill_defining_trade_instance(get_stock_instances):
    with pytest.raises(ValueError):
        Trade(
            quantity=2,
            stock=get_stock_instances[2],
            buysell='BUY',
            price=23
        )
        Trade(
            quantity=2,
            stock=get_stock_instances[2],
            buysell="iordan",
            price=23
        )
    Trade(
        quantity=2,
        stock=get_stock_instances[2],
        buysell=BuySell.BUY,
        price=23
    )
