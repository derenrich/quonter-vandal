from quonter_vandal.diff import *


def test_alias_add_diff():
    revid = 1942074309
    oldid = 1942074306
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "BrokenSegue"
    assert diff.comments == [
        "/* wbsetaliases-add:1|en */ legal challenge to Executive Order 13769"]
    assert len(diff.changes) == 1

    alias_change = diff.changes[0]
    assert (alias_change.field == Alias("en"))
    assert (alias_change.old == None)
    assert (type(alias_change.new) is StatementStringValue)
    assert (alias_change.new.value ==
            "legal challenge to Executive Order 13769")


def test_description_add_diff():
    revid = 1942048859
    oldid = 1938660715
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "BrokenSegue"
    assert diff.comments == [
        "/* wbsetdescription-add:1|en */ U.S. government-led effort to fight antisemitism, import w/ [[Wikidata:Wwwyzzerdd|🧙 Wwwyzzerdd for Wikidata]]"]
    assert len(diff.changes) == 1
    assert diff.tags == [["wwwyzzerdd"]]

    description_change = diff.changes[0]
    assert (description_change.field == Description("en"))
    assert (description_change.old == None)
    assert (type(description_change.new) is StatementStringValue)
    assert (description_change.new.value ==
            "U.S. government-led effort to fight antisemitism")


def test_label_change_diff():
    revid = 1942074306
    oldid = 1419596909
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "BrokenSegue"
    assert diff.comments == [
        "/* wbsetlabel-set:1|en */ legal challenges to the Trump travel ban"]
    assert len(diff.changes) == 1
    label_change = diff.changes[0]
    assert (label_change.field == Label("en"))
    assert (type(label_change.old) is StatementStringValue)
    assert (type(label_change.new) is StatementStringValue)
    assert (label_change.old.value ==
            "legal challenge to Executive Order 13769")
    assert (label_change.new.value ==
            "legal challenges to the Trump travel ban")


def test_label_and_alias_diff():
    revid = 1942074309
    oldid = 1419596909
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "BrokenSegue"
    print(diff.comments)
    assert diff.comments == ["/* wbsetaliases-add:1|en */ legal challenge to Executive Order 13769",
                             "/* wbsetlabel-set:1|en */ legal challenges to the Trump travel ban"]
    assert len(diff.changes) == 2
    label_change = diff.changes[0]
    assert (label_change.field == Label("en"))
    assert (type(label_change.old) is StatementStringValue)
    assert (type(label_change.new) is StatementStringValue)
    assert (label_change.old.value ==
            "legal challenge to Executive Order 13769")
    assert (label_change.new.value ==
            "legal challenges to the Trump travel ban")
    alias_change = diff.changes[1]
    assert (alias_change.field == Alias("en"))
    assert (alias_change.old == None)
    assert (type(alias_change.new) is StatementStringValue)
    assert (alias_change.new.value ==
            "legal challenge to Executive Order 13769")
    assert (alias_change.old == None)


def test_add_qualifier_and_rank_diff():
    # https://www.wikidata.org/w/index.php?title=XXX&diff=1942162509&oldid=1934969781
    revid = 1942162509
    oldid = 1934969781
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "BorkedBot"
    # comments needs to be fixed
    assert diff.comments == ['/* wbsetqualifier-add:1| */ [[Property:P7452]]: [[Q71536040]]',
                             '/* wbsetclaim-update:2||1 */ [[Property:P569]]: 21 January 1956']
    assert len(diff.changes) == 2
    rank_change = diff.changes[0]
    assert (rank_change.field == RankChangeStatement("P569"))
    assert (rank_change.old == "normal")
    assert (rank_change.new == "preferred")
    qualifier_change = diff.changes[1]
    assert (qualifier_change.field ==
            QualifierChangeStatement("P569", StatementStringValue("21 January 1956")))
    assert (qualifier_change.old == None)
    assert (qualifier_change.new == StatementQualifierValue(
        pid='P7452', value=StatementItemValue(value='Q71536040')))


def test_wwwyzzerdd_diff():
    # https://www.wikidata.org/w/index.php?title=XXX&diff=1942024562&oldid=1851566554
    revid = 1942024562
    oldid = 1851566554
    diff = get_diff(oldid, revid).changes()
    print(get_diff(oldid, revid).get_url())
    assert diff.user == "BrokenSegue"
    assert len(diff.changes) == 9
    add_movement = diff.changes[0]
    assert (add_movement.field == RegularStatement(pid='P135'))
    assert (add_movement.old == None)
    assert (add_movement.new == StatementItemValue(value='Q30325066'))

    add_movement_rank = diff.changes[1]
    assert (add_movement_rank.field == RankChangeStatement(pid='P135'))
    assert (add_movement_rank.old == None)
    assert (add_movement_rank.new == "normal")

    add_movement_reference = diff.changes[2]
    assert (add_movement_reference.field ==
            ReferenceChangeStatement(pid='P135', qid="Q30325066"))
    assert add_movement_reference.old is None
    assert type(add_movement_reference.new) is ReferenceValue
    assert add_movement_reference.new == ReferenceValue([
        Statement(RegularStatement('P143'), StatementItemValue(value='Q328')),
        Statement(RegularStatement('P813'),
                  StatementTimeValue("28 July 2023")),
        Statement(RegularStatement('P4656'), StatementExternalLinkValue(
            "https://en.wikipedia.org/w/index.php?title=Lucian_Wintrich&oldid=1163978108",
            "https://en.wikipedia.org/w/index.php?title=Lucian_Wintrich&oldid=1163978108"))
    ])

    add_employer = diff.changes[3]
    assert (add_employer.field == RegularStatement(pid='P108'))
    assert (add_employer.old == None)
    assert (add_employer.new == StatementItemValue(value='Q30589935'))

    add_employer_rank = diff.changes[4]
    assert (add_employer_rank.field == RankChangeStatement(pid='P108'))
    assert (add_employer_rank.old == None)
    assert (add_employer_rank.new == "normal")

    add_employer_reference = diff.changes[5]
    assert (add_employer_reference.field ==
            ReferenceChangeStatement(pid='P108', qid="Q30589935"))
    assert add_employer_reference.old is None
    assert type(add_employer_reference.new) is ReferenceValue
    assert add_employer_reference.new == ReferenceValue([
        Statement(RegularStatement('P143'), StatementItemValue(value='Q328')),
        Statement(RegularStatement('P813'),
                  StatementTimeValue("28 July 2023")),
        Statement(RegularStatement('P4656'), StatementExternalLinkValue(
            "https://en.wikipedia.org/w/index.php?title=Lucian_Wintrich&oldid=1163978108#cite_note-:11-3",
            "https://en.wikipedia.org/w/index.php?title=Lucian_Wintrich&oldid=1163978108#cite_note-:11-3"))
    ])

    add_orientation = diff.changes[6]
    assert (add_orientation.field == RegularStatement(pid='P91'))
    assert (add_orientation.old == None)
    assert (add_orientation.new == StatementItemValue(value='Q6636'))

    add_orientation_rank = diff.changes[7]
    assert (add_orientation_rank.field == RankChangeStatement(pid='P91'))
    assert (add_orientation_rank.old == None)
    assert (add_orientation_rank.new == "normal")

    add_orientation_reference = diff.changes[8]
    assert add_orientation_reference.old is None
    assert add_orientation_reference.new == ReferenceValue([
        Statement(RegularStatement('P854'), StatementExternalLinkValue(
            href="https://www.dailydot.com/irl/conservative-queers-lgbtq-trump/",
            text="https://www.dailydot.com/irl/conservative-queers-lgbtq-trump/")),
        Statement(RegularStatement('P813'),
                  StatementTimeValue("28 July 2023"))
    ])


def test_fennel():
    # https://www.wikidata.org/w/index.php?title=Q121167625&diff=1946482672&oldid=1946481281
    revid = 1946482672
    oldid = 1946481281
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "BrokenSegue"
    assert len(diff.changes) == 12

    add_business = diff.changes[0]
    assert (add_business.field == RegularStatement(pid='P31'))
    assert (add_business.old == None)
    assert (add_business.new == StatementItemValue(value='Q4830453'))

    add_business_rank = diff.changes[1]
    assert (add_business_rank.field == RankChangeStatement(pid='P31'))
    assert (add_business_rank.old == None)
    assert (add_business_rank.new == "normal")

    add_crunchbase = diff.changes[2]
    assert (add_crunchbase.field == RegularStatement(pid='P2088'))
    assert (add_crunchbase.old == None)
    assert (add_crunchbase.new == StatementExternalLinkValue(
        "https://www.crunchbase.com/organization/fennel-ai", "fennel-ai"))


def test_unk_qual():
    # https://www.wikidata.org/w/index.php?title=Q4115189&diff=1952202478&oldid=1952154007
    revid = 1952202478
    oldid = 1952154007
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "BrokenSegue"
    assert len(diff.changes) == 1
    add_unk_qual = diff.changes[0]
    assert (add_unk_qual.field == QualifierChangeStatement(
        'P460', StatementItemValue(value='Q13406268')))
    assert (add_unk_qual.old == None)
    assert (add_unk_qual.new == StatementQualifierValue(
        "P1013", StatementSpecialValue("somevalue")))


def test_unk_value():
    # https://www.wikidata.org/w/index.php?title=Q4115189&diff=1952251903&oldid=1952205143
    revid = 1952251903
    oldid = 1952205143
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "BrokenSegue"
    assert len(diff.changes) == 1
    add_unk_value = diff.changes[0]
    assert (add_unk_value.field == RegularStatement(pid='5021'))
    assert (add_unk_value.old == None)
    assert (add_unk_value.new == StatementSpecialValue("somevalue"))
