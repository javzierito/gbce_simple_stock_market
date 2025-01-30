import math
import pytest

from src.market_calculations import calculate_gbce_shared_index


def test_calculation_of_gbce_shared_index():
    original_data = list(range(1, 20))
    ref_value = 7.928946844865149
    index_value = calculate_gbce_shared_index(original_data)
    assert math.isclose(ref_value, index_value)


def test_calculation_of_gbce_shared_index_ill_data():
    original_data = list(range(20))
    with pytest.raises(ValueError):
        calculate_gbce_shared_index(original_data)
        calculate_gbce_shared_index(list(range(-10, 0)))

