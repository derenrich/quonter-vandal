import asyncio
from typing import List
from quonter_vandal.classifier import Classifier
from quonter_vandal.revision_stream import StreamEvent, StreamConfig, event_loop
from quonter_vandal.diff_grouper import DiffGrouper
from quonter_vandal.document_maker import DocumentMaker
import mwapi
import aiohttp
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
import time
from importlib.resources import files
import os
from jinja2 import Template
from quonter_vandal.results_logger import ResultsLogger, LogLine, ResultsFetcher

TOOLFORGE_MODE = os.environ.get('TOOLFORGE', '0') == '1'
app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def handle_root():
    html_template = Template(
        files("quonter_vandal").joinpath("index.html").read_text())
    return HTMLResponse(html_template.render())


@app.get("/time")
async def handle_time():
    return {"time": time.time()}

if TOOLFORGE_MODE:
    @app.get("/results/{page_num}")
    async def handle_results(page_num: int):
        fetcher = ResultsFetcher()
        return fetcher.fetch_vandalous(10, page_num * 10)


def start_service():
    mw_session = mwapi.AsyncSession('https://www.wikidata.org',
                                    user_agent='Quonter Vandal')
    session = aiohttp.ClientSession()
    dm = DocumentMaker(mw_session, session)
    classifier = Classifier()

    logger = None
    if TOOLFORGE_MODE:
        logger = ResultsLogger()

    loop = asyncio.get_event_loop()
    config = StreamConfig(logFeatures=True)

    async def handle_edit_group(edits: List[StreamEvent]):
        assert len(edits) > 0
        oldid = edits[0].rev_old
        newid = edits[-1].rev_new
        if oldid and newid:
            res = dm.make_document(oldid, newid)
            doc = await res
            if doc:
                classification = None  # await classifier.classify(doc)
                if logger:
                    if len(doc) > 4096:
                        print("===TOO LONG", len(doc))
                        print(doc)
                    if classification:
                        label = str(
                            classification.revert) if classification.revert is not None else ""
                        log = LogLine(doc, oldid, newid,
                                      classification.doc, label, "")
                        logger.log(log)
                    else:
                        log = LogLine(doc, oldid, newid, "", "", "")
                        logger.log(log)
                else:
                    print(doc, "--->", classification)

    grouper = DiffGrouper(loop, handle_edit_group, 240)

    async def handle_diff(diff: StreamEvent, filtered: bool):
        print(".", end="", flush=True)
        await grouper.add(diff, filtered)

    @app.get("/groups")
    async def handle_grouper_status():
        return {
            "groups": await grouper.status()
        }

    diff_stream = event_loop(config, handle_diff)

    diff_stream_task = loop.create_task(diff_stream)


start_service()
