import asyncio
from functools import reduce
from operator import or_
from typing import Any

from retirement_accelerator.data_source.cache import (
    CacheUnavailableError,
    ProviderCache,
)
from retirement_accelerator.data_source.vendor import VendorTwelveData
from retirement_accelerator.helper import GatheringTaskGroup, Singleton


class ETFDataLoader(Singleton):
    async def __load_data(self, etf_code: str) -> dict[str, Any]:
        try:
            return {etf_code: await ProviderCache().read_cache(etf_code)}
        except CacheUnavailableError:
            content = await VendorTwelveData().get_fundamental_data(etf_code)
            await ProviderCache().write_cache(etf_code, content)

        return {etf_code: await ProviderCache().read_cache(etf_code)}

    async def load_data(self, etf_codes: set[str]) -> dict[str, Any]:
        async with GatheringTaskGroup() as tg:
            for etf_code in etf_codes:
                tg.create_task(self.__load_data(etf_code))

            return reduce(or_, await tg.results())
