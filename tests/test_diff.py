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


DIFFS = [
    [1812009089, 1812010723],
    [1804638109, 1812025592],
    [1827880759, 1832395721],
    [1873634717, 1874733994],
    [1874770065, 1876858902],
    [1876880300, 1891270183],
    [1891270362, 1891271031],
    [1891271201, 1891271241],
    [1891271314, 1891275492],
    [1811546156, 1812030146],
    [1499093073, 1812049676],
    [1710239985, 1812147907],
    [1812248570, 1812248572],
    [1796878489, 1812295400],
    [1811775489, 1812296330],
    [1813463130, 1813951084],
    [1636727623, 1812397254],
    [1746728572, 1898751731],
    [1361923457, 1812504510],
    [1782902066, 1812511077],
    [1795683161, 1812527134],
    [1760319346, 1812552702],
    [1778713369, 1812632623],
    [1818110596, 1839833204],
    [1847772997, 1848084235],
    [1849925055, 1872011807],
    [1884935223, 1892322822],
    [1735522304, 1812643748],
    [1807476376, 1812108070],
    [1812245857, 1812656072],
    [1753044746, 1812706204],
    [1774225337, 1812730375],
    [1720617570, 1812755933],
    [1402413915, 1812848197],
    [1812827663, 1812861128],
    [1802365955, 1813091265],
    [1787685332, 1813164029],
    [1824840115, 1839532307],
    [1867858669, 1873087222],
    [1740569972, 1813303588],
    [1798479221, 1813315661],
    [1882869338, 1897096304],
    [1906152512, 1909525021],
    [1784711257, 1813327115],
    [1480797121, 1813342102],
    [1759966011, 1813407208],
    [1601689679, 1813443466],
    [1523293053, 1813450754],
    [1816406198, 1877488236],
    [1809620138, 1813460294],
    [1351901299, 1813459998],
    [1650208158, 1813462514],
    [1880008889, 1894140574],
    [1786446236, 1813464735],
    [1389081901, 1813506465],
    [1785132746, 1813526960],
    [1772892775, 1813557948],
    [1813566954, 1813567038],
    [1785154813, 1813698731],
    [1803549902, 1813713087],
    [1840353497, 1840821521],
    [1801191599, 1819335835],
    [1794707540, 1813730386],
    [1877167985, 1890939892],
    [1775431930, 1835392176],
    [1787634111, 1813839037],
    [1790641570, 1813909733],
    [1849067847, 1851324101],
    [1746311366, 1813928821],
    [1734563048, 1813948621],
    [1813462900, 1813948719],
    [1699598849, 1813956505],
    [1790965582, 1844547211],
    [1810160137, 1813994656],
    [1812618364, 1814032103],
    [1710235929, 1819662869],
    [1788279221, 1814159648],
    [1859341921, 1867171756],
    [1573598442, 1814166033],
    [1714064841, 1814194280],
    [1748211311, 1879123442],
    [1790455529, 1814232645],
    [1872149407, 1901984918],
    [1763211039, 1874366048],
    [1813218457, 1814522849],
    [1813219477, 1814528382],
    [1790756397, 1834429291],
    [1836116601, 1842409964],
    [1365406628, 1814642234],
    [1707931528, 1814661447],
    [1736617967, 1814664427],
    [1748285044, 1814672697],
    [1605586691, 1814674094],
    [1790304167, 1814677354],
    [1748262904, 1814677180],
    [1781198909, 1814695654],
    [1812040457, 1814821837],
    [1765667935, 1814832585],
    [1262739905, 1814932832],
    [1521909713, 1814933079],
    [1778027542, 1814972402],
    [1654373796, 1814986121],
    [1428324528, 1814997371],
    [1084558414, 1815238152],
    [1782206051, 1815258330],
    [1800026354, 1815338614],
    [1796535060, 1815347611],
    [929396000, 1815363598],
    [1586700551, 1815395024],
    [1683929182, 1815413813],
    [1812081177, 1815493207],
    [1748128375, 1815624514],
    [1776701876, 1815632350],
    [1826729550, 1828613469],
    [1446531607, 1815658448],
    [1778247866, 1839515305],
    [1895922758, 1900818734],
    [1784015752, 1815716299],
    [1193168541, 1815841578],
    [1379239606, 1815953759],
    [1781516494, 1815948061],
    [1813491766, 1816020946],
    [1775076715, 1816123715],
    [1794103880, 1816181516],
    [1804305762, 1816196232],
    [1720754655, 1816579148],
    [1476146547, 1854145571],
    [1534442013, 1816952951],
    [1763411602, 1817228537],
    [1812790729, 1817241087],
    [1882172871, 1882953977],
    [1883055545, 1885644442],
    [1815487790, 1817417263],
    [1817442573, 1817442643],
    [1817447390, 1817447519],
    [1787054762, 1811789796],
    [1811790256, 1812998778],
    [1814632204, 1817447946],
    [1839940185, 1851827550],
    [1883568820, 1889436325],
    [1889513477, 1905362571],
    [1905364443, 1921746990],
    [1921807259, 1924355495],
    [1817471905, 1817472140],
    [1805503641, 1817506330],
    [1805923138, 1817553512],
    [1835701909, 1843474627],
    [1924932489, 1928255690],
    [1629663731, 1817562615],
    [1739003442, 1817594138],
    [1817692747, 1817693071],
    [1794248038, 1817737664],
    [1817490419, 1817738184],
    [1807601978, 1817790651],
    [1905346770, 1905956282],
    [1815810523, 1817809489],
    [1817809645, 1817974174],
    [1778705810, 1818136271],
    [1757305809, 1818144275],
    [1794695191, 1818254092],
    [1797517050, 1818257122],
    [1775361379, 1818286646],
    [1811988095, 1818300818],
    [1793711222, 1818314956],
    [1793711036, 1818315752],
    [1783147343, 1818346667],
    [1756273207, 1818476309],
    [1814657855, 1818383831],
    [1867513070, 1888139347],
    [1915932096, 1923510001],
    [1800099518, 1821750387],
    [1814696695, 1818390329],
    [1815404379, 1818393905],
    [1782381997, 1818409349],
    [1808423970, 1818423705],
    [1791150665, 1818437782],
    [1523060413, 1818446884],
    [1773933003, 1818447643],
    [1348597527, 1818512498],
    [1775172375, 1818549052],
    [1804182393, 1818585659],
    [1818586298, 1818586564],
    [1729233134, 1818737721],
    [1809019018, 1818856258],
    [1843201615, 1844564532],
    [1855742517, 1857242322],
    [1817523723, 1823726251],
    [1806742772, 1818872144],
    [1374039188, 1818883637],
    [1747315256, 1800310289],
    [1818859049, 1829324817],
    [1668466403, 1818927173],
    [1764109078, 1848147869],
    [1809762838, 1819094192],
    [1862114509, 1863187057],
    [1818528224, 1819109852],
    [1819241414, 1825024604],
    [1825070983, 1871462078],
    [1819116134, 1819116246],
    [1833439748, 1839362027],
    [1819147927, 1819148319],
    [1793113845, 1819152580],
    [1787882558, 1819381534],
    [1805007718, 1819472279],
    [1837560894, 1855138068],
    [1664404473, 1819624795],
    [1819709471, 1819709739],
    [1857492647, 1864753417],
    [1662760045, 1819720402],
    [1805470132, 1819724088],
    [1804478824, 1908179277],
    [1760307402, 1819808552],
    [1778362249, 1819826865],
    [1568861276, 1819855918],
    [1812434916, 1819864576],
    [1856020598, 1857002034],
    [1804095688, 1819873399],
    [1798907864, 1820011136],
    [1595149872, 1820251118],
    [1806420905, 1820251134],
    [1756164856, 1820254003],
    [1365961631, 1820268613],
    [1774270293, 1820268940],
    [1420912089, 1820269724],
    [1789310425, 1820270085],
    [1788413005, 1820272434],
    [1820298630, 1820298767],
    [1812392318, 1822346963],
    [1822594096, 1829144430],
    [1849907491, 1857457960],
    [1882023692, 1882419222],
    [1905872583, 1913651438],
    [701053303, 1820317579],
    [1775639741, 1820361437],
    [1820362844, 1820363025],
    [1582863785, 1820369965],
    [1759376613, 1820369639],
    [1820380523, 1820380621],
    [1807841578, 1813308317],
    [1817681980, 1819842956],
    [1819905308, 1821933238],
    [1853354421, 1855669491],
    [1890685475, 1894431023],
    [1820502050, 1820502257],
    [1820502302, 1820502500],
    [1679305847, 1820566806],
    [1805553690, 1820571367],
    [1423308693, 1820632621],
    [1820922374, 1820922747],
    [1693725042, 1820971494],
    [1820326356, 1820982911],
    [1819683130, 1821124514],
    [1815735114, 1821155414],
    [1876871317, 1925691978],
    [1925693688, 1925694538],
    [1925694644, 1925695437],
    [1628169272, 1821174535],
    [1793291548, 1821183068],
    [1791095420, 1812964198],
    [1819664678, 1821431791],
    [1826500000, 1847235470],
    [1863355200, 1879019246],
    [1902472113, 1905801624],
    [1905807020, 1916886884],
    [1793246695, 1821590802],
    [1821895632, 1821928345],
    [1822349047, 1823277522],
    [1822031760, 1822034264],
    [1797445808, 1822110490],
    [1810215000, 1822128423],
    [1809955134, 1822180635],
    [1851467935, 1887051604],
    [1815499266, 1822206025],
    [1822885246, 1822885454],
    [1785800253, 1822247808],
    [1723787580, 1822527505],
    [1773951522, 1822700704],
    [1738686327, 1822725456],
    [1807289304, 1822748100],
    [1810708884, 1822834093],
    [1830817665, 1835960236],
    [1847710157, 1847979393],
    [1814745941, 1822919313],
    [1857746819, 1859202538],
    [1708854657, 1822935234],
    [1619600259, 1822944762],
    [1639032564, 1822988597],
    [1821730719, 1823056906],
    [1914353194, 1914630028],
    [1702521419, 1823156043],
    [1802225414, 1823196917],
    [1794328128, 1823237117],
    [1785690362, 1823254824],
    [1782735342, 1823314864],
    [1848092944, 1850252320],
    [1702425203, 1823350425],
    [1528222894, 1823411607],
    [1765301878, 1823420167],
    [1780109040, 1834704401],
    [1808989238, 1823470166],
    [1569752521, 1823523641],
    [1818870657, 1823626564],
    [1839389750, 1841614626],
    [1811952291, 1823626969],
    [1722812828, 1844400608],
    [1719220365, 1823681028],
    [1812546766, 1823734598],
    [1867544879, 1910015200],
    [1812787668, 1823754427],
    [1730651147, 1823767620],
    [1812022402, 1823790613],
    [1757296012, 1870557198],
    [1618268133, 1823850081],
    [1792168950, 1823851822],
    [1790506265, 1823885969],
    [1859347917, 1879307446],
    [1673581612, 1824059246],
    [1817508600, 1823956835],
    [1865992985, 1890507028],
    [1798992237, 1823964390],
    [1829290043, 1841587540],
    [1798787716, 1824014225],
    [1846306695, 1899152946],
    [1899305742, 1901357627],
    [1822431824, 1824019287],
    [1766400649, 1824043706],
    [1813767936, 1834051678],
    [1835181371, 1847253865],
    [1755543376, 1824088100],
    [1801351126, 1824154968],
    [1825382351, 1837074609],
    [1814987413, 1824273337],
    [1824299338, 1824299443],
    [1787152626, 1824321137],
    [1795393213, 1824321194],
    [1549635942, 1824330384],
    [1787893149, 1824332549],
    [1619287802, 1824368486],
    [1753020415, 1824372767],
    [1814735726, 1824396553],
    [1846999839, 1856793460],
    [1908752696, 1910876096],
    [1717359186, 1824475422],
    [1569110017, 1824541747],
    [1783409440, 1824577849],
    [1820300683, 1824611153],
    [1804851163, 1817134203],
    [1822932516, 1824620787],
    [1885094200, 1903193330],
    [1903642063, 1903861321],
    [1802922881, 1824632467],
    [1698968191, 1824639170],
    [1824639181, 1824639390],
    [1814912207, 1824645673],
    [1776211115, 1824647517],
    [1793748028, 1819452586],
    [1819683672, 1842688457],
    [1842688711, 1869163242],
    [1770239317, 1824670123],
    [1741661593, 1808266397],
    [1813685422, 1824728503],
    [1763745917, 1824719852],
    [1824731793, 1824731941],
    [1869937818, 1869938444],
    [1692746275, 1824738875],
    [1824733717, 1824757613],
    [1818808139, 1824807350],
    [1824809802, 1824809897],
    [1522212194, 1824831602],
    [1810515075, 1824860405],
    [1813517382, 1824883152],
    [1775041827, 1825117028],
    [1783971252, 1825131548],
    [1803146147, 1825139555],
    [1757313686, 1825246030],
    [1733877557, 1825316165],
    [1785671667, 1830070556],
    [1824734488, 1825342866],
    [1822397223, 1825380003],
    [1328952782, 1825385807],
    [1489568165, 1825409524],
    [1805704781, 1825419271],
    [1814337906, 1825446011],
    [1825438162, 1906731643],
    [1678931569, 1825484161],
    [1741830090, 1825618729],
    [1565197572, 1825634902],
    [1825678604, 1825679202],
    [1636772111, 1825697329],
    [1731490131, 1825735995],
    [1787939352, 1825738214],
    [1775499041, 1825782035],
    [1895210102, 1898698604],
    [1824683573, 1825820748],
    [1751016278, 1826016621],
    [1818428935, 1826030978],
    [1826092861, 1826093045],
    [1655726688, 1826322563],
    [1584339357, 1826384284],
    [1809179591, 1826414363],
    [1772177029, 1826431951],
    [1826526844, 1857055417],
    [1347958070, 1826693458],
    [1685577117, 1826703682],
    [1728137374, 1826790128],
    [1778694902, 1826797002],
    [1755870220, 1826804021],
    [1795101346, 1826807963],
    [1823731531, 1826892267],
    [1826762639, 1827048267],
    [1821363816, 1827097023],
    [1787897006, 1827167073],
    [1857559433, 1897301714],
    [1786722327, 1827223633],
    [1824473836, 1827375432],
    [1812698484, 1827395491],
    [1805986159, 1827419819],
    [1744098068, 1827422414],
    [1796633907, 1827500467],
    [1791402487, 1822765397],
    [1826607209, 1827590878],
    [1835503986, 1846031079],
    [1722136313, 1827594372],
    [1828346774, 1833262862],
    [1726776762, 1827691667],
    [1797822119, 1827866212],
    [1800868257, 1827982632],
    [1802882406, 1828314899],
    [1871937787, 1874346191],
    [1812550490, 1858793687],
    [1826461564, 1828335923],
    [1778849455, 1828364941],
    [1828367859, 1828368619],
    [1686374115, 1828401890],
    [1826833408, 1828412839],
    [1797026327, 1828418292],
    [1828525934, 1828538311],
    [1569778880, 1828572380],
    [1626685174, 1918145411],
    [1785865145, 1828634980],
    [1791476418, 1813539405],
    [1814032057, 1828389311],
    [1828444002, 1828638627],
    [1864493943, 1867350560],
    [1828706652, 1828707700],
    [1826549321, 1902565808],
    [1708977598, 1828732840],
    [1828720421, 1828802594],
    [508375019, 1828804497],
    [1574293102, 1828808161],
    [1824816185, 1828850213],
    [1807338189, 1828917451],
    [1733168710, 1828918767],
    [1828203891, 1829098774],
    [1826789791, 1829131785],
    [1829223447, 1829223572],
    [1727482918, 1829258228],
    [1824851238, 1830254479],
    [1878761573, 1897237647],
    [1820457782, 1829312186],
    [1788181369, 1851699585],
    [1763659234, 1829330768],
    [1802028580, 1829354509],
    [1742754536, 1829369153],
    [1789856953, 1829383144],
    [1828359882, 1848953348],
    [1648129089, 1829419454],
    [1807958129, 1829471379],
    [1819606044, 1829662965],
    [1778320388, 1829743357],
    [1830051185, 1893074461],
    [1893557710, 1893558464],
    [1830074789, 1830075108],
    [1822550651, 1835018334],
    [1882030132, 1892294535],
    [1893207041, 1893590072],
    [1895003558, 1896265486],
    [1822812685, 1830115103],
    [1832708720, 1833235779],
    [1748127060, 1833798500],
    [1746715010, 1830149050],
    [1820419446, 1830233327],
    [1393911892, 1830244345],
    [1823011751, 1830871704],
    [1426567924, 1830315126],
    [1781748427, 1830397866],
    [1701848558, 1830530703],
    [1813376711, 1825496045],
    [1827009606, 1830590425],
    [1859032511, 1862279924],
    [1883206964, 1892791842],
    [1910231289, 1912668608],
    [1827184499, 1830638606],
    [1817457048, 1830825710],
    [1372560411, 1830928861],
    [1830888621, 1831153166],
    [1746012970, 1831204306],
    [1791537908, 1845204409],
    [1783511820, 1831286712],
    [1800624111, 1831635996],
    [1829349819, 1831651340],
    [1838959194, 1863121443]
]


def test_bulk():
    for (i, j) in DIFFS:
        print(i, j)
        get_diff(i, j).changes()
