from dataclasses import dataclass
import requests
from typing import Optional, Self, Union, Any, List, Dict
from quonter_vandal.revision_listing import get_revisions
from bs4 import BeautifulSoup
from bs4.element import Tag, PageElement
from enum import Enum



@dataclass
class StatementValue:
    @staticmethod
    def extract_pid(a: Tag) -> str:
        # check if it's a link
        if a.name == "a" and a.attrs["title"].startswith("P"):
            # get the title
            title = a.attrs["title"]
            pid = title.split(":")[-1]
            return pid
        # throw error
        raise Exception("Expected a tag for the main pid")
    
    @staticmethod
    def extract_qid(a: Tag) -> str:
        # check if it's a link
        if a.name == "a" and a.attrs["title"].startswith("Q"):
            # get the title
            title = a.attrs["title"]
            qid = title.split("/")[-1]
            return qid
        # throw error
        raise Exception("Expected a QID in the link")

    @staticmethod
    def extract_value(a: PageElement, wrapped=False) -> Self:
        if type(a) == Tag:
            if "wb-time-details" in a.attrs.get("class", []):
                return StatementTimeValue.from_block(a)
            elif a.name == "a":
                if "external" in a.attrs.get("class", []):
                    return StatementExternalLinkValue(a.attrs['href'], a.text)
                else:
                    return StatementItemValue(StatementValue.extract_qid(a))
            else:
                links = a.find_all("a")
                if links:
                    # either an external link, external identifier or a link to another item
                    if "external" in links[0].attrs.get("class", []):
                        return StatementExternalLinkValue(links[0].attrs['href'], links[0].text)
                    elif links[0].attrs["href"].startswith("/wiki/Q"):
                        # internal property link
                        return StatementItemValue(StatementValue.extract_qid(links[0]))
                    elif "hreflang" in links[0].attrs:
                        return StatementInternalLinkValue(links[0].attrs["href"], links[0].text, links[0].attrs["hreflang"])
                    elif "extiw" in links[0].attrs.get("class", []):
                        return StatementFileLink(links[0].attrs["href"], links[0].text)
                else:
                    monolingual_text = a.find("span", class_="wb-monolingualtext-value")
                    if type(monolingual_text) == Tag:
                        return StatementMonolingualTextValue(monolingual_text.text, monolingual_text.attrs["lang"])
                    somevalue = a.find("span", class_="wikibase-snakview-variation-somevaluesnak")
                    if somevalue:
                        return StatementSpecialValue("somevalue")
                    novalue = a.find("span", class_="wikibase-snakview-variation-novaluesnak")
                    if novalue:
                        return StatementSpecialValue("novalue")
                    missing_value = a.find("span", class_="wb-entity-undefinedinfo")
                    if missing_value:
                        return StatementSpecialValue("missing")
                    date_block = a.find(class_="wb-time-details")
                    if date_block and type(date_block) == Tag:
                        return StatementTimeValue.from_block(date_block)
                    if a.find(class_="wb-quantity-details"):
                        return StatementQuantityValue.from_block(a)
        
        if not wrapped:
            # try again but wrapped in a span
            wrapped_tag = BeautifulSoup(f"<span>{a}</span>", "html.parser").span
            if wrapped_tag:
                return StatementValue.extract_value(wrapped_tag, True)
        
        raise Exception(f"Not implemented yet for value: {a}")


@dataclass
class StatementType:
    pass

@dataclass
class Alias(StatementType):
    lang: str

@dataclass
class Description(StatementType):
    lang: str

@dataclass
class Label(StatementType):
    lang: str

@dataclass
class RegularStatement(StatementType):
    pid: str

@dataclass
class RankChangeStatement(StatementType):
    pid: str

@dataclass
class SitelinkChangeStatement(StatementType):
    lang: str

@dataclass
class QualifierChangeStatement(StatementType):
    pid: str
    value: StatementValue

@dataclass
class ReferenceChangeStatement(StatementType):
    pid: str
    value: StatementValue

@dataclass
class StatementStringValue(StatementValue):
    value: str

@dataclass 
class StatementMonolingualTextValue(StatementValue):
    value: str
    lang: str

@dataclass
class StatementTimeValue(StatementValue):
    value: str

    @staticmethod
    def from_block(block: Tag) -> Self:
        next_element = block.next_element
        if next_element:
            date_string = next_element.text
            # get calendar name
            calendar_name = block.find(class_="wb-calendar-name")
            if calendar_name:
                date_string += " " + calendar_name.text
            return StatementTimeValue(date_string)
        raise Exception("Unkown date format")
    
@dataclass
class StatementExternalLinkValue(StatementValue):
    href: str
    text: str

@dataclass
class StatementInternalLinkValue(StatementValue):
    href: str
    text: str
    lang: str

@dataclass
class StatementFileLink(StatementValue):
    href: str
    text: str

@dataclass
class StatementSpecialValue(StatementValue):
    value: str

@dataclass
class StatementItemValue(StatementValue):
    value: str

@dataclass
class StatementQuantityValue(StatementValue):
    rendered_value: str

    @staticmethod
    def from_block(block: Tag) -> Self:
        quantity_rendered = block.find(class_="wb-quantity-rendered")
        if quantity_rendered:
            return StatementQuantityValue(quantity_rendered.text)
        raise Exception("Unkown quantity format")

@dataclass
class StatementNumberValue(StatementValue):
    value: int | float

@dataclass
class StatementRankValue(StatementValue):
    value: str

    @classmethod
    def from_string(cls, s: str) -> Self:
        if s == "Normal rank":
            return "normal"
        elif s == "Deprecated rank":
            return "deprecated"
        elif s == "Preferred rank":
            return "preferred"
        else:
            raise Exception("Unknown rank: " + s)

@dataclass
class StatementQualifierValue(StatementValue):
    pid: str
    value: StatementValue

    @classmethod
    def from_html(cls, tag: Tag) -> Self:
        links = tag.find_all("a")
        pid = StatementValue.extract_pid(links[0])
        if len(links) > 1:
            value = StatementValue.extract_qid(links[1])
            return StatementQualifierValue(pid, StatementItemValue(value))
        else:
            # likely unknown or no value
            # find span with class = "wikibase-snakview-variation-somevaluesnak"
            span = tag.find("span", class_="wikibase-snakview-variation-somevaluesnak")
            if span:
                somevalue = StatementSpecialValue("somevalue")
                return StatementQualifierValue(pid, somevalue)
            span = tag.find("span", class_="wikibase-snakview-variation-novaluesnak")
            if span:
                novalue = StatementSpecialValue("novalue")
                return StatementQualifierValue(pid, novalue)
            raise Exception("Unknown qualifier value")
        
@dataclass
class Statement:
    field: RegularStatement
    value: StatementValue

    @classmethod
    def from_span(cls, span: Tag) -> Self:
        """
        Parses a statement from a span tag with a colon delimited prop/value pair
        """
        # get first link in span
        link = span.find("a")
        if link and type(link) == Tag:
            pid = StatementValue.extract_pid(link)
            field = RegularStatement(pid)
        else:
            raise Exception("Expected a link in the span")

        if link.next_sibling:
            if link.next_sibling.text.strip() == ":":
                # look at the 2nd value after the link because there's a separating colon
                value = StatementValue.extract_value(list(link.next_siblings)[1])
            else:
                # ok it's just a string (maybe)
                # oh god end this
                value = StatementStringValue("/".join(link.next_sibling.text.strip()[1:].split("/")[0:-1]).strip())
        else:
            raise Exception("no second value in statement span")
        return Statement(field, value)

@dataclass
class ReferenceValue(StatementValue):
    statements: List[Statement]

    @classmethod
    def from_div(cls, div: Tag) -> Self:
        statements = []
        inner_div = div.find("ins", class_="diffchange-inline") or div.find("del", class_="diffchange-inline")
        if not inner_div or type(inner_div) != Tag:
            raise Exception("reference block missing references")
        else:
            for span in inner_div.find_all("span", recursive=False):
                statements.append(Statement.from_span(span))
        return ReferenceValue(statements)

@dataclass
class Change:
    field: StatementType
    old: Optional[StatementValue]
    new: Optional[StatementValue]

    @classmethod
    def from_html(cls, field: Tag, old: Optional[Tag], new: Optional[Tag]) -> Self:
        statement_type = Change.parse_field(field)

        match statement_type:
            case Alias(lang) | Description(lang) | Label(lang):
                old_value = StatementStringValue(old.text) if old else None
                new_value = StatementStringValue(new.text) if new else None
                return Change(statement_type, old_value, new_value)
            case RegularStatement(pid):
                old_value = StatementValue.extract_value(old) if old else None
                new_value = StatementValue.extract_value(new) if new else None
                return Change(statement_type, old_value, new_value)

            case RankChangeStatement(pid):
                old_value = StatementRankValue.from_string(old.text) if old else None
                new_value = StatementRankValue.from_string(new.text) if new else None
                return Change(statement_type, old_value, new_value)
            
            case QualifierChangeStatement(pid):
                old_value = StatementQualifierValue.from_html(old) if old else None
                new_value = StatementQualifierValue.from_html(new) if new else None
                return Change(statement_type, old_value, new_value)
            
            case ReferenceChangeStatement(pid, qid):
                old_value = ReferenceValue.from_div(old) if old else None
                new_value = ReferenceValue.from_div(new) if new else None
                return Change(statement_type, old_value, new_value)
            
            case SitelinkChangeStatement(lang):
                old_value = StatementValue.extract_value(old) if old else None
                new_value = StatementValue.extract_value(new) if new else None

                return Change(statement_type, old_value, new_value)
            case None:
                raise Exception("unk statement type")
                pass

        return Change(statement_type, None, None)

    @staticmethod
    def parse_field(field: Tag) -> StatementType:
        if field.text.startswith("aliases"):
            _, lang, _ = field.text.split("/")
            return Alias(lang.strip())
        elif field.text.startswith("description"):
            _, lang = field.text.split("/")
            return Description(lang.strip())
        elif field.text.startswith("label"):
            _, lang = field.text.split("/")
            return Label(lang.strip())
        elif field.text.startswith("Property") and field.text.endswith("rank"):
            link = field.find("a")
            if type(link) == Tag:
                # get the title
                title = link.attrs["title"]
                pid = title.split(":")[-1]
                return RankChangeStatement(pid)
        elif field.text.startswith("Property") and field.text.endswith("qualifier"):
            statement = Statement.from_span(field)
            return QualifierChangeStatement(statement.field.pid, statement.value)  
        elif field.text.startswith("Property") and field.text.endswith("reference"):
            links = field.find_all("a")
            span = field.find("span")
            details = field.find(class_="wb-details")
            if type(links[0]) == Tag:
                pid = StatementValue.extract_pid(links[0])
                if len(links) == 2:
                    # ok we have two links so the second one is the qid or an external link
                    value = StatementValue.extract_value(links[1])
                elif details and type(details) == Tag:
                    value = StatementValue.extract_value(details)
                elif span and type(span) == Tag:
                    value = StatementValue.extract_value(span)
                else:
                    # ok we have a value in the text so we need to strip the colon
                    data_child = list(field.children)[2]
                    value = StatementValue.extract_value(data_child)
                return ReferenceChangeStatement(pid, value)
            else:
                raise Exception("Expected a tag for the main pid")
        elif field.text.startswith("Property"):
            link = field.find("a")
            if type(link) == Tag:
                # get the title
                title = link.attrs["title"]
                pid = title.split(":")[-1]
                return RegularStatement(pid)
        elif field.text.startswith("links"):
            args = field.text.split("/")
            lang = args[1].strip()
            if len(args) == 4 and args[2].strip() == "badges":
                return SitelinkChangeStatement(lang)
            if len(args) == 3 and args[2].strip() == "name":
                return SitelinkChangeStatement(lang)
        # unknown field type
        raise Exception("Unknown field type: " + field.text)

@dataclass
class Diff:
    user: str
    title: str
    changes: List[Change]
    comments: List[str]
    tags: List[List[str]]

class DiffStateMachine:
    def __init__(self) -> None:
        # the kind of field we are dealing with
        self._cur_field: Optional[Tag] = None
        # the old value of the field
        self._cur_old: Optional[Tag] = None
        # the new value of the field
        self._cur_new: Optional[Tag] = None
        self.changes: List[Change] = []


    def process_row(self, row: Tag, col1: Optional[Any], col2: Optional[Any], col3: Optional[Any], col4: Optional[Any]) -> Optional[Change]:
        # yeah these col columns aren't used anymore really and we could replace it all with the row now that we know about the classnames
        emit = False

        if self._cur_field == None:
            self._cur_field = col1 or col3
            self._cur_new = None
            self._cur_old = None
        else:
            cur_old = row.findChild("td", {"class": "diff-deletedline"})
            if type(cur_old) == Tag:
                self._cur_old = cur_old
            cur_new = row.findChild("td", {"class": "diff-addedline"})
            if type(cur_new) == Tag:
                self._cur_new= cur_new

            emit = True

        if emit:
            assert(self._cur_field != None)
            cur_old_str = self._cur_old.text if self._cur_old else None
            cur_new_start = self._cur_new.text if self._cur_new else None
            change = Change.from_html(self._cur_field, self._cur_old, self._cur_new)
            self._cur_field = None
            self._cur_old = None
            self._cur_new = None
            self.changes.append(change)


class ItemDiffer:
    def __init__(self, diff_json: dict):
        compare: Optional[dict] = diff_json['compare']
        if not compare:
            raise Exception("Invalid ItemDiff. Missing `compare`")
        
        self.fromrevid = compare['fromrevid']
        self.torevid = compare['torevid']

        if self.fromrevid >= self.torevid:
            raise Exception("Invalid ItemDiff. fromrevid >= torevid")

        fromns = compare['fromns']
        tons = compare['tons']
        fromid = compare['fromid']
        toid = compare['toid']
        fromtitle = compare['fromtitle']
        totitle = compare['totitle']    
        if fromns != tons or fromid != toid or fromtitle != totitle:
            raise Exception("Invalid ItemDiff. Not same item.")
        touser = compare['touser']
        self.title: str = fromtitle
        self.user: str = touser
        self._diff: str = compare['*']
        self._revisions = get_revisions(self.title, self.torevid, self.fromrevid)

    def get_url(self) -> str:
        return f"https://www.wikidata.org/w/index.php?title=XXX&diff={self.torevid}&oldid={self.fromrevid}"

    def changes(self) -> Diff:
        comments = [r.comment for r in self._revisions]
        tags = [r.tags for r in self._revisions]
        soup = BeautifulSoup(self._diff, "html.parser")
        rows = soup.findChildren("tr", recursive=False)
        cur_field: Optional[str] = None
        sm = DiffStateMachine()
        for r in rows:
            # extract tds from tr
            tds = r.findChildren("td", recursive=False)
            if len(tds) == 2:
                # two columns
                previous, result = tds
                previous_text_present = previous.get_text().strip() != ""
                result_text_present = result.get_text().strip() != ""
                if previous_text_present and result_text_present:
                    sm.process_row(r, previous, None, result, None)
                elif previous_text_present:
                    sm.process_row(r, previous, None, None, None)
                elif result_text_present:
                    sm.process_row(r, None, None, result, None)
                else:
                    # unexpected result
                    raise Exception("Invalid diff row. Two columns, but both empty")

            elif len(tds) == 3:
                # three column
                previous, mid, result = tds
                previous_text = previous.get_text()
                mid_text = mid.get_text()
                result_text = result.get_text()

                # get colspan from previous
                previous_colspan = previous.get('colspan')
                mid_colspan = mid.get('colspan')
                result_colspan = result.get('colspan')

                if previous_colspan == '2' and previous_text.strip() == "":
                    # no previous exists
                    sm.process_row(r, None, None, mid, result)
                elif result_colspan == '2' and result_text.strip() == "":
                    # no previous exists
                    sm.process_row(r, previous, mid, None, None)
                else:
                    # unexpected result
                    raise Exception("Invalid diff row. Three columns, but not colspan.")
            elif len(tds) == 4:
                # four column
                previous, mid1, mid2, result = tds
                previous_text = previous.get_text()
                mid1_text = mid1.get_text()
                mid2_text = mid2.get_text()
                result_text = result.get_text()
                sm.process_row(r, previous, mid1, mid2, result)
            else:
                # error condition
                raise Exception("Invalid diff row. Not 2 or 3 columns.")


        return Diff(self.user, self.title, sm.changes, comments, tags)



def get_diff(from_rev_id: int, to_rev_id: int) -> ItemDiffer:
    URL = f"https://www.wikidata.org/w/api.php?action=compare&prop=user|diff|title|rel|ids&format=json&fromrev={from_rev_id}&torev={to_rev_id}"
    resp = requests.get(URL)
    return ItemDiffer(resp.json())

if __name__ == "__main__":
    res = get_diff(1916986831, 1916992133)
    print(res.changes())