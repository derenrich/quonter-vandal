
from collections import defaultdict
from dataclasses import dataclass
import pytest
from pytest_asyncio.plugin import *
from quonter_vandal.diff_grouper import DiffGrouper, Timestamped
import time


@dataclass
class TimestampTester(Timestamped):
    title: str
    user: str
    timestamp: int
    data: str


@pytest.mark.asyncio
async def test_grouping_basic():

    out = []

    async def eject_fn(items):
        out.extend(items)

    loop = asyncio.get_event_loop()
    grouper = DiffGrouper(loop, eject_fn, 2)

    for i in range(5):
        t = TimestampTester(title="foo", user="bar",
                            timestamp=int(time.time()), data=str(i))
        await grouper.add(t)

    await asyncio.sleep(3)
    assert len(out) == 5


@pytest.mark.asyncio
async def test_grouping_surrender():

    out = []

    async def eject_fn(items):
        out.extend(items)

    loop = asyncio.get_event_loop()
    grouper = DiffGrouper(loop, eject_fn, 2)

    for i in range(5):
        t = TimestampTester(title="foo", user="bar",
                            timestamp=int(time.time()), data=str(i))
        await grouper.add(t)

    await asyncio.sleep(1)

    # same title but a new user arrived
    t = TimestampTester(title="foo", user="zar",
                        timestamp=int(time.time()), data=str(i))
    await grouper.add(t)
    await asyncio.sleep(1.6)
    assert len(out) == 0
    await asyncio.sleep(1)
    assert len(out) == 1


@pytest.mark.asyncio
async def test_grouping_complex():

    out = []

    async def eject_fn(items):
        out.extend(items)

    loop = asyncio.get_event_loop()
    grouper = DiffGrouper(loop, eject_fn, 5)

    for i in range(5):
        t = TimestampTester(title="foo", user="bar",
                            timestamp=int(time.time()), data=str(i))
        await grouper.add(t)
    await asyncio.sleep(4)
    assert len(out) == 0
    t = TimestampTester(title="foo", user="bar",
                        timestamp=int(time.time()), data="last")
    await grouper.add(t)
    await asyncio.sleep(4)
    assert len(out) == 0
    await asyncio.sleep(2)
    assert len(out) == 6


@pytest.mark.asyncio
async def test_grouping_multi_titles():

    out = defaultdict(list)

    async def eject_fn(items):
        out[items[0].title].extend(items)

    loop = asyncio.get_event_loop()
    grouper = DiffGrouper(loop, eject_fn, 5)

    for i in range(5):
        t = TimestampTester(title="foo", user="bar",
                            timestamp=int(time.time()), data=str(i))
        await grouper.add(t)
    await asyncio.sleep(2)
    for i in range(8):
        t = TimestampTester(title="bar", user="bar",
                            timestamp=int(time.time()), data=str(i))
        await grouper.add(t)
    await asyncio.sleep(2)
    assert len(out) == 0
    t = TimestampTester(title="foo", user="bar",
                        timestamp=int(time.time()), data="last")
    await grouper.add(t)
    await asyncio.sleep(4)
    assert len(out) == 1
    assert len(out["bar"]) == 8
    await asyncio.sleep(2)
    assert len(out) == 2
    assert len(out["foo"]) == 6
