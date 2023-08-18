from quonter_vandal.lookup import LookupEntities, LookupItemAtRevision
import mwapi
import pytest
from pytest_asyncio.plugin import *


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_lookup():
    session = mwapi.AsyncSession('https://www.wikidata.org',
                                 user_agent='Quonter Vandal')
    lookup = LookupEntities(session)
    entities = await lookup.lookup_entities(
        set(['Q42', 'Q5', 'Q3712743', 'Q2994625']))

    assert entities['Q42'].label == 'Douglas Adams'
    assert entities['Q42'].label_lang == 'en'
    assert entities['Q42'].description == 'English science fiction writer and humourist'
    assert entities['Q42'].description_lang == 'en'

    assert entities['Q2994625'].label == 'consistance'
    assert entities['Q2994625'].label_lang == 'fr'
    assert entities['Q2994625'].description == None
    assert entities['Q2994625'].description_lang == None

    assert entities['Q3712743'].label == 'Dom'
    assert entities['Q3712743'].label_lang == 'es'
    assert entities['Q3712743'].description == 'Título honorífico'
    assert entities['Q3712743'].description_lang == 'es'


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_make_revision_content():
    session = mwapi.AsyncSession('https://www.wikidata.org',
                                 user_agent='Quonter Vandal')
    lookup = LookupItemAtRevision(session)
    content = await lookup.lookup_item_at_revision('Q5', 1954530026)

    assert content is not None
    assert content.label['label'] == 'human'
    assert content.label['lang_code'] == 'en'

    assert content.description['label'] == 'any member of Homo sapiens, unique extant species of the genus Homo, from embryo to adult'
    assert content.description['lang_code'] == 'en'

    assert 'human being' in [val['label'] for val in content.aliases]
    assert 'individual Homo sapien' in [
        val['label'] for val in content.aliases]

    assert 'enwiki' in [val['lang_code'] for val in content.sitelinks]
    assert 'enwikiquote' in [val['lang_code'] for val in content.sitelinks]
    assert 'nlwiki' in [val['lang_code'] for val in content.sitelinks]

    assert 'instance of' in content.claims
    assert 'organisms known by a particular common name' in [
        val.label for val in content.claims['instance of']]
    assert 'subclass of' in content.claims
    assert 'mammal' in [
        val.label for val in content.claims['subclass of']]

    assert 'part of' in content.claims
