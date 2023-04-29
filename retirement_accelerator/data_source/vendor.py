from typing import Any

from aiohttp import ClientSession, ContentTypeError
from loguru import logger
from retirement_accelerator.config import ManagerConfig
from retirement_accelerator.data_source.cache import ProviderCache
from retirement_accelerator.errors import RetirementAcceleratorError
from retirement_accelerator.helper import Singleton


class DataVendorError(RetirementAcceleratorError):
    pass


class VendorTwelveData(Singleton):
    async def __construct_url(self, etf_code: str) -> Any:
        return (
            f"{ManagerConfig().EODHD_API_ENDPOINT}"
            f"/{etf_code}"
            f"?api_token={ManagerConfig().EODHD_API_KEY}"
        )

    async def __get_session(self) -> ClientSession:
        return ClientSession()

    async def get_fundamental_data(self, etf_code: str) -> dict[str, Any]:
        async with await self.__get_session() as session:
            logger.info("requesting data from vendor", vendor="twelve data")
            async with session.get(
                await self.__construct_url(etf_code),
            ) as resp:
                try:
                    return await resp.json()
                except ContentTypeError as err:
                    raise DataVendorError(
                        "failed to decode response from vendor"
                    ) from err
