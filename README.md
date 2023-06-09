# Retirement Accelerator
Retirement Accelerator is a toolkit aims to filter ETFs with specific rules and indicators easily.

The project use [EODHD APIs](https://eodhistoricaldata.com/) as data vendor, please fill in your API keys in `.env` file.

# Getting Started

```python
import asyncio
from typing import Any

from retirement_accelerator.data_source.loader import ETFDataLoader
from retirement_accelerator.strategy.indicators import (
    Indicator,
    max_annual_mgmt_charge,
    top_sector_weights,
)
from retirement_accelerator.strategy.portfolio import Portfolio


async def show_portfolio_no_mgmt_fee(data: dict[str, Any]):
    await Portfolio(
        "Zero Management Fee",
        data,
        (Indicator(max_annual_mgmt_charge, lambda x: x == 0),),
    ).rank(top_sector_weights)


async def main():
    data = await ETFDataLoader().load_data({"VTI"})
    await show_portfolio_no_mgmt_fee(data)


asyncio.run(main())

```