from typing import Any, Callable

from retirement_accelerator.helper import GatheringTaskGroup


class Indicator:
    def __init__(
        self,
        func_metric: Callable[[dict[str, Any]], Any],
        func_rule: Callable[[float], bool] | Callable[[tuple[float, ...]], bool],
    ) -> None:
        self.__func_metric = func_metric
        self.__func_rule = func_rule

    async def __scan(
        self,
        information: dict[str, Any],
    ) -> bool:
        return self.__func_rule(self.__func_metric(information))

    async def scan(self, data: dict[str, Any]) -> set[str]:
        async with GatheringTaskGroup() as tg:
            for information in data.values():
                tg.create_task(self.__scan(information))

            results = await tg.results()

        return set(etf_code for etf_code, result in zip(data.keys(), results) if result)


def max_annual_mgmt_charge(information: dict[str, Any]) -> float:
    return float(information["ETF_Data"]["Max_Annual_Mgmt_Charge"])


def total_assets(information: dict[str, Any]) -> float:
    return float(information["ETF_Data"]["TotalAssets"])


def asset_allocation_bond(information: dict[str, Any]) -> float:
    return float(information["ETF_Data"]["Asset_Allocation"]["Bond"]["Long_%"])


def asset_allocation_stock_us(information: dict[str, Any]) -> float:
    return float(information["ETF_Data"]["Asset_Allocation"]["Bond"]["Stock US"])


def asset_allocation_stock_non_us(information: dict[str, Any]) -> float:
    return float(information["ETF_Data"]["Asset_Allocation"]["Bond"]["Stock non-US"])


def top_world_region(information: dict[str, Any]) -> tuple[Any, Any] | None:
    hold = None
    for region, ratio in information["ETF_Data"]["World_Regions"].items():
        ratio = float(ratio["Equity_%"])
        if hold is None or ratio > hold[1]:
            hold = (region, ratio)
    return hold


def top_sector_weights(information: dict[str, Any]) -> tuple[Any, Any] | None:
    hold = None
    for sector, ratio in information["ETF_Data"]["Sector_Weights"].items():
        ratio = float(ratio["Equity_%"])
        if hold is None or ratio > hold[1]:
            hold = (sector, ratio)
    return hold


def dividend_yield_factor(information: dict[str, Any]) -> float:
    return float(
        information["ETF_Data"]["Valuations_Growth"]["Valuations_Rates_Portfolio"][
            "Dividend-Yield Factor"
        ]
    )


def morning_star_ratio(information: dict[str, Any]) -> float:
    return float(information["ETF_Data"]["MorningStar"]["Ratio"])


def morning_star_ratio_sustainability(information: dict[str, Any]) -> float:
    return float(information["ETF_Data"]["MorningStar"]["Sustainability_Ratio"])


def returns_1y(information: dict[str, Any]) -> float:
    return float(information["ETF_Data"]["Performance"]["Returns_1Y"])


def returns_3y(information: dict[str, Any]) -> float:
    return float(information["ETF_Data"]["Performance"]["Returns_3Y"])


def returns_5y(information: dict[str, Any]) -> float:
    return float(information["ETF_Data"]["Performance"]["Returns_5Y"])


def returns_10y(information: dict[str, Any]) -> float:
    return float(information["ETF_Data"]["Performance"]["Returns_10Y"])
