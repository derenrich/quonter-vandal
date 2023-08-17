from quonter_vandal.lookup import LookupEntities
import mwapi
import pytest


@pytest.mark.vcr()
def test_lookup():
    session = mwapi.Session('https://www.wikidata.org',
                            user_agent='Quonter Vandal')
    lookup = LookupEntities(session)
    entities = lookup.lookup_entities(
        set(['Q42', 'Q5', 'Q3712743', 'Q2994625']), 4)

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
