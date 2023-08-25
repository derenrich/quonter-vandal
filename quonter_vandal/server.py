import asyncio
from typing import List
from quonter_vandal.revision_stream import StreamEvent, StreamConfig, event_loop
from quonter_vandal.diff_grouper import DiffGrouper
from quonter_vandal.document_maker import DocumentMaker
import mwapi
import aiohttp
from aiohttp import web
import json
import time


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def handle_time(request):
    return web.Response(text=str(time.time()))


app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/time', handle_time)])


async def start_server(app: web.Application):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()


def main():
    mw_session = mwapi.AsyncSession('https://www.wikidata.org',
                                    user_agent='Quonter Vandal')
    session = aiohttp.ClientSession()
    dm = DocumentMaker(mw_session, session)

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
                print(doc)

    grouper = DiffGrouper(loop, handle_edit_group, 240)

    async def handle_diff(diff: StreamEvent):
        print(".", end="", flush=True)
        await grouper.add(diff)

    async def handle_grouper_status(request):
        return web.Response(
            text=json.dumps(await grouper.status()),
            content_type="application/json"
        )

    app.add_routes([web.get('/groups', handle_grouper_status)])

    diff_stream = event_loop(config, handle_diff)

    server_task = loop.create_task(start_server(app))
    diff_stream_task = loop.create_task(diff_stream)
    run_server_task = asyncio.gather(server_task, diff_stream_task)

    loop.run_until_complete(run_server_task)


if __name__ == "__main__":
    main()
