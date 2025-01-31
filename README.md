# Global Beverage Corporation Exchange (GBCE) - Python Stock Market Model

## Overview
This repository implements an object-oriented stock market model for GBCE. It calculates:
- Dividend Yield
- P/E Ratio
- Volume Weighted Stock Price (VWSP)
- GBCE All Share Index

## Getting Started
### Install Dependencies
```bash
pip install -r requirements.txt

## Run the tests
pytest tests/

## Example of use
from src.stock import Stock, StockType
tea_stock = Stock("TEA", StockType.COMMON.value, 10, 0, 100)
print(tea_stock.dividend_yield(50))  # Output: 0.2
