USER_AGENT = "Quonter Vandal /0.0 (https://qop.toolforge.org/)"

DB_NAME = "s55536__qop"

# the languages in the order of preference for fetching/displaying
language_preferences = [
    'en',
    'de',
    'fr',
    'es',
    'ru',
    'it',
    'pt',
    'nl',
    'ar',
    'uk',
    'bn',
    'sq',
    'he',
    'ko',
    'bg',
    'sk',
    'vi',
    'el',
    'sv',
    'hu',
    'id',
    'ast',
    'ga',
    'pl',
    'th',
    'fa',
    'ur',
    'mk',
    'be',
    'ml',
    'eu',
    'zh-hant'
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

surpressed_qid_descriptions = set([
    "Q13442814", "Q5412157", "Q5", "Q328", "Q1860", "Q5188229", "Q4167836", "Q229883", "Q6581097", "Q16521", "Q30", "Q7432", "Q1531570", "Q837615", "Q783521", "Q11573", "Q169514", "Q1194038", "Q48183", "Q82486", "Q4167410", "Q20641742", "Q7187", "Q51885189", "Q15241312", "Q8447", "Q905695", "Q54919", "Q20747295", "Q8054", "Q5531047", "Q206855", "Q30239", "Q6581072", "Q148", "Q11266439", "Q183", "Q145", "Q11920", "Q6985", "Q142", "Q13100073", "Q19652", "Q136736", "Q82955", "Q22809680", "Q82575", "Q22809711", "Q830106", "Q8502", "Q8449", "Q922063", "Q159", "Q10000", "Q174728", "Q177837", "Q13711410", "Q486972", "Q58943792", "Q2578548", "Q16", "Q2736", "Q23190881", "Q1551807", "Q1650915", "Q38", "Q20", "Q55", "Q28018111", "Q34", "Q28563569", "Q4022", "Q668", "Q604063", "Q15628808", "Q6973052", "Q29", "Q96", "Q3305213", "Q7850", "Q79007", "Q15700834", "Q12857515", "Q47246828", "Q7737", "Q1777301", "Q36669", "Q14005", "Q180445", "Q3047275", "Q54050", "Q17", "Q712226", "Q13406463", "Q6723", "Q17329259", "Q34266", "Q13407958", "Q36", "Q191168", "Q6655", "Q47542613", "Q36578", "Q101352", "Q11424", "Q532", "Q937857", "Q19938912", "Q15978631", "Q408", "Q252", "Q8229", "Q482994", "Q23397", "Q3863", "Q199698", "Q7736786", "Q36180", "Q200386", "Q15634506", "Q213", "Q60332278", "Q29940705", "Q30068043", "Q18916547", "Q188", "Q34740", "Q155", "Q150162", "Q564954", "Q33999", "Q11921", "Q63170780", "Q577", "Q794", "Q150", "Q41176", "Q17633526", "Q296955", "Q180686", "Q2886424", "Q423048", "Q3947", "Q16970", "Q27924673", "Q2745977", "Q58679", "Q16335166", "Q355304", "Q4259259", "Q30612", "Q861259", "Q48952", "Q83310", "Q11173", "Q33", "Q565", "Q4830453", "Q546003", "Q828224", "Q58035056", "Q51711", "Q483261", "Q45029998", "Q4783991", "Q1321", "Q23442", "Q21287602", "Q278487", "Q110874", "Q45029859", "Q1028181", "Q26936509", "Q14349455", "Q39825", "Q1146531", "Q867727", "Q27020041", "Q523716", "Q61779016", "Q61779006", "Q62115984", "Q56436498", "Q212", "Q62115934", "Q40", "Q15180", "Q62183372", "Q8035497", "Q21014462", "Q9903", "Q2456810", "Q184224", "Q5084", "Q14327652", "Q47521", "Q2493771", "Q9396337", "Q2668072", "Q2311683"
])


IGNORED_QIDS = set([
    'Q16943273',
    'Q4115189',
    'Q13406268',
    'Q15397819',
    'Q112795079'
])
