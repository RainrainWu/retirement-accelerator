from datetime import datetime, timedelta
from json import dumps, loads
from typing import Any

from aiofiles import open
from aiofiles.ospath import exists
from loguru import logger
from retirement_accelerator.config import ManagerConfig
from retirement_accelerator.errors import RetirementAcceleratorError
from retirement_accelerator.helper import Singleton


class CacheUnavailableError(RetirementAcceleratorError):
    pass


class ProviderCache(Singleton):
    async def __check_expiration(self, etf_code: str, last_updated_raw: str) -> None:
        last_updated = datetime.strptime(
            last_updated_raw,
            ManagerConfig().CACHED_FILE_TIMESTAMP_FORMAT,
        )
        if (
            last_updated + timedelta(hours=ManagerConfig().CACHED_FILE_EXPIRATION_HOURS)
            < datetime.now()
        ):
            raise CacheUnavailableError(f"cache file for {etf_code} is outdated")

    async def read_cache(self, etf_code: str) -> dict[str, Any]:
        path = f"cached_data/{etf_code}.json"
        if not (await exists(path)):
            raise CacheUnavailableError(f"cache file for {etf_code} not found")

        async with open(path, mode="r") as f:
            cached_data = loads(await f.read())

        await self.__check_expiration(etf_code, cached_data["last_updated"])
        return cached_data["content"]

    async def __construct_cache(self, raw_content: dict[str, Any]) -> dict[str, Any]:
        return {
            "last_updated": datetime.now().strftime(
                ManagerConfig().CACHED_FILE_TIMESTAMP_FORMAT,
            ),
            "content": raw_content,
        }

    async def write_cache(self, etf_code: str, raw_content: dict[str, Any]) -> None:
        path = f"cached_data/{etf_code}.json"
        async with open(path, mode="w") as f:
            logger.bind(etf_code=etf_code).info("writing data into cache file")
            content = await self.__construct_cache(raw_content)
            await f.write(dumps(content, indent=4))
            await f.flush()
