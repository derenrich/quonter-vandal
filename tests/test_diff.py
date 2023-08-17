import json
import time
import gzip
from quonter_vandal.diff import *
from pytest_asyncio.plugin import *
import pytest


@pytest.mark.vcr()
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


@pytest.mark.vcr()
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


@pytest.mark.vcr()
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


@pytest.mark.vcr()
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


@pytest.mark.vcr()
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


@pytest.mark.vcr()
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
            ReferenceChangeStatement('P135', StatementItemValue("Q30325066")))
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
            ReferenceChangeStatement('P108', StatementItemValue("Q30589935")))
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


@pytest.mark.vcr()
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


@pytest.mark.vcr()
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


@pytest.mark.vcr()
def test_unk_value():
    # https://www.wikidata.org/w/index.php?title=Q4115189&diff=1952251903&oldid=1952205143
    revid = 1952251903
    oldid = 1952205143
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "BrokenSegue"
    assert len(diff.changes) == 2
    add_unk_value = diff.changes[0]
    assert (add_unk_value.field == RegularStatement(pid='P5021'))
    assert (add_unk_value.old == None)
    assert (add_unk_value.new == StatementSpecialValue("somevalue"))

    add_unk_rank = diff.changes[1]
    assert (add_unk_rank.field == RankChangeStatement(pid='P5021'))
    assert (add_unk_rank.old == None)
    assert (add_unk_rank.new == "normal")


@pytest.mark.vcr()
def test_no_value():
    # https://www.wikidata.org/w/index.php?title=Q4115189&diff=1952663526&oldid=1952481644
    revid = 1952663526
    oldid = 1952481644
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "BrokenSegue"
    assert len(diff.changes) == 2
    add_no_value = diff.changes[0]
    assert (add_no_value.field == RegularStatement(pid='P5021'))
    assert (add_no_value.old == StatementSpecialValue("somevalue"))
    assert (add_no_value.new == StatementSpecialValue("novalue"))

    add_unk_rank = diff.changes[1]
    assert (add_unk_rank.field == RankChangeStatement(pid='P5021'))
    assert (add_unk_rank.old == "normal")
    assert (add_unk_rank.new == "deprecated")


@pytest.mark.vcr()
def test_badges_change():
    # https://www.wikidata.org/w/index.php?title=Q4115189&diff=1952667555&oldid=1952667492
    revid = 1952667555
    oldid = 1952667492
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "BrokenSegue"
    assert len(diff.changes) == 4
    add_no_proof_badge = diff.changes[0]
    assert (add_no_proof_badge.field == SitelinkChangeStatement(lang='dewiki'))
    assert (add_no_proof_badge.old == None)
    assert (add_no_proof_badge.new == StatementItemValue("Q20748091"))

    add_problematic_badge = diff.changes[1]
    assert (add_problematic_badge.field ==
            SitelinkChangeStatement(lang='dewiki'))
    assert (add_problematic_badge.old == None)
    assert (add_problematic_badge.new == StatementItemValue("Q20748094"))

    rm_featured_list_badge = diff.changes[2]
    print(rm_featured_list_badge)
    assert (rm_featured_list_badge.field ==
            SitelinkChangeStatement(lang='dewiki'))
    assert (rm_featured_list_badge.old == StatementItemValue("Q17506997"))
    assert (rm_featured_list_badge.new == None)

    rm_featured_portal_badge = diff.changes[3]
    assert (rm_featured_portal_badge.field ==
            SitelinkChangeStatement(lang='dewiki'))
    assert (rm_featured_portal_badge.old == StatementItemValue("Q17580674"))
    assert (rm_featured_portal_badge.new == None)


@pytest.mark.vcr()
def test_sitelink_change():
    # https://www.wikidata.org/w/index.php?title=Q110970851&curid=105981221&diff=1952555904&oldid=1866394894
    revid = 1952555904
    oldid = 1866394894
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "Laziz Baxtiyorov"
    assert len(diff.changes) == 1
    add_sitelink = diff.changes[0]
    assert (add_sitelink.field == SitelinkChangeStatement(lang='tkwiki'))
    assert (add_sitelink.old == None)
    assert (add_sitelink.new == StatementInternalLinkValue(
        "https://tk.wikipedia.org/wiki/Buharany%C5%88_gabawy", "Buharanyň gabawy", 'tk'))


@pytest.mark.vcr()
def test_external_reference_change():
    # https://www.wikidata.org/w/index.php?title=Q110970851&curid=105981221&diff=1800955256&oldid=1711288204
    revid = 1800955256
    oldid = 1711288204
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "146.196.34.28"
    assert len(diff.changes) == 3
    change_infocard = diff.changes[0]
    assert (change_infocard.field == RegularStatement('P2566'))
    assert (change_infocard.old == StatementExternalLinkValue(
        "https://echa.europa.eu/substance-information/-/substanceinfo/100.009.176", "100.009.176"))
    assert (change_infocard.new == StatementExternalLinkValue(
        "https://echa.europa.eu/substance-information/-/substanceinfo/27.902005", "27.902005"))

    change_infocard_ref = diff.changes[1]
    assert (change_infocard_ref.field == ReferenceChangeStatement('P2566', StatementExternalLinkValue(
        "https://echa.europa.eu/substance-information/-/substanceinfo/27.902005", "27.902005")))
    assert (change_infocard_ref.old == None)
    assert (change_infocard_ref.new == ReferenceValue(
        [
            Statement(
                field=RegularStatement('P248'),
                value=StatementItemValue('Q59911453')
            ),
            Statement(field=RegularStatement(pid='P2566'),
                      value=StatementExternalLinkValue(href='https://echa.europa.eu/substance-information/-/substanceinfo/27.902005',
                                                       text='27.902005')),
            Statement(field=RegularStatement(pid='P813'),
                      value=StatementTimeValue(value='27 December 2018')),
            Statement(field=RegularStatement(pid='P1476'),
                      value=StatementMonolingualTextValue(value='2,4-dinitro-1-naphthol',
                                                          lang='en')),
            Statement(field=RegularStatement(pid='P1683'),
                      value=StatementMonolingualTextValue(value='CAS no.: 605-69-6',
                                                          lang='en')),
        ]
    ))
    change_infocard_ref = diff.changes[2]
    print(change_infocard_ref.field)
    assert (change_infocard_ref.field == ReferenceChangeStatement('P2566', StatementExternalLinkValue(
        "https://echa.europa.eu/substance-information/-/substanceinfo/100.009.176", "100.009.176")))
    assert (change_infocard_ref.old == ReferenceValue([
        Statement(field=RegularStatement(pid='P248'),
                  value=StatementItemValue(value='Q59911453')),
        Statement(field=RegularStatement(pid='P2566'),
                  value=StatementExternalLinkValue(href='https://echa.europa.eu/substance-information/-/substanceinfo/100.009.176',
                                                   text='100.009.176')),
        Statement(field=RegularStatement(pid='P813'),
            value=StatementTimeValue(value='27 December 2018')),
        Statement(field=RegularStatement(pid='P1476'),
            value=StatementMonolingualTextValue(value='2,4-dinitro-1-naphthol',
                                                lang='en')),
        Statement(field=RegularStatement(pid='P1683'),
                  value=StatementMonolingualTextValue(value='CAS no.: 605-69-6',
                                                      lang='en')),
    ]))
    assert (change_infocard_ref.new == None)


@pytest.mark.vcr()
def test_date_ref_on_no_value_statement():
    # https://www.wikidata.org/w/index.php?title=Q4115189&diff=1952763643&oldid=1952667555
    revid = 1952763643
    oldid = 1952667555
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "BrokenSegue"
    assert len(diff.changes) == 1
    change_assesment_ref = diff.changes[0]
    assert change_assesment_ref.field == ReferenceChangeStatement(
        'P5021', StatementSpecialValue("novalue"))
    assert change_assesment_ref.old == None
    assert change_assesment_ref.new == ReferenceValue([
        Statement(field=RegularStatement(pid='P813'),
                  value=StatementTimeValue(value='13 August 2023'))])


@pytest.mark.vcr()
def test_georgian_date():
    # https://www.wikidata.org/w/index.php?title=Q114233325&diff=1801067965&oldid=1766849620
    revid = 1801067965
    oldid = 1766849620
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "74.12.222.39"
    assert len(diff.changes) == 1
    change_georgian_date = diff.changes[0]
    assert change_georgian_date.field == RegularStatement('P569')
    assert change_georgian_date.old == StatementTimeValue("29 August 188")
    assert change_georgian_date.new == StatementTimeValue(
        "29 August 1888 Gregorian")


@pytest.mark.vcr()
def test_quantity_statement():
    # https://www.wikidata.org/w/index.php?title=Q114233325&diff=1856453216&oldid=1774447242
    revid = 1856453216
    oldid = 1774447242
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "176.12.82.139"
    assert len(diff.changes) == 5

    death_date_change = diff.changes[0]
    assert death_date_change.field == RegularStatement('P570')
    assert death_date_change.old == StatementTimeValue("1646")
    assert death_date_change.new == StatementTimeValue("2050")

    quantity_change = diff.changes[4]
    assert quantity_change.field == RegularStatement('P1971')
    assert quantity_change.old == StatementQuantityValue("4")
    assert quantity_change.new == StatementQuantityValue("13")


@pytest.mark.vcr()
def test_string_change():
    # https://www.wikidata.org/w/index.php?title=1874928741&diff=1874928741&oldid=1846303619
    revid = 1874928741
    oldid = 1846303619
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "186.67.40.154"
    assert len(diff.changes) == 8

    pseudonym_change = diff.changes[3]
    assert pseudonym_change.field == RegularStatement('P742')
    assert pseudonym_change.old == StatementStringValue("Américo")
    assert pseudonym_change.new == StatementStringValue("Pancho")

    birhtname_change = diff.changes[4]
    assert birhtname_change.field == RegularStatement('P1477')
    assert birhtname_change.old == StatementMonolingualTextValue(
        "Domingo Johnny Vega Urzúa", "es")
    assert birhtname_change.new == StatementMonolingualTextValue(
        "Francisco Vera", "es")


@pytest.mark.vcr()
def test_date_qualifier_change():
    # https://www.wikidata.org/w/index.php?title=1874928741&diff=1921063976&oldid=1913859487
    revid = 1921063976
    oldid = 1913859487
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "190.202.238.19"
    assert len(diff.changes) == 6

    image_date_qualifier_rm = diff.changes[2]
    assert image_date_qualifier_rm.field == QualifierChangeStatement('P18', StatementFileLink(
        "//commons.wikimedia.org/wiki/File:Letizia_von_Spanien_(2022).jpg", "Letizia von Spanien (2022).jpg"))
    assert image_date_qualifier_rm.new == None
    assert image_date_qualifier_rm.old == StatementQualifierValue(
        "P585", StatementTimeValue("2022"))

    image_qualifier_rm = diff.changes[3]
    assert image_qualifier_rm.field == QualifierChangeStatement('P18', StatementFileLink(
        "//commons.wikimedia.org/wiki/File:Letizia_von_Spanien_(2022).jpg", "Letizia von Spanien (2022).jpg"))
    assert image_qualifier_rm.new == None
    assert image_qualifier_rm.old == StatementQualifierValue(
        "P2096", StatementMonolingualTextValue("Letícia Ortiz", "ca"))


@pytest.mark.vcr()
def test_reference_on_date():
    # https://www.wikidata.org/w/index.php?title=Q4115189&diff=1813636413&oldid=1807348139
    revid = 1813636413
    oldid = 1807348139
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "2A02:587:CC90:282A:6DFC:4569:8C9C:1C61"
    assert len(diff.changes) == 3

    assert diff.changes[2].field == ReferenceChangeStatement(
        'P4602', StatementStringValue("7 January 2023"))
    assert diff.changes[2].new == None
    assert diff.changes[2].old == ReferenceValue([
        Statement(field=RegularStatement(pid='P854'),
                  value=StatementExternalLinkValue("https://www.iefimerida.gr/ellada/kideia-noti-mayroydi-poioi-pigan-eikones", "https://www.iefimerida.gr/ellada/kideia-noti-mayroydi-poioi-pigan-eikones")),
        Statement(field=RegularStatement(pid='P813'),
                  value=StatementTimeValue("9 January 2023")),
    ])


@pytest.mark.vcr()
def test_amount_with_units():
    # https://www.wikidata.org/w/index.php?title=Q4115189&diff=1897073502&oldid=1788346432
    revid = 1897073502
    oldid = 1788346432
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "80.11.85.7"
    assert len(diff.changes) == 1

    assert diff.changes[0].field == RegularStatement('P2130')
    assert diff.changes[0].new == StatementQuantityValue("10 euro")
    assert diff.changes[0].old == StatementQuantityValue("18 bee")


@pytest.mark.vcr()
def test_property_ends_in_rank():
    # https://www.wikidata.org/w/index.php?title=Q1515445&diff=1803826490&oldid=1703741037
    revid = 1803826490
    oldid = 1703741037
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "93.176.133.171"
    assert len(diff.changes) == 4


@pytest.mark.vcr()
def test_coord_change():
    # https://www.wikidata.org/w/index.php?title=Q114233325&diff=1808526599&oldid=1803785463
    revid = 1808526599
    oldid = 1803785463
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "195.221.59.157"
    assert len(diff.changes) == 1
    coord_change = diff.changes[0]
    assert coord_change.field == RegularStatement('P625')
    assert coord_change.old == StatementGlobeCoordinateValue(
        "47° 16' 48\", -1° 52' 48\"")
    assert coord_change.new == StatementGlobeCoordinateValue(
        "47° 0' 48\", -6° 52' 48\"")


@pytest.mark.vcr()
def test_redirect_change():
    # https://www.wikidata.org/w/index.php?title=1814194280&diff=1814194280&oldid=1714064841
    revid = 1814194280
    oldid = 1714064841
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "109.161.200.40"
    assert len(diff.changes) == 1
    redirect_change = diff.changes[0]
    assert redirect_change.field == Redirect()
    assert redirect_change.old == StatementStringValue("Q38200141")
    assert redirect_change.new == None


@pytest.mark.vcr()
def test_no_such_diff():
    # https://www.wikidata.org/w/index.php?title=1814194280&diff=1838236382&oldid=1747008787
    revid = 1838236382
    oldid = 1747008787
    diff = get_diff(oldid, revid)
    assert diff == None


@pytest.mark.vcr()
def test_metre_diff():
    # https://www.wikidata.org/w/index.php?title=1814194280&diff=1846325831&oldid=1794231076
    revid = 1846325831
    oldid = 1794231076
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "109.20.19.85"
    assert len(diff.changes) == 7

    assert diff.changes[0].field == Alias('fr')
    assert diff.changes[0].old == None
    assert diff.changes[0].new == StatementStringValue("Vienois")

    assert diff.changes[3].field == ReferenceChangeStatement(
        'P2048', StatementStringValue("1.76 metre"))
    assert diff.changes[3].old == ReferenceValue(statements=[Statement(RegularStatement('P854'),
                                                                       StatementExternalLinkValue('https://bodysize.org/fr/vianney/', 'https://bodysize.org/fr/vianney/'))])
    assert diff.changes[3].new == None

    assert diff.changes[4].field == RegularStatement('P2067')
    assert diff.changes[4].old == StatementQuantityValue("75 kilogram")
    assert diff.changes[4].new == None


@pytest.mark.vcr()
def test_ext_id_without_link():
    # https://www.wikidata.org/w/index.php?title=Q67011165&diff=1853463165&oldid=1844960481
    revid = 1853463165
    oldid = 1844960481
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "82.210.51.60"
    assert len(diff.changes) == 3

    assert diff.changes[0].field == RegularStatement('P27')
    assert diff.changes[0].old == StatementItemValue("Q142")
    assert diff.changes[0].new == StatementItemValue("Q880")

    assert diff.changes[2].field == QualifierChangeStatement(
        'P106', StatementItemValue("Q937857"))
    assert diff.changes[2].old == None
    assert diff.changes[2].new == StatementQualifierValue(
        "P8601", StatementExternalLinkValue(None, "madrid"))


@pytest.mark.vcr()
def test_lexeme_usage():
    # https://www.wikidata.org/w/index.php?title=Q4115189&diff=1953415294&oldid=1952843189
    revid = 1953415294
    oldid = 1952843189
    diff = get_diff(oldid, revid).changes()
    assert len(diff.changes) == 4
    for c in diff.changes:
        assert c.old == None
    assert diff.changes[0].field == RegularStatement('P6254')
    assert diff.changes[1].field == RankChangeStatement('P6254')
    assert diff.changes[2].field == QualifierChangeStatement(
        pid='P6254', value=StatementLexemeValue(value='L312259'))
    assert diff.changes[2].new == StatementQualifierValue(
        'P6254', StatementLexemeValue(value='L10464'))
    assert diff.changes[3].field == ReferenceChangeStatement(
        pid='P6254', value=StatementLexemeValue(value='L312259'))


@pytest.mark.vcr()
def test_form_usage():
    # https://www.wikidata.org/w/index.php?title=Q4115189&diff=1953435688&oldid=1953425917
    revid = 1953435688
    oldid = 1953425917
    diff = get_diff(oldid, revid).changes()
    assert len(diff.changes) == 4
    for c in diff.changes:
        assert c.old == None

    assert diff.changes[0].field == RegularStatement('P5189')
    assert diff.changes[1].field == RankChangeStatement('P5189')
    assert diff.changes[2].field == QualifierChangeStatement(
        pid='P5189', value=StatementLexemeValue(value='L452382-F1'))
    assert diff.changes[2].new == StatementQualifierValue(
        'P5189', StatementLexemeValue(value='L54611-F1'))
    assert diff.changes[3].field == ReferenceChangeStatement(
        pid='P5189', value=StatementLexemeValue(value='L452382-F1'))


@pytest.mark.vcr()
def test_music_usage():
    # https://www.wikidata.org/w/index.php?title=Q4115189&diff=1953439427&oldid=1953435688
    revid = 1953439427
    oldid = 1953435688
    diff = get_diff(oldid, revid).changes()
    assert len(diff.changes) == 4
    for c in diff.changes:
        assert c.old == None
    assert diff.changes[0].field == RegularStatement('P6604')
    assert diff.changes[2].field == QualifierChangeStatement(
        pid='P6604', value=StatementMusicValue("\\relative c' { c d e f | g2 g | a4 a a a | g1 |}"))


@pytest.mark.vcr()
def test_table_usage():
    # https://www.wikidata.org/w/index.php?title=Q4115189&diff=1953444806&oldid=1953439427
    revid = 1953444806
    oldid = 1953439427
    diff = get_diff(oldid, revid).changes()
    assert len(diff.changes) == 4
    for c in diff.changes:
        assert c.old == None
    assert diff.changes[0].field == RegularStatement('P4045')
    assert diff.changes[2].field == QualifierChangeStatement(
        'P4045', StatementFileLink(
            "https://commons.wikimedia.org/wiki/Data:FileMediaExt.tab", "Data:FileMediaExt.tab")
    )


@pytest.mark.vcr()
def test_geoshape_usage():
    # https://www.wikidata.org/w/index.php?title=Q4115189&diff=1953423760&oldid=1953415294
    revid = 1953423760
    oldid = 1953415294
    diff = get_diff(oldid, revid).changes()
    assert len(diff.changes) == 4
    for c in diff.changes:
        assert c.old == None
    assert diff.changes[2].field == QualifierChangeStatement(
        'P3896', StatementFileLink(
            "https://commons.wikimedia.org/wiki/Data:ROCEEH/Gravettian.map", "Data:ROCEEH/Gravettian.map")
    )
    assert diff.changes[3].field == ReferenceChangeStatement(
        'P3896', StatementFileLink(
            "https://commons.wikimedia.org/wiki/Data:ROCEEH/Gravettian.map", "Data:ROCEEH/Gravettian.map")
    )


@pytest.mark.vcr()
def test_formula_usage():
    # https://www.wikidata.org/w/index.php?title=Q4115189&diff=1953425917&oldid=1953423760
    revid = 1953425917
    oldid = 1953423760
    diff = get_diff(oldid, revid).changes()
    assert len(diff.changes) == 4
    for c in diff.changes:
        assert c.old == None
    assert diff.changes[0].field == RegularStatement('P2534')
    assert diff.changes[0].new == StatementMathValue(
        '{\\displaystyle a^{2}+b^{2}=c^{2}}')
    assert diff.changes[2].field == QualifierChangeStatement(
        'P2534', StatementMathValue('{\\displaystyle a^{2}+b^{2}=c^{2}}'))
    assert diff.changes[3].field == ReferenceChangeStatement(
        'P2534', StatementMathValue('{\\displaystyle a^{2}+b^{2}=c^{2}}'))
    assert diff.changes[3].new == ReferenceValue(
        [Statement(RegularStatement('P2534'), StatementMathValue(
            '{\\displaystyle a^{4}+b^{4}=c^{4}}'))]
    )


@pytest.mark.vcr()
def test_property_usage():
    # https://www.wikidata.org/w/index.php?title=Q4115189&diff=1953446623&oldid=1953446518
    revid = 1953446623
    oldid = 1953446518
    diff = get_diff(oldid, revid).changes()
    assert len(diff.changes) == 4
    for c in diff.changes:
        assert c.old == None
    assert diff.changes[0].field == RegularStatement('P2368')
    assert diff.changes[0].new == StatementPropertyValue('P1889')
    assert diff.changes[2].field == QualifierChangeStatement(
        'P2368', StatementPropertyValue('P1889'))


# curl -s -H 'Accept: application/json'  https://stream.wikimedia.org/v2/stream/recentchange | jq 'select(.meta.domain == "www.wikidata.org")' | jq .revision -c > wikidata_revisions.jsonl
def test_bulk():
    c = 0
    return
    with gzip.open('logs.jsonl') as f:
        while line := f.readline():
            blob = json.loads(line)
            old, new = blob.get('old'), blob.get('new')
            print(old, new)
            if not old or not new:
                continue
            diff = get_diff(old, new)
            if diff:
                diff.changes()
            time.sleep(0.5)
            c += 1
            if c > 100:
                break
