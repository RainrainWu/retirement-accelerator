from asyncio import Task, TaskGroup, gather
from typing import Any, Iterable


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance


class GatheringTaskGroup(
    TaskGroup,
):
    def __init__(self) -> None:
        super().__init__()
        self.__tasks: list[Task[Any]] = []

    def create_task(self, coro, *, name=None, context=None) -> Task[Any]:
        task = super().create_task(coro, name=name, context=context)
        self.__tasks.append(task)
        return task

    async def results(self) -> Iterable[Any]:
        await gather(*self.__tasks)
        return (task.result() for task in self.__tasks)
