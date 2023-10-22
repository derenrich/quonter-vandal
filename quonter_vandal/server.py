import asyncio
from typing import List
from quonter_vandal.classifier import Classifier
from quonter_vandal.diff import Change, SitelinkChangeStatement
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
from contextlib import asynccontextmanager
from quonter_vandal.results_logger import ResultsLogger, LogLine, ResultsFetcher

TOOLFORGE_MODE = os.environ.get('TOOLFORGE', '0') == '1'


async def maybe_make_document(dm: DocumentMaker, oldid: int, newid: int):
    qid_pid_info, prior_data, diff, summary = await dm.make_document_data(oldid, newid)
    if len(diff.changes) == 1:
        # check if it's only sitelink changes (those are boring)
        change: Change = diff.changes[0]
        if type(change.field) == SitelinkChangeStatement:
            return None
    doc = await dm.make_document_from_data(oldid, newid,
                                           qid_pid_info, prior_data, diff, summary)
    return doc


loop = asyncio.get_event_loop()
context = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    if TOOLFORGE_MODE:
        fetcher = await ResultsFetcher.create_fetcher(loop)
        logger = await ResultsLogger.create_logger(loop)
        context['fetcher'] = fetcher
        context['logger'] = logger
    yield
    if TOOLFORGE_MODE:
        del context['fetcher']
        del context['logger']


def start_service():
    mw_session = mwapi.AsyncSession('https://www.wikidata.org',
                                    user_agent='Quonter Vandal')
    session = aiohttp.ClientSession()
    dm = DocumentMaker(mw_session, session)
    classifier = Classifier()

    config = StreamConfig(logFeatures=True)

    app = FastAPI(lifespan=lifespan)

    @app.get("/", response_class=HTMLResponse)
    async def handle_root():
        html_template = Template(
            files("quonter_vandal").joinpath("index.html").read_text())
        return HTMLResponse(html_template.render())

    @app.get("/considering", response_class=HTMLResponse)
    async def handle_considering():
        html_template = Template(
            files("quonter_vandal").joinpath("considering.html").read_text())
        return HTMLResponse(html_template.render())

    @app.get("/time")
    async def handle_time():
        return {"time": time.time()}

    @app.get("/diff/{oldid}/{newid}", response_class=HTMLResponse)
    async def fetch_diff(oldid: int, newid: int):
        html_template = Template(
            files("quonter_vandal").joinpath("diff.html").read_text())
        res = await session.get(
            f"https://www.wikidata.org/w/api.php?action=compare&prop=user|diff|title|rel|ids|timestamp|comment&fromrev={oldid}&torev={newid}&format=json")
        diff_json = await res.json()
        totitle = diff_json['compare']['totitle']
        res = await session.get(
            f"https://www.wikidata.org/w/api.php?action=wbformatentities&ids={totitle}&format=json")
        format_json = await res.json()
        title_html = format_json['wbformatentities'][totitle]
        diff_html = diff_json['compare']['*']
        out = {
            "title_html": title_html,
            "diff_html": diff_html,
            "from_rev": diff_json['compare']['fromrevid'],
        }
        return HTMLResponse(html_template.render(**out))

    async def handle_edit_group(edits: List[StreamEvent]):
        assert len(edits) > 0
        logger: ResultsLogger | None = context['logger']

        oldid = edits[0].rev_old
        newid = edits[-1].rev_new
        if oldid and newid:
            res = maybe_make_document(dm, oldid, newid)
            doc = await res
            if doc:
                classification = await classifier.classify(doc)
                if logger:
                    if len(doc) > 4096:
                        print("===TOO LONG", len(doc))
                        print(doc)
                    if classification:
                        label = str(
                            classification.revert) if classification.revert is not None else ""
                        log = LogLine(doc, oldid, newid,
                                      classification.doc, label, "")
                        await logger.log(log)
                    else:
                        log = LogLine(doc, oldid, newid, "", "", "")
                        await logger.log(log)
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

    if TOOLFORGE_MODE:
        @app.get("/results/{page_num}")
        async def handle_results(page_num: int) -> List[LogLine]:
            if context['fetcher']:
                print('fetching!')
                fetcher: ResultsFetcher = context['fetcher']
                return await fetcher.fetch_vandalous(10, page_num * 10)
            raise Exception("No fetcher enabled")

    diff_stream = event_loop(config, handle_diff)

    diff_stream_task = loop.create_task(diff_stream)
    return app


app = start_service()
