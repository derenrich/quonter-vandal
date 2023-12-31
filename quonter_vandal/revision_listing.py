from dataclasses import dataclass
from typing import List, Optional, Dict
import requests
import aiohttp
import asyncio


@dataclass
class Revision:
    user: str
    timestamp: str
    comment: str
    tags: List[str]


def get_revisions(title: str, startid: int, endid: int) -> List[Revision]:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(async_get_revisions(title, startid, endid))


async def async_get_revisions(title: str, startid: int, endid: int, session: Optional[aiohttp.ClientSession] = None) -> List[Revision]:
    if not session:
        session = aiohttp.ClientSession()

    URL = f"https://www.wikidata.org/w/api.php?action=query&prop=revisions&titles={title}&rvprop=timestamp|user|comment|tags&rvstartid={startid}&rvendid={endid}&format=json"
    resp = await session.get(URL)
    result = await resp.json()
    if not result:
        raise Exception("No result returned.")
    pages = result['query']['pages']
    if not pages:
        raise Exception("No pages returned.")
    if len(pages) > 1:
        # this shouldn't happen
        raise Exception("More than one page returned.")
    page = pages[list(pages.keys())[0]]
    if page['title'] != title:
        # this shouldn't happen either
        raise Exception("Title returned doesn't match title requested.")
    revisions = page.get('revisions')
    if not revisions or len(revisions) < 2:
        raise Exception(
            "Less than two revisions returned. Expected at least two.")
    return [Revision(r['user'], r['timestamp'], r['comment'], r.get('tags', [])) for r in revisions[0:-1]]
