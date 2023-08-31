import asyncio
from typing import List
from quonter_vandal.revision_stream import StreamEvent, StreamConfig, event_loop
from quonter_vandal.diff_grouper import DiffGrouper
from quonter_vandal.document_maker import DocumentMaker
import mwapi
import aiohttp
from flask import Flask, jsonify, request
import json
import time
from threading import Thread

app = Flask(__name__)


@app.get("/")
def read_root():
    return jsonify({"Hello": "World"})


@app.get("/time")
async def handle_time():
    return jsonify({"time": time.time()})


def start_service():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    mw_session = mwapi.AsyncSession('https://www.wikidata.org',
                                    user_agent='Quonter Vandal')
    session = aiohttp.ClientSession()
    dm = DocumentMaker(mw_session, session)

    config = StreamConfig(logFeatures=True)

    async def handle_edit_group(edits: List[StreamEvent]):
        assert len(edits) > 0
        oldid = edits[0].rev_old
        newid = edits[-1].rev_new
        if oldid and newid:
            res = dm.make_document(oldid, newid)
            doc = await res
            if doc:
                print(doc)

    grouper = DiffGrouper(loop, handle_edit_group, 240)

    async def handle_diff(diff: StreamEvent):
        print(".", end="", flush=True)
        await grouper.add(diff)

    @app.get("/groups")
    async def handle_grouper_status():
        return jsonify({
            "groups": await grouper.status()
        })

    diff_stream = event_loop(config, handle_diff)
    diff_stream_task = loop.create_task(diff_stream)
    loop.run_until_complete(diff_stream_task)


t = Thread(target=start_service)
t.start()
