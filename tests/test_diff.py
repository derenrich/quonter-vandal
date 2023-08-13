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
    assert len(diff.changes) == 2
    add_unk_value = diff.changes[0]
    assert (add_unk_value.field == RegularStatement(pid='P5021'))
    assert (add_unk_value.old == None)
    assert (add_unk_value.new == StatementSpecialValue("somevalue"))

    add_unk_rank = diff.changes[1]
    assert (add_unk_rank.field == RankChangeStatement(pid='P5021'))
    assert (add_unk_rank.old == None)
    assert (add_unk_rank.new == "normal")


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


def test_property_ends_in_rank():
    # https://www.wikidata.org/w/index.php?title=Q1515445&diff=1803826490&oldid=1703741037
    revid = 1803826490
    oldid = 1703741037
    diff = get_diff(oldid, revid).changes()
    assert diff.user == "93.176.133.171"
    assert len(diff.changes) == 4


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


DIFFS = [
    [1807597414, 1807597442],
    [1788166880, 1807673132],
    [1699642681, 1807703958],
    [1660621497, 1807711612],
    [1775682727, 1807716376],
    [1720680009, 1828148702],
    [1678055689, 1807823739],
    [1807865433, 1807873607],
    [1719454149, 1807884858],
    [1807924509, 1807927346],
    [1806100936, 1808276823],
    [1778923422, 1808380191],
    [1773892824, 1808445016],
    [1832358499, 1837564921],
    [1925752714, 1925826169],
    [1456093785, 1808446761],
    [1731164280, 1808463506],
    [1806582765, 1861689217],
    [1803785463, 1808526599],
    [1762559876, 1808545101],
    [1807661135, 1830362254],
    [1780943820, 1808563320],
    [1672249808, 1808587088],
    [1788723179, 1808617900],
    [1713104221, 1808636813],
    [1794012371, 1808657765],
    [1854546993, 1858145566],
    [1804953790, 1808691321],
    [1750571818, 1808737689],
    [1799189248, 1808789772],
    [1794451685, 1808815165],
    [1760274394, 1808846927],
    [1291191536, 1808856855],
    [1772710928, 1846082931],
    [1739664776, 1832623497],
    [1849935800, 1852850884],
    [1798186272, 1809021855],
    [1877553861, 1928593101],
    [1790173639, 1808140985],
    [1808169651, 1809029919],
    [1777152111, 1864426173],
    [1806384642, 1809106116],
    [1800801271, 1809853214],
    [1699157931, 1809146023],
    [1729835051, 1809169555],
    [1726225409, 1809170971],
    [1789976805, 1809176437],
    [1780048101, 1809191247],
    [1672857362, 1809217712],
    [1787871047, 1809266377],
    [1582961371, 1809314121],
    [1797924776, 1809323527],
    [1808217808, 1830294244],
    [1840892255, 1844703029],
    [1888130458, 1894585783],
    [1638248386, 1809375262],
    [1750118684, 1809384976],
    [1800419965, 1809399729],
    [1799943779, 1808807871],
    [1808808766, 1809531434],
    [1797672399, 1809554437],
    [1875392576, 1877023123],
    [1791718684, 1809603500],
    [1809737168, 1809737316],
    [1777458610, 1809795844],
    [1791473012, 1861005195],
    [1881861684, 1886352741],
    [1809831701, 1838029904],
    [1773011019, 1809836839],
    [1809873130, 1809873385],
    [1489809701, 1809875968],
    [1784914378, 1809884546],
    [1814777786, 1839779510],
    [1839795806, 1843495064],
    [1843495202, 1843507398],
    [1849854009, 1851105221],
    [1791080916, 1809885041],
    [1832960983, 1834343290],
    [1517004523, 1809930133],
    [574443122, 1809957722],
    [1808559172, 1809979684],
    [1801902720, 1809998934],
    [1817967812, 1820293814],
    [1821116448, 1827836630],
    [1851488731, 1859237165],
    [1875652291, 1896686716],
    [1896695693, 1909671256],
    [1458235882, 1810075701],
    [1776043421, 1810150742],
    [1819206090, 1831849987],
    [1792390111, 1810187427],
    [1713984084, 1810216138],
    [1810232035, 1810232256],
    [1810232726, 1810423749],
    [1810233340, 1810234337],
    [1810236643, 1810429524],
    [1521162022, 1810270816],
    [1779628498, 1810277757],
    [1813458103, 1836333859],
    [1836709357, 1838049289],
    [1843188968, 1843198228],
    [1843223753, 1847438370],
    [1891253034, 1897214001],
    [1900701237, 1911147764],
    [1911150678, 1912517040],
    [1912531741, 1912825063],
    [1912825223, 1912825245]
]


def test_bulk():
    for (i, j) in DIFFS:
        print(i, j)
        get_diff(i, j).changes()
