import asyncio
import pickle
from typing import Tuple
import aiohttp
import tqdm
import mwapi
import random
from quonter_vandal.document_maker import DocumentMaker


def main(changes: list[Tuple[int, int]], outfile: str):
    mw_session = mwapi.AsyncSession('https://www.wikidata.org',
                                    user_agent='Quonter Vandal')
    session = aiohttp.ClientSession()
    loop = asyncio.get_event_loop()

    # shuffle the changes
    random.shuffle(changes)

    dm = DocumentMaker(mw_session, session)
    out = []
    for (oldid, newid) in tqdm.tqdm(changes[0:1000]):
        # print(f"Old: {oldid}, New: {newid}\n")
        try:
            res = loop.run_until_complete(dm.make_document(oldid, newid))
            out.append({"fromrevid": oldid, "torevid": newid, "doc": res})
        except:
            pass
    pickle.dump(out, open(outfile, "wb"))


if __name__ == "__main__":
    # dat = pickle.load(open("diffs_grouped_vandalous.2.pkl", "rb"))
    INFILE = "diffs_grouped_vandalous.2.pkl"
    OUTFILE = "diffs_with_docs_vandalous.pkl"
    dat = pickle.load(open(INFILE, "rb"))
    print(len(dat))

    changes = []
    out = []
    for groups in dat:
        for group in groups:
            startid = group[0]['fromrevid']
            endif = group[-1]['torevid']
            doc = changes.append((startid, endif))

    main(changes, OUTFILE)
