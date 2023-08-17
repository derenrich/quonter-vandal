from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import mwapi
from itertools import islice
from quonter_vandal.config import language_preferences
from quonter_vandal.util import grouper


@dataclass
class EntityInfo:
    label: Optional[str]
    label_lang: Optional[str]
    description: Optional[str]
    description_lang: Optional[str]


class LookupEntities:

    def __init__(self, session: mwapi.Session):
        self.session = session

    def lookup_entities(self, entities: List[str], revision_id: int) -> Dict[str, EntityInfo]:
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
            result = self.session.get(params)
            entity_results: Dict[str, Any] = result['entities']
            for qid, data in entity_results.items():
                assert data["type"] == "item"
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
