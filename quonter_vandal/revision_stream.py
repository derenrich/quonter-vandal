import asyncio
from dataclasses import dataclass
from typing import Optional
import aiohttp
from aiohttp import client_exceptions
from sse_client import EventSource
import time
import json


@dataclass
class StreamConfig:
    logFeatures: bool = False


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

    async def __anext__(self):
        if not self._client_iter:
            self._client_iter = await self.client.__aenter__()
        try:
            n = await anext(self._client_iter)
            return n
        except (asyncio.TimeoutError, client_exceptions.ClientPayloadError, OSError):
            print("iteration fail; reconnect")
            await asyncio.sleep(1)
            await self.client.__aexit__(None, None, None)
            self.client = EventSource(
                self._url, last_event_id=self.client.last_event_id)
            self._client_iter = await self.client.__aenter__()
            return await anext(self)


def filter_event(event_json):
    """
    Filter out events that we don't care about.
    """
    return event_json.get('wiki') == 'wikidatawiki' and \
        event_json.get('type') == 'edit' and \
        event_json.get('namespace') == 0 and \
        event_json.get('bot') is False and \
        event_json.get('patrolled') is False


async def event_loop(config: StreamConfig) -> None:
    t = time.time()
    hits = 0
    misses = 0
    client = AsyncRetryingSseClient()
    async for event in client:
        event_json = json.loads(event.data)
        if not filter_event(event_json):
            # print(".", end="", flush=True)
            misses += 1
        else:
            if hits > 0 and hits % 100 == 0:
                print(f"{hits} hits, {misses} misses in {time.time() - t} seconds")
            hits += 1
