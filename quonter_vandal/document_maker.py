from typing import Mapping, Optional, Tuple, List
import mwapi
import aiohttp
import asyncio
from quonter_vandal.config import surpressed_qid_descriptions
from quonter_vandal.diff import *
from quonter_vandal.lookup import LookupItemAtRevision, EntityInfo, LookupEntities, RevisionContent
from quonter_vandal.util import clip_list
from dataclasses import dataclass
from itertools import chain


from quonter_vandal.wiki_summary import get_summary


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

    @classmethod
    def _render_time(cls, time: Mapping[str, Any]) -> str:
        # handle negative dates
        if time['time'][0] == '-':
            _, y, m, d = time['time'].split("T")[0].strip().split("-")
        else:
            y, m, d = time['time'].split("T")[0].strip().split("-")
        y = y[1:]
        prec = time['precision']

        if prec >= 11:
            dt = f"{y}-{m}-{d}"
        elif prec == 10:
            dt = f"{y}-{m}"
        elif prec == 9:
            dt = y
        elif prec == 8:
            dt = f"{y} decade"
        elif prec == 7:
            dt = f"{y} century"
        elif prec == 8:
            dt = f"{y} millennium"
        else:
            dt = f"{y}"
        suffix = ""
        if time['time'][0] == '-':
            suffix = " BC"
        return dt + suffix

    @classmethod
    def _render_coordinate(cls, coord: Mapping[str, Any]) -> str:
        return f"{coord['latitude']} lat, {coord['longitude']} lon"

    def _revision_content_to_document(self, content: RevisionContent) -> str:
        doc = []

        if content.label:
            if content.label['lang_code'] == "en":
                doc.append(f"Label: {content.label['label']}")
            else:
                doc.append(
                    f"Label ({content.label['lang_code']}): {content.label['label']}")
        if content.description:
            if content.description['lang_code'] == "en":
                doc.append(f"Description: {content.description['label']}")
            else:
                doc.append(
                    f"Label ({content.description['lang_code']}): {content.description['label']}")

        if content.aliases:
            content.aliases = clip_list(content.aliases, 5)
            if content.aliases[0]['lang_code'] == "en":
                alias_line = f"Aliases:"
            else:
                alias_line = f"Aliases ({content.aliases[0]['lang_code']}):"
            alias_line += " " + \
                ", ".join([alias['label'] for alias in content.aliases])
            doc.append(alias_line)

        if content.sitelinks:
            doc.append("Sitelinks:")
            content.sitelinks = clip_list(content.sitelinks, 5)
            for sitelink in content.sitelinks:
                doc.append(f" {sitelink['lang_code']}:{sitelink['label']}")

        if content.claims:
            doc.append("Claims:")
            for prop, statements in content.claims.items():
                if len(statements) > 1:
                    doc.append(f"{prop}:")
                for e_info in clip_list(statements, 7):
                    if len(statements) == 1:
                        line = f"{prop}: "
                    else:
                        line = "  "

                    if type(e_info) == EntityInfo:
                        if e_info.label_lang == "en":
                            line += f"{e_info.label}"
                        else:
                            line += f"{e_info.label} ({e_info.label_lang})"
                    elif type(e_info) == dict:
                        if 'time' in e_info and e_info['time']:
                            line += self._render_time(e_info)
                        elif 'latitude' in e_info and e_info['latitude']:
                            line += self._render_coordinate(e_info)
                        else:
                            raise Exception(
                                f"not implemented yet for {type(e_info)}, {e_info}")
                    else:
                        raise Exception(
                            f"not implemented yet for {type(e_info)}, {e_info}")
                    doc.append(line)

        return "\n".join(doc)

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
            case Redirect():
                pass
            case SitelinkChangeStatement(_):
                pass
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
            case ReferenceValue(statements):
                for statement in statements:
                    if statement.value:
                        value_bucket = self._get_items_from_values(
                            statement.value)
                        bucket += value_bucket
                    statement_bucket = self._get_items_from_statement(
                        statement.field)
                    bucket += statement_bucket

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
        match field:
            case Alias(lang):
                if lang == "en":
                    return "Alias"
                return f"Alias ({lang})"
            case Description(lang):
                if lang == "en":
                    return "Description"
                return f"Description ({lang})"
            case Redirect():
                return "Redirect to"
            case Label(lang):
                if lang == "en":
                    return "Label"
                return f"Label ({lang})"
            case RegularStatement(pid):
                return f"{qid_map[pid].label}"
            case RankChangeStatement(pid):
                return f"Rank of {qid_map[pid].label}"
            case QualifierChangeStatement(pid):
                return f"Qualifier of {qid_map[pid].label}"
            case ReferenceChangeStatement(pid, value):
                return f"Reference of {qid_map[pid].label} for {self._statement_value_to_string(value, qid_map)}"
            case SitelinkChangeStatement():
                return "Sitelink"
            case _:
                raise Exception(f"Unknown statement type: {field}")

    def _statement_value_to_string(self, value: StatementValue, qid_map: Mapping[str, EntityInfo]) -> str:
        match value:
            case StatementQualifierValue(pid, value):
                return f"{qid_map[pid].label} for {self._statement_value_to_string(value, qid_map)}"
            case StatementPropertyValue(pid):
                return f"{qid_map[pid].label} ({qid_map[pid].description})"
            case StatementItemValue(qid):
                if qid not in surpressed_qid_descriptions:
                    return f"{qid_map[qid].label} ({qid_map[qid].description})"
                else:
                    return f"{qid_map[qid].label}"
            case StatementQuantityValue(quantity):
                return f"{quantity}"
            case StatementMonolingualTextValue(text, lang):
                if lang == "en":
                    return f"{text}"
                return f"{text} in {lang}"
            case StatementInternalLinkValue(href, text, lang):
                if lang == "en":
                    return f"[{text}]({href})"
                return f"[{text}]({href}) in {lang}"
            case StatementFileLink(href, text) | StatementExternalLinkValue(href, text):
                if href and href != text:
                    return f"[{text}]({href})"
                else:
                    return f"{text}"
            case StatementMathValue(val) | StatementTimeValue(val) | StatementStringValue(val) | \
                StatementLexemeValue(val) | StatementQuantityValue(val) | StatementGlobeCoordinateValue(val) | \
                    StatementNumberValue(val) | StatementRankValue(val) | StatementMusicValue(val) | StatementSpecialValue(val):
                return f"{val}"
            case ReferenceValue(statements):
                return " / ".join([self._statement_to_document(state, qid_map)
                                   for state in statements])
            case _:
                raise Exception(f"Unknown statement value: {value}")

    def _statement_to_document(self, statement: Statement, qid_map: Mapping[str, EntityInfo]) -> str:
        field = statement.field
        value = statement.value
        field_doc = self._statement_type_to_string(field, qid_map)
        value_doc = self._statement_value_to_string(value, qid_map)
        return f"{field_doc}: {value_doc}"

    def _diff_to_document(self, diff: Diff, qid_map: Mapping[str, EntityInfo]) -> str:
        docs = []
        # docs.append(f"Comment: {diff.comments}")
        tags = list(filter(lambda x: 'OAuth' not in x and 'reverted' not in x,
                    set(chain.from_iterable(diff.tags))))
        # doesn't seem very helpful
        # if tags:
        #    docs.append(f"Tags: {'/'.join(tags)}")
        for c in diff.changes:
            field = c.field
            old_value = c.old
            new_value = c.new
            if type(field) == RankChangeStatement and \
                old_value is None and type(new_value) == StatementRankValue and \
                    new_value.value == "normal":
                # this is very boring, so we skip it
                continue
            if type(field) == RankChangeStatement and \
                new_value is None and type(old_value) == StatementRankValue and \
                    old_value.value == "normal":
                # this is very boring, so we skip it
                continue
            field_doc = self._statement_type_to_string(field, qid_map)
            old_doc = None
            if old_value:
                old_doc = self._statement_value_to_string(old_value, qid_map)
            new_doc = None

            if new_value:
                new_doc = self._statement_value_to_string(new_value, qid_map)

            if old_doc and new_doc:
                docs.append(f"{field_doc}: '{old_doc}' changed to '{new_doc}'")
            elif old_doc:
                docs.append(f"{field_doc}: '{old_doc}' removed")
            elif new_doc:
                docs.append(f"{field_doc}: added '{new_doc}'")
        return "\n".join(docs)

    async def make_document_data(self, start_rev: int, end_rev: int) -> Any:
        # first get the diff
        differ = await async_get_diff(start_rev, end_rev, self._session)
        if not differ:
            raise Exception(
                f"Failed to get data for diff {start_rev} -> {end_rev} (no differ)")
        diff = differ.changes()

        qid = diff.title

        # now get the names of the qids/pids in the diff
        qid_pid_info_await = self._get_qid_map_for_diff(diff)
        # get the state of the item before the diff
        prior_data_await = self._lookup.lookup_item_at_revision(
            qid, start_rev)

        qid_pid_info, prior_data = await asyncio.gather(qid_pid_info_await, prior_data_await)

        if prior_data:
            try:
                summary = (await get_summary(prior_data))
                if not summary.snippet:
                    summary = None
            except:
                summary = None
        else:
            summary = None

        if not prior_data:
            raise Exception(
                f"Failed to get data for diff {start_rev} -> {end_rev}")
        return qid_pid_info, prior_data, diff, summary

    async def make_document(self, start_rev: int, end_rev: int) -> Optional[str]:
        try:
            qid_pid_info, prior_data, diff, summary = await self.make_document_data(start_rev, end_rev)
            doc = await self.make_document_from_data(start_rev, end_rev,
                                                     qid_pid_info, prior_data, diff, summary)
            return doc
        except Exception as e:
            import traceback
            print(f"Failed to make document for {start_rev} -> {end_rev}: {e}")
            traceback.print_exc()
            return None

    async def make_document_from_data(self, start_rev, end_rev, qid_pid_info, prior_data, diff, summary) -> Optional[str]:
        try:
            if len(diff.changes) == 0:
                # don't emit documents for null changes
                return None
            diff_doc = self._diff_to_document(diff, qid_pid_info)

            if summary and summary.snippet:
                summary_doc = f"\nSnippet ({summary.wiki})\n====\n {summary.snippet}\n"
            else:
                summary_doc = ""
            if summary and summary.categories:
                category_sub_doc = "\n".join(summary.categories)
                category_doc = f"\nCategories ({summary.wiki})\n====\n{category_sub_doc}\n"
            else:
                category_doc = ""

            item_doc = self._revision_content_to_document(prior_data)
            final_doc = f"Item\n====\n{item_doc}\n{summary_doc}\n{category_doc}\nEdit\n====\n{diff_doc}"
            return final_doc
        except Exception as e:
            import traceback
            print(f"Failed to make document for {start_rev} -> {end_rev}: {e}")
            traceback.print_exc()
            return None


if __name__ == "__main__":
    import sys
    mw_session = mwapi.AsyncSession('https://www.wikidata.org',
                                    user_agent='Quonter Vandal')
    session = aiohttp.ClientSession()
    loop = asyncio.get_event_loop()

    dm = DocumentMaker(mw_session, session)

    # 1955679209&oldid=1954306252
    # 1955680063&oldid=1848557346
    # 1955616425&oldid=1955615684
    start, args = sys.argv[1].split("?")
    _, _, newdif, oldif = args.split("=")
    newdif = newdif.split("&")[0]

    # import gzip
    # import json
    # with gzip.open("logs.jsonl", "r") as f:
    #    for line in f:
    #        d = json.loads(line)
    #        if d and 'old' in d and 'new' in d:
    #            oldif = d['old']
    #            newdif = d['new']
    #            lookup = loop.run_until_complete(
    #                dm.make_document(int(oldif), int(newdif)))
    #            print(lookup)
