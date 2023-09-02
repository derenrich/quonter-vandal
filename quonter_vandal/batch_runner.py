import asyncio
import pickle
from typing import Tuple
import aiohttp
import tqdm
import mwapi
import random
from quonter_vandal.document_maker import DocumentMaker
import pandas as pd
import sys
from urllib.parse import urlparse, parse_qs
import yaml


def main(changes: list[Tuple[int, int]], outfile: str, responses: list[str]):
    mw_session = mwapi.AsyncSession('https://www.wikidata.org',
                                    user_agent='Quonter Vandal')
    session = aiohttp.ClientSession()
    loop = asyncio.get_event_loop()

    # shuffle the changes
    # random.shuffle(changes)

    dm = DocumentMaker(mw_session, session)
    out = []
    for ((oldid, newid), resp) in tqdm.tqdm(zip(changes, responses)):
        # print(f"Old: {oldid}, New: {newid}\n")
        try:
            res = loop.run_until_complete(dm.make_document(oldid, newid))
            out.append({"fromrevid": oldid, "torevid": newid,
                       "doc": res, "resp": resp})
        except:
            pass
    pickle.dump(out, open(outfile, "wb"))


if __name__ == "__main__":
    # dat = pickle.load(open("diffs_grouped_vandalous.2.pkl", "rb"))
    # INFILE = "diffs_grouped_vandalous.2.pkl"
    # OUTFILE = "diffs_with_docs_vandalous.pkl"
    # dat = pickle.load(open(INFILE, "rb"))

    df = pd.read_csv("edits2.csv")
    print(len(df))

    changes = []
    out = []

    for index, row in df.iterrows():
        url = row['Diff Url']
        revert = row['Revert?'] == 'y'
        rationale = row['Rationale']
        parsed_url = urlparse(url)
        args = parse_qs(parsed_url.query)
        oldid = args['oldid'][0]
        newid = args['diff'][0]
        changes.append((oldid, newid))
        resp = {"rationale": rationale, "revert": revert}

        out.append(yaml.dump(resp))

    print(out[-1])
    # for groups in for index, row in df.iterrows()::
    #    for group in groups:
    #        startid = group[0]['fromrevid']
    #        endif = group[-1]['torevid']
    #        doc = changes.append((startid, endif))

    OUTFILE = "hand_annotated_docs.2.pkl"
    main(changes, OUTFILE, responses=out)
