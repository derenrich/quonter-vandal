import asyncio
from dataclasses import dataclass
import dataclasses
from typing import Any, Awaitable, Callable, List, Mapping, TypeVar, Generic
from quonter_vandal.config import IGNORED_QIDS
from collections import defaultdict
import time


@dataclass
class Timestamped:
    timestamp: int
    user: str
    title: str


T = TypeVar('T', bound=Timestamped, contravariant=True)


class DiffGrouper(Generic[T]):
    def __init__(self, loop: asyncio.AbstractEventLoop, eject_fn: Callable[[List[T]], Awaitable[Any]], eject_delay: int = 60):
        self._eject_fn = eject_fn
        self._buffer: dict[str, List[T]] = defaultdict(list)
        self._lock = asyncio.Lock()
        self._eject_delay = eject_delay
        self._loop_task = loop.create_task(self._main_loop())

    async def status(self) -> dict[str, List[dict]]:
        async with self._lock:
            return {k: [dataclasses.asdict(i) for i in v] for k, v in self._buffer.items()}

    async def _main_loop(self):
        while True:
            async with self._lock:
                try:
                    wipe_list = []
                    for key, q in self._buffer.items():
                        if len(q) > 0 and ((self._time() - q[-1].timestamp) > self._eject_delay):
                            await self._eject_fn(q)
                            wipe_list.append(key)
                    for key in wipe_list:
                        del self._buffer[key]
                except Exception as e:
                    import traceback
                    print("fail?", e)
                    print(traceback.format_exc())
            await asyncio.sleep(1)

    def _time(self):
        return time.time()

    async def add(self, item: T, filtered: bool = False):
        if item.title in IGNORED_QIDS:
            return
        async with self._lock:
            queue_ready = await self._check_user(item.title, item.user)
            if not queue_ready:
                await self._surrender_key(item.title)
            if not filtered:
                self._buffer[item.title].append(item)

    async def _check_user(self, title: str, user: str) -> bool:
        """
        Are we ready to append a diff to this title for this user?
        """

        q = self._buffer.get(title)
        if q is None or len(q) == 0:
            return True
        if q[-1].user == user:
            return True
        return False

    async def _surrender_key(self, key: str):
        """
        Before we could revert someone else there did something.
        Just give up on it.
        """
        del self._buffer[key]


async def printer(items: List[Timestamped]):
    print("eject")
    print(items)

if __name__ == "__main__":
    import time
    loop = asyncio.get_event_loop()

    grouper = DiffGrouper(loop, printer, 35)
    # loop.run_until_complete(grouper._loop)
    loop.run_until_complete(grouper.add(Timestamped(
        timestamp=int(time.time() - 30), user="a", title="a")))

    loop.run_until_complete(asyncio.sleep(10))
