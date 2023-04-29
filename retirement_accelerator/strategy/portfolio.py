from typing import Any, Callable

from retirement_accelerator.helper import GatheringTaskGroup
from retirement_accelerator.strategy.indicators import Indicator


class Portfolio:
    def __init__(
        self,
        name: str,
        data: dict[str, Any],
        indicators: tuple[Indicator, ...],
    ) -> None:
        self.__name = name
        self.__data = data
        self.__indicators = indicators

    async def __pick(self, indicator: Indicator) -> set[str]:
        return await indicator.scan(self.__data)

    async def pick(self) -> set[Any]:
        async with GatheringTaskGroup() as tg:
            for indicator in self.__indicators:
                tg.create_task(self.__pick(indicator))

            results = list(await tg.results())
            return results[0].intersection(*results[1:]) if results else set()

    async def rank(self, sort_key: Callable[[dict[str, Any]], Any]) -> None:
        print(f"=====[{self.__name}]=====\n")
        candidates = (
            (etf_code, sort_key(self.__data[etf_code]))
            for etf_code in await self.pick()
        )
        print(" " * 10 + f"{sort_key.__name__}")
        for candidate in sorted(candidates, key=lambda x: x[1]):
            print(f"{candidate[0]:<10}{candidate[1]}")
