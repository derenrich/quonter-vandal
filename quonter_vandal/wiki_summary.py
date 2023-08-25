from dataclasses import dataclass
import mwapi

from quonter_vandal.lookup import RevisionContent

from quonter_vandal.config import wikis, wikis_to_url, USER_AGENT


@dataclass
class SnippetResponse:
    snippet: str
    wiki: str


async def get_summary(revision_content: RevisionContent) -> SnippetResponse:

    sitelinks_by_langcode = dict()
    for sitelink in revision_content.sitelinks:
        sitelinks_by_langcode[sitelink['lang_code']] = sitelink['label']

    title = None
    wiki_url = None
    wiki = None
    for wiki in wikis:
        if wiki in sitelinks_by_langcode:
            title = sitelinks_by_langcode[wiki]
            wiki_url = wikis_to_url[wiki]
            break

    if not title or not wiki_url:
        raise Exception("No title or wiki_url found.")
    session = mwapi.AsyncSession(
        wiki_url, user_agent=USER_AGENT, timeout=5)

    params = {
        'action': 'query',
        'prop': 'extracts',
        'exchars': 225,
        'explaintext': 'true',
        'exsectionformat': 'plain',
        'titles': [title]
    }

    result = await session.get(params)

    if not result:
        raise Exception("No result returned.")
    pages = result['query']['pages']
    if not pages:
        raise Exception("No pages returned.")
    if len(pages) > 1:
        # this shouldn't happen
        raise Exception("More than one page returned.")
    page = pages[list(pages.keys())[0]]
    if page['title'] != title:
        # this shouldn't happen either
        raise Exception("Title returned doesn't match title requested.")
    return SnippetResponse(page['extract'].strip() + "...", wiki)
