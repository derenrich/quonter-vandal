USER_AGENT = "Quonter Vandal"

# the languages in the order of preference for fetching/displaying
language_preferences = [
    'en',
    'de',
    'fr',
    'es',
    'ru',
    'it',
    'pt',
    'nl'
]


wikis = [
    'enwiki',
    'dewiki',
    'frwiki',
    'eswiki',
    'ruwiki',
    'itwiki',
    'ptwiki',
    'nlwiki',
    'jawiki',
    'plwiki',
    'viwiki',
    'zhwiki',
    'arwiki',
    'svwiki',
    'cebwiki',
    'svwiki',
    'fawiki',
    'shwiki',
    'kowiki',
    'trwiki',
    'nowiki',
    'enwikiquote',
    'itwikiquote',
    'plwikiquote',
    'enwikisource',
    'commonswiki'
]

wikis_to_url = {
    'enwiki': 'https://en.wikipedia.org',
    'dewiki': 'https://de.wikipedia.org',
    'frwiki': 'https://fr.wikipedia.org',
    'eswiki': 'https://es.wikipedia.org',
    'ruwiki': 'https://ru.wikipedia.org',
    'itwiki': 'https://it.wikipedia.org',
    'ptwiki': 'https://pt.wikipedia.org',
    'nlwiki': 'https://nl.wikipedia.org',
    'jawiki': 'https://ja.wikipedia.org',
    'plwiki': 'https://pl.wikipedia.org',
    'viwiki': 'https://vi.wikipedia.org',
    'zhwiki': 'https://zh.wikipedia.org',
    'arwiki': 'https://ar.wikipedia.org',
    'svwiki': 'https://sv.wikipedia.org',
    'cebwiki': 'https://ceb.wikipedia.org',
    'svwiki': 'https://sv.wikipedia.org',
    'fawiki': 'https://fa.wikipedia.org',
    'shwiki': 'https://sh.wikipedia.org',
    'kowiki': 'https://ko.wikipedia.org',
    'trwiki': 'https://tr.wikipedia.org',
    'nowiki': 'https://no.wikipedia.org',
    'enwikiquote': 'https://en.wikiquote.org',
    'itwikiquote': 'https://it.wikiquote.org',
    'plwikiquote': 'https://pl.wikiquote.org',
    'enwikisource': 'https://en.wikisource.org',
    'commonswiki': 'https://commons.wikimedia.org'
}

props = {
    'P31': 'instance of',
    'P279': 'subclass of',
    'P361': 'part of',
    'P21': 'gender',
    'P27': 'country of citizenship',
    'P17': 'country',
    'P495': 'country of origin',
    'P131': 'located in the administrative territorial entity',
    'P276': 'location',
    'P19': 'place of birth',
    'P625': 'coordinate location',
    'P735': 'first name',
    'P734': 'family name',
    'P569': 'date of birth',
    'P570': 'date of death',
    'P571': 'inception',
    'P580': 'start time',
    'P582': 'end time',
    'P585': 'point in time',
    'P577': 'publication date',
    'P101': 'field of work',
    'P106': 'occupation',
    'P69': 'educated at',
    'P170': 'creator',
    'P136': 'genre',
    'P452': 'industry',
    'P641': 'sport',
    'P175': 'performer',
    'P360': 'is a list of',
    'P86': 'composer',
    'P607': 'conflict',
    'P1269': 'facet of',
    'P674': 'characters',
    'P172': 'ethnic group',
    'P112': 'founded by',
    'P400': 'platform',
}

prop_datatypes = {
    'P31': 'wikibase-item',  # 'instance of',
    'P279': 'wikibase-item',  # 'subclass of',
    'P361': 'wikibase-item',  # 'part of',
    'P21': 'wikibase-item',  # 'gender',
    'P27': 'wikibase-item',  # 'country of citizenship',
    'P17': 'wikibase-item',  # 'country',
    'P495': 'wikibase-item',  # 'country of origin',
    'P131': 'wikibase-item',  # 'located in the administrative territorial entity',
    'P276': 'wikibase-item',  # 'location',
    'P19': 'wikibase-item',  # 'place of birth',
    'P625': 'globe-coordinate',  # 'coordinate location',
    'P735': 'wikibase-item',  # 'first name',
    'P734': 'wikibase-item',  # 'family name',
    'P569': 'time',  # 'date of birth',
    'P570': 'time',  # 'date of death',
    'P571': 'time',  # 'inception',
    'P580': 'time',  # 'start time',
    'P582': 'time',  # 'end time',
    'P585': 'time',  # 'point in time',
    'P577': 'time',  # 'publication date',
    'P101': 'wikibase-item',  # 'field of work',
    'P106': 'wikibase-item',  # 'occupation',
    'P69': 'wikibase-item',  # 'educated at',
    'P170': 'wikibase-item',  # 'creator',
    'P136': 'wikibase-item',  # 'genre',
    'P452': 'wikibase-item',  # 'industry',
    'P641': 'wikibase-item',  # 'sport',
    'P175': 'wikibase-item',  # 'performer',
    'P360': 'wikibase-item',  # 'is a list of',
    'P86': 'wikibase-item',  # 'composer',
    'P607': 'wikibase-item',  # 'conflict',
    'P1269': 'wikibase-item',  # 'facet of',
    'P674': 'wikibase-item',  # 'characters',
    'P172': 'wikibase-item',  # 'ethnic group',
    'P112': 'wikibase-item',  # 'founded by',
    'P400': 'wikibase-item',  # 'platform',
}
