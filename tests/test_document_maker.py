import mwapi
import pytest
from pytest_asyncio.plugin import *
import aiohttp
from quonter_vandal.document_maker import DocumentMaker


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_buggy_lookup():
    newid = 1956762765
    oldid = 1903569755

    mw_session = mwapi.AsyncSession('https://www.wikidata.org',
                                    user_agent='Quonter Vandal')
    session = aiohttp.ClientSession()
    dm = DocumentMaker(mw_session, session)

    qid_pid_info, prior_data, diff = await dm.make_document_data(oldid, newid)
    assert 'date of death' not in prior_data.claims
    assert len(diff.changes) == 3
