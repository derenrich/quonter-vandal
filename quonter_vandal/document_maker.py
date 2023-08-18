from typing import Mapping, Optional, Tuple, List
import mwapi
import aiohttp
import asyncio
from quonter_vandal.diff import *
from quonter_vandal.lookup import LookupItemAtRevision, EntityInfo, LookupEntities
from dataclasses import dataclass


@dataclass
class QidPidBucket:
    pids: List[str]
    qids: List[str]

    @classmethod
    def make(cls) -> Self:
        return QidPidBucket([], [])

    def __add__(self, other: Self) -> Self:
        return QidPidBucket(self.pids + other.pids, self.qids + other.qids)

    def __iadd__(self, other: Self) -> Self:
        self.pids += other.pids
        self.qids += other.qids
        return self

    def add_pid(self, pid):
        self.pids.append(pid)

    def add_qid(self, qid):
        self.qids.append(qid)


class DocumentMaker:

    def __init__(self, mw_session: mwapi.AsyncSession, session: aiohttp.ClientSession) -> None:
        self._mw_session = mw_session
        self._session = session
        self._lookup = LookupItemAtRevision(mw_session)

    def _get_items_from_statement(self, field: StatementType) -> QidPidBucket:
        bucket = QidPidBucket.make()

        match field:
            case Alias(lang) | Description(lang) | Label(lang):
                pass  # nothing to parse
            case RegularStatement(pid) | RankChangeStatement(pid) | QualifierChangeStatement(pid):
                bucket.add_pid(pid)
            case ReferenceChangeStatement(pid, value):
                bucket.add_pid(pid)
                value_bucket = self._get_items_from_values(value)
                bucket += value_bucket
            case _:
                raise Exception(f"Unknown statement type: {field}")
        return bucket

    def _get_items_from_values(self, value: StatementValue) -> QidPidBucket:
        bucket = QidPidBucket.make()

        match value:
            case StatementQualifierValue(pid, value):
                bucket.add_pid(pid)
                value_bucket = self._get_items_from_values(value)
                bucket += value_bucket
            case StatementPropertyValue(pid):
                bucket.add_pid(pid)
            case StatementLexemeValue(lexeme):
                pass  # nobody uses lexemes
            case StatementItemValue(qid):
                bucket.add_qid(qid)
            case _:
                pass
        return bucket

    async def _get_qid_map_for_diff(self, diff: Diff) -> Mapping[str, EntityInfo]:

        bucket = QidPidBucket.make()

        for c in diff.changes:
            field = c.field
            old_value = c.old
            new_value = c.new

            bucket += self._get_items_from_statement(field)
            if old_value:
                bucket += self._get_items_from_values(old_value)
            if new_value:
                bucket += self._get_items_from_values(new_value)

        pids, qids = bucket.pids, bucket.qids

        lookup_entities = LookupEntities(self._mw_session)
        return await lookup_entities.lookup_entities(pids + qids)

    def _statement_type_to_string(self, field: StatementType, qid_map: Mapping[str, EntityInfo]) -> str:
        pass

    def _statement_value_to_string(self, value: StatementValue, qid_map: Mapping[str, EntityInfo]) -> str:
        pass

    def _diff_to_document(self, diff: Diff, qid_map: Mapping[str, EntityInfo]) -> str:
        docs = []
        for c in diff.changes:
            field = c.field
            old_value = c.old
            new_value = c.new
            field_doc = self._statement_type_to_string(field, qid_map)
            old_doc = None
            if old_value:
                old_doc = self._statement_value_to_string(old_value, qid_map)
            new_doc = None
            if new_value:
                new_doc = self._statement_value_to_string(new_value, qid_map)
            docs.append(f"{field_doc}: {old_doc} -> {new_doc}")
        return "\n".join(docs)

    async def make_document(self, start_rev: int, end_rev: int) -> Optional[str]:

        # first get the diff
        differ = await async_get_diff(start_rev, end_rev, self._session)
        if not differ:
            return None
        diff = differ.changes()

        qid = diff.title

        # now get the names of the qids/pids in the diff
        qid_pid_info_await = self._get_qid_map_for_diff(diff)
        # get the state of the item before the diff
        prior_data_await = self._lookup.lookup_item_at_revision(qid, start_rev)

        qid_pid_info, prior_data = await asyncio.gather(qid_pid_info_await, prior_data_await)

        return ""


if __name__ == "__main__":
    mw_session = mwapi.AsyncSession('https://www.wikidata.org',
                                    user_agent='Quonter Vandal')
    session = aiohttp.ClientSession()
    loop = asyncio.get_event_loop()

    dm = DocumentMaker(mw_session, session)

    lookup = loop.run_until_complete(dm.make_document(1916986831, 1916992133))
    print(lookup)
