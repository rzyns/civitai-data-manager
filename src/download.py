from abc import abstractmethod
from typing import override
import attrs
from pydantic import DirectoryPath
import pydantic
from pathlib import Path
import asyncio
from attrs import define
import aiohttp

from civitai_manager.utils.config import Config
from data import ModelData


@define
class DownloadTask:
    url: str
    dest: Path

    config: Config

    model: ModelData | None = attrs.field(default=None)


DEFAULT_PRIORITY = 10

class AbstractDownloadQueue:
    @abstractmethod
    async def add(self, task: DownloadTask, priority: int | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self) -> tuple[int, DownloadTask]:
        raise NotImplementedError

    @abstractmethod
    def empty(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def wait(self) -> None:
        raise NotImplementedError

@define
class DownloadQueue(AbstractDownloadQueue):
    dest_dir: DirectoryPath = attrs.field(converter=pydantic.TypeAdapter(DirectoryPath).validate_python, factory=Path)
    config: Config = attrs.field(factory=Config)
    input_queue: asyncio.PriorityQueue[tuple[int, DownloadTask]] = attrs.field(factory=asyncio.PriorityQueue[tuple[int, DownloadTask]])
    default_priority: int = attrs.field(default=DEFAULT_PRIORITY)

    @override
    async def add(self, task: DownloadTask, priority: int | None = None):
        await self.input_queue.put((self.default_priority if priority is None else priority, DownloadTask(url=task.url, dest=self.dest_dir, config=self.config, model=task.model)))

    @override
    async def get(self) -> tuple[int, DownloadTask]:
        return await self.input_queue.get()

    @override
    def empty(self) -> bool:
        return self.input_queue.empty()

    @override
    async def start(self):
        while not self.input_queue.empty():
            _priority, task = await self.get()

            headers: dict[str, str] = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36'}

            async with aiohttp.ClientSession() as session:
                async with session.get(task.url, headers=headers) as response:
                    a = await response.text(encoding="utf-8")
