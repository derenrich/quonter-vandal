import asyncio
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Optional, Self
import aiohttp
from aiohttp import client_exceptions
from quonter_vandal.diff_grouper import Timestamped
from quonter_vandal.sse_client import EventSource
import time
import json
import traceback


@dataclass
class StreamConfig:
    logFeatures: bool = False


@dataclass
class StreamEvent(Timestamped):
    wiki: str
    type: str
    namespace: int
    bot: bool
    patrolled: bool
    minor: bool
    user: str
    comment: str
    timestamp: int
    rev_old: Optional[int]
    rev_new: Optional[int]
    title: str

    @classmethod
    def from_json(cls, json: dict) -> Self:
        return cls(
            wiki=json.get('wiki'),
            type=json.get('type'),
            namespace=json.get('namespace'),
            bot=json.get('bot'),
            patrolled=json.get('patrolled'),
            minor=json.get('minor'),
            user=json.get('user'),
            comment=json.get('parsedcomment'),
            timestamp=json.get('timestamp'),
            title=json.get('title'),
            rev_old=json.get('revision', {}).get('old'),
            rev_new=json.get('revision', {}).get('new')
        )


loop = asyncio.get_event_loop()

WIKIMEDIA_STREAM_URL = 'https://stream.wikimedia.org/v2/stream/recentchange'


class AsyncRetryingSseClient:
    def __init__(self, URL=WIKIMEDIA_STREAM_URL):
        self._url = URL
        self.client = EventSource(self._url)
        self._awaiting_iter = False

    def __aiter__(self):
        self._client_iter = None
        return self

    async def _reconnect(self):
        try:
            self._client_iter = await self.client.__aenter__()
            return self._client_iter
        except (ConnectionError, asyncio.TimeoutError, client_exceptions.ClientPayloadError, OSError):
            await asyncio.sleep(2)
            return await self._reconnect()

    async def __anext__(self):
        if not self._client_iter:
            self._client_iter = await self._reconnect()
        try:
            n = await anext(self._client_iter)
            return n
        except (ConnectionError, asyncio.TimeoutError, client_exceptions.ClientPayloadError, OSError, ValueError):
            print("iteration fail; reconnect")
            await asyncio.sleep(2)
            await self.client.__aexit__(None, None, None)
            self.client = EventSource(
                self._url, last_event_id=self.client.last_event_id)
            self._client_iter = await self._reconnect()
            return await anext(self)


def filter_event(event_json) -> bool:
    """
    Filter out events that we don't care about.
    """
    return event_json.get('wiki') == 'wikidatawiki' and \
        event_json.get('type') == 'edit' and \
        event_json.get('namespace') == 0 and \
        event_json.get('bot') is False


async def event_loop(config: StreamConfig, callback: Callable[[StreamEvent, bool], Awaitable[Any]]) -> None:

    while True:
        try:
            print("starting event loop for revision stream")
            client = AsyncRetryingSseClient()
            async for event in client:
                event_json = json.loads(event.data)
                stream_event = StreamEvent.from_json(event_json)
                if filter_event(event_json):
                    try:
                        await callback(stream_event, stream_event.patrolled)
                    except:
                        # print stacktrace
                        print("revision stream callback failed")
                        traceback.print_exc()

        except asyncio.CancelledError:
            print("cancelled revision stream")
            raise
        except:
            print("failed to fetch from revision stream")
            traceback.print_exc()


async def printer(x, filtered):
    print(x)

if __name__ == "__main__":
    import sys
    import mwapi
    mw_session = mwapi.AsyncSession('https://www.wikidata.org',
                                    user_agent='Quonter Vandal')
    session = aiohttp.ClientSession()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(event_loop(StreamConfig(True),  printer))
