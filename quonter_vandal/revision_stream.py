import asyncio
from dataclasses import dataclass
import aiohttp
from aiosseclient import aiosseclient, Event
import time
import json


@dataclass
class StreamConfig:
    logFeatures: bool = False


loop = asyncio.get_event_loop()

WIKIMEDIA_STREAM_URL = 'https://stream.wikimedia.org/v2/stream/recentchange'


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
    async with aiohttp.ClientSession() as session:
        async for event in aiosseclient(WIKIMEDIA_STREAM_URL):
            event_json = json.loads(event.data)
            if not filter_event(event_json):
                print(".", end="", flush=True)
                continue
            print(event)

x = loop.run_until_complete(event_loop(StreamConfig(logFeatures=True)))
