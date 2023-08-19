from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional
import mwapi
from itertools import islice
from quonter_vandal.config import language_preferences, wikis, prop_datatypes, props
from quonter_vandal.util import grouper
import json
import asyncio
from qwikidata.entity import WikidataItem
from qwikidata.typedefs import MonolingualTextValue, LanguageCode, PropertyId
from collections import defaultdict


@dataclass
class EntityInfo:
    label: Optional[str]
    label_lang: Optional[str]
    description: Optional[str]
    description_lang: Optional[str]


@dataclass
class Statement:
    pid: str
    pid_label: str
    pid_label_lang: str

    qid: str
    qid_label: str
    qid_label_lang: str
    qid_description: str
    qid_description_lang: str


@dataclass
class Label:
    label: str
    llang: str


@dataclass
class RevisionContent:
    label: Any  # monolingual text value
    description: Any
    aliases: List[Any]
    sitelinks: List[Any]
    claims: Mapping[str, List[EntityInfo] | dict | str]


class LookupEntities:
    """
    Look up  descriptions and labels of a list of entities at the current time.
    """

    def __init__(self, session: mwapi.AsyncSession):
        self.session = session

    async def lookup_entities(self, entities: List[str]) -> Dict[str, EntityInfo]:
        """
        Lookup entities by their QIDs.

        :param entities: List of QIDs
        :return: Dict of entities
        """

        out = {}
        # sort this for determinism in testing
        chunked_entities = grouper(40, sorted(set(entities)))
        for entity_block in chunked_entities:
            params = {
                'action': 'wbgetentities',
                'ids': "|".join(entity_block),
                'props': 'labels|descriptions',
                'languages':  "|".join(language_preferences),
                'format': 'json'
            }
            result = await self.session.get(params)
            entity_results: Dict[str, Any] = result['entities']
            for qid, data in entity_results.items():
                assert data["type"] == "item" or data['type'] == 'property'
                assert data["id"] == qid
                labels = data["labels"]
                label = None
                label_lang = None
                for lang in language_preferences:
                    if lang in labels:
                        label = labels[lang]["value"]
                        label_lang = lang
                        break
                descriptions = data["descriptions"]
                description = None
                description_lang = None
                for lang in language_preferences:
                    if lang in descriptions:
                        description = descriptions[lang]["value"]
                        description_lang = lang
                        break
                out[qid] = EntityInfo(
                    label, label_lang, description, description_lang)
        return out


class LookupItemAtRevision:
    """
    Looks up the contents of an item at a given revision.
    """

    def __init__(self, session: mwapi.AsyncSession):
        self.session = session

    async def lookup_item_at_revision(self, qid: str, revision_id: int) -> Optional[Any]:
        """
        Lookup an item at a given revision.

        :param qid: QID of item
        :param revision_id: Revision ID to look up
        :return: Dict of item
        """
        params = {
            'action': 'query',
            'prop': 'revisions',
            'rvprop': 'content|ids',
            'titles': qid,
            'rvstartid': revision_id,
            'format': 'json',
            'rvslots': 'main',
            'rvlimit': 1
        }
        result = await self.session.get(params)
        pages = result['query']['pages']
        if "-1" in pages:
            return None

        page = pages[list(pages.keys())[0]]
        revisions = page['revisions']
        if not revisions or len(revisions) == 0:
            return None

        content = json.loads(revisions[0]['slots']['main']['*'])

        # clean out the bad stuff that won't parse for some reason
        if content['claims']:
            for pid, claims in content.get('claims', {}).items():
                for claim in claims:
                    datatype = prop_datatypes.get(pid, "wikibase-item")
                    claim['mainsnak']['datatype'] = datatype
                    if 'qualifiers' in claim:
                        del claim['qualifiers']
                        del claim['qualifiers-order']
                    if 'references' in claim:
                        del claim['references']

        item = WikidataItem(content)

        lang_out = None
        for lang in language_preferences:
            lang_code = LanguageCode(lang)
            label = item.get_label(lang_code)
            if label:
                lang_out = MonolingualTextValue(
                    dict(label=label, lang_code=lang_code))
                break

        description_out = []
        for lang in language_preferences:
            lang_code = LanguageCode(lang)
            description = item.get_description(lang_code)
            if description:
                description_out = MonolingualTextValue(
                    dict(label=description, lang_code=lang_code))
                break

        aliases_out = []
        for lang in language_preferences:
            lang_code = LanguageCode(lang)
            aliases = item.get_aliases(lang_code)
            if aliases:
                aliases_out = [MonolingualTextValue(
                    dict(label=a, lang_code=lang_code)) for a in aliases]
                break

        sitelinks = []
        sitelink_dict = item.get_sitelinks("")
        for wiki in wikis:
            if wiki in sitelink_dict:
                lang_code = LanguageCode(wiki)
                sitelinks.append(MonolingualTextValue(
                    dict(label=sitelink_dict[wiki]['title'], lang_code=lang_code)))

        claims = dict()

        for prop in props.keys():
            claims[prop] = item.get_truthy_claim_group(PropertyId(prop))

        qids_to_lookup = set()
        for prop, claim_group in claims.items():
            for claim in claim_group:
                if claim.mainsnak and claim.mainsnak.snak_datatype == "wikibase-item":
                    qids_to_lookup.add(claim.mainsnak.datavalue.value['id'])

        entity_data = dict()
        if qids_to_lookup:
            lookup_obj = LookupEntities(self.session)
            entity_data = await lookup_obj.lookup_entities(list(qids_to_lookup))

        claims_out = defaultdict(list)
        for prop, claim_group in claims.items():
            for claim in claim_group:
                prop_name = props[prop]
                if claim.mainsnak.snak_datatype == "wikibase-item":
                    qid = claim.mainsnak.datavalue.value['id']
                    entity_info = entity_data.get(qid, None)
                    if entity_info:
                        claims_out[prop_name].append(entity_info)
                else:
                    claims_out[prop_name].append(
                        claim.mainsnak.datavalue.value)

        return RevisionContent(
            label=lang_out,
            description=description_out,
            aliases=aliases_out,
            sitelinks=sitelinks,
            claims=claims_out
        )


if __name__ == '__main__':
    session = mwapi.AsyncSession('https://www.wikidata.org',
                                 user_agent='Quonter Vandal')

    loop = asyncio.get_event_loop()

    lookup = LookupItemAtRevision(session)
    import json
    revid = 1951767291
    revid = 1951763454
    res = loop.run_until_complete(
        lookup.lookup_item_at_revision('Q5', revid))
    if res is not None:
        for prop, claims in res.claims.items():
            print(prop)
            for claim in claims:
                print("\t", claim)
