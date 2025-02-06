# Global Beverage Corporation Exchange (GBCE) - Python Stock Market Model

## Overview
This repository implements an object-oriented stock market model for GBCE. 
It calculates for the stock:
- Dividend Yield
- P/E Ratio
- Record a trade, with timestamp, quantity, buy or sell indicator and price
- Volume Weighted Stock Price (VWSP)
And finally, calcualtes,
- GBCE All Share Index using the geometric mean of the volume weighted stock price for all stocs

## Relevant Branches to look at
I started the exercise with something very basic that I have been completing up to now.

### Main branch
The implementation found in main tackled, 
- setting the repo structure
- finding right packages
- search for good ways of solving the assignment given
- solve the assignment with a clear functionality description
- Thorough testing and search for corner cases

### Development: trade_system_concurrency
This branch aims to make more realistic the trading system. As I imagine, dont see a trading system uncapable of handling multiple transactions or trades at the same time.
Therefore some study and exploration of concurrency, threads and multiprocess was needed.
I thought about a threading implementation, but it seemt to me that the complexity of the threads speaking to each other wasnt worth the risk of the implementation.
As a consequence, I ended up implementing a threadpoolexecutor which is capable of handling the situation described above.

## Getting Started
### Install Dependencies
```bash
pip install -r requirements.txt

## Run the tests
pytest tests/

## Example of use
from src.stock import Stock, StockType
from decimal import Decimal
tea_stock = CommonStock("TEA", Decimal(10), Decimal(100))
print(tea_stock.dividend_yield(50))  # Output: 0.2
