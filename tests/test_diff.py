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


def test_no_such_diff():
    # https://www.wikidata.org/w/index.php?title=1814194280&diff=1838236382&oldid=1747008787
    revid = 1838236382
    oldid = 1747008787
    diff = get_diff(oldid, revid)
    assert diff == None


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


DIFFS = [
    [1799817913, 1800002446],
    [1799720965, 1800002423],
    [1799942516, 1800004457],
    [1799957297, 1800006388],
    [1800007376, 1800007541],
    [1800007667, 1800007986],
    [1800008068, 1800008360],
    [1800008598, 1800008679],
    [1800009245, 1800012156],
    [1768648811, 1800011398],
    [1800011455, 1800037865],
    [1800038084, 1800038587],
    [1800038659, 1800038799],
    [1795350208, 1800011323],
    [1800011586, 1800011808],
    [1800011969, 1800012045],
    [1800012115, 1800012540],
    [1771764109, 1800012586],
    [1800011450, 1800012977],
    [1800012985, 1800013015],
    [1800013383, 1800013466],
    [1796221572, 1800014486],
    [1796407163, 1800015499],
    [1800016300, 1801350544],
    [1796367059, 1800017175],
    [1796418596, 1800017625],
    [1092050773, 1800019539],
    [1797770845, 1800020377],
    [1771516827, 1800021526],
    [1796405822, 1800021658],
    [1796408954, 1800021996],
    [1800022873, 1800023275],
    [1800098881, 1800323697],
    [1796367273, 1800024112],
    [1796405943, 1800024508],
    [1796406197, 1800024683],
    [1796399100, 1800025057],
    [1354695831, 1800028357],
    [1800028444, 1800029230],
    [1800029871, 1800030099],
    [1800030203, 1800030733],
    [1800030812, 1800031673],
    [1800031717, 1800031871],
    [1768710740, 1800033086],
    [1800033629, 1800033712],
    [1800034054, 1800034137],
    [1800034200, 1800034349],
    [1800034531, 1800034918],
    [1800035309, 1800035866],
    [1800035926, 1800036181],
    [1800036313, 1800036525],
    [1800038834, 1800038964],
    [1800039253, 1800039526],
    [1800039872, 1800039900],
    [1800767535, 1800770948],
    [1800040467, 1800041831],
    [1768713362, 1800040546],
    [1800040976, 1800041011],
    [1800041110, 1800041966],
    [1800042132, 1800042290],
    [1800042367, 1800042542],
    [1800042739, 1800042764],
    [1308611957, 1800044499],
    [1768654147, 1800043490],
    [1800043882, 1800044331],
    [1800044351, 1800044778],
    [1800045008, 1800045515],
    [1575508312, 1800047632],
    [1800047740, 1800048012],
    [1800048175, 1800053694],
    [1800053984, 1800054437],
    [1800045462, 1800045654],
    [1800046141, 1800046219],
    [1800046424, 1800046606],
    [1800046437, 1800046524],
    [1798787114, 1800047578],
    [1800047013, 1800047599],
    [1800048114, 1800048216],
    [1800048230, 1800048515],
    [1800048708, 1800048837],
    [1800054916, 1800054963],
    [1800055335, 1800059223],
    [1799718386, 1800062446],
    [1800063383, 1800064481],
    [1800062913, 1800073841],
    [1710108750, 1800070319],
    [1800071303, 1800072870],
    [1800055183, 1800073446],
    [1800091764, 1800091922],
    [1342836354, 1800076726],
    [1800077116, 1800078156],
    [1800078272, 1800079319],
    [1800080866, 1800081043],
    [1800081483, 1800085097],
    [1800081272, 1800084650],
    [1796422941, 1800089005],
    [1800089646, 1800091889],
    [1800092185, 1800092798],
    [1800090790, 1800091311],
    [1800093753, 1800093969],
    [1521802669, 1800094413],
    [1800094894, 1800095004],
    [1800095053, 1800095148],
    [1800095744, 1800096293],
    [1800096348, 1800096483],
    [1800097109, 1800097185],
    [1800097856, 1800098153],
    [1800098194, 1800776060],
    [1800097237, 1800098760],
    [1800098803, 1800099212],
    [1800099346, 1800774677],
    [1799881866, 1800101597],
    [1799891575, 1800102965],
    [1800101305, 1800102902],
    [1800103275, 1800103431],
    [1786648018, 1800102623],
    [1796039671, 1800103025],
    [1787424327, 1800105710],
    [1800106074, 1800106369],
    [1800108872, 1800124625],
    [1800124859, 1800127121],
    [1800110809, 1800116690],
    [1800116757, 1800116807],
    [1724043241, 1800116715],
    [1800115279, 1800117860],
    [1800118730, 1818458071],
    [1783716289, 1800118036],
    [1791675028, 1800118604],
    [1790575184, 1800118931],
    [1798043354, 1800127320],
    [1794529791, 1800127654],
    [1793381734, 1800128305],
    [1768712880, 1800131947],
    [1800132286, 1800132387],
    [1800132449, 1800132493],
    [1800132568, 1800132805],
    [1768713542, 1800133243],
    [1800133449, 1800133776],
    [1800133918, 1800134023],
    [1768728597, 1800134719],
    [1800135135, 1800135323],
    [1799935277, 1800140691],
    [1800140992, 1800141643],
    [1800142087, 1800142749],
    [1800142896, 1800143854],
    [1800135363, 1800135424],
    [1800135628, 1800135764],
    [1783639519, 1800136149],
    [1800136567, 1800136593],
    [1800136773, 1800136828],
    [1685883259, 1800140209],
    [1800137101, 1800137255],
    [1800137336, 1800137508],
    [1768648840, 1800137587],
    [1800183746, 1800200513],
    [1800200738, 1800200830],
    [1800200854, 1800200906],
    [1800201149, 1800201265],
    [1800137895, 1800141080],
    [1800142970, 1800145566],
    [1468708790, 1800146675],
    [1800146150, 1800147378],
    [1800149203, 1800150917],
    [1800151987, 1800153442],
    [1800155271, 1800157816],
    [1770966125, 1800210339],
    [1800159131, 1800159264],
    [1800159127, 1800161483],
    [1802203815, 1802204033],
    [1517421973, 1800160907],
    [1783715720, 1800162135],
    [1799053270, 1823264353],
    [1736148714, 1800166747],
    [1710328668, 1800168921],
    [1778630885, 1800168934],
    [1746999137, 1800171610],
    [1800187200, 1800212692],
    [1791919807, 1800173290],
    [1800174120, 1800176523],
    [1747221307, 1800177058],
    [1731458863, 1800177312],
    [1800188039, 1800209373],
    [1800179563, 1800180890],
    [1770965428, 1800189259],
    [1800190525, 1800207782],
    [1776243508, 1800189386],
    [1800190711, 1800213201],
    [1770726962, 1800189694],
    [1800191289, 1800208436],
    [1776243367, 1800184211],
    [1800184264, 1800189744],
    [1800191350, 1800211706],
    [1800183619, 1800184099],
    [1800184965, 1800185008],
    [1800185274, 1800185398],
    [1800185464, 1800185504],
    [1800185652, 1800185719],
    [1777218663, 1800189832],
    [1800191667, 1800228783],
    [1776296015, 1800185419],
    [1800191740, 1800212525],
    [1776322220, 1800189893],
    [1800191799, 1800213308],
    [1800183636, 1800186184],
    [1800186499, 1800186730],
    [1800187045, 1800187153],
    [1087897736, 1800186435],
    [1801063918, 1803145455],
    [1084749758, 1803107110],
    [1088957832, 1803172667],
    [1082541086, 1800187385],
    [1800186781, 1800228361],
    [1795191291, 1800187592],
    [1800187641, 1800208761],
    [1800183648, 1800187773],
    [1800187825, 1800189652],
    [1800189845, 1800190272],
    [1091089189, 1800188045],
    [1090906031, 1800188418],
    [1745118857, 1800188331],
    [1800188444, 1800228481],
    [1787868763, 1800188887],
    [1800189020, 1800189400],
    [1766364147, 1800188546],
    [1084635660, 1800188828],
    [1800188724, 1800188925],
    [1800189139, 1800189279],
    [1090962982, 1800189271],
    [1736560488, 1800189030],
    [1800190167, 1800211876],
    [1766364568, 1800189069],
    [1773100083, 1800189144],
    [1800190276, 1800230796],
    [1692107524, 1800189197],
    [1800190363, 1800209143],
    [1788164073, 1800189326],
    [1088920476, 1800189663],
    [1692032281, 1800189511],
    [1800190770, 1800212151],
    [1692021304, 1800189544],
    [1770965422, 1800189638],
    [1800191239, 1800209008],
    [1719854310, 1800189780],
    [1800191507, 1800208584],
    [1775763688, 1800189924],
    [1800191999, 1800213510],
    [1800183658, 1800190487],
    [1800190577, 1800190746],
    [1800183672, 1800190815],
    [1800190874, 1800191589],
    [1800191691, 1800191759],
    [1082339408, 1800191227],
    [1089094179, 1800191711],
    [1796459659, 1800192174],
    [1708856122, 1800192049],
    [1800192177, 1800192335],
    [1800192581, 1800192684],
    [1800189682, 1800194355],
    [1796461484, 1800192633],
    [1084690621, 1800193108],
    [1084570414, 1800193258],
    [1800183687, 1800193977],
    [1800194057, 1800194302],
    [1800194453, 1800194992],
    [1800193124, 1800201025],
    [1800183692, 1800195261],
    [1800195407, 1800195763],
    [1800196139, 1800196227],
    [1090060081, 1800196209],
    [1082389346, 1800196552],
    [1800183697, 1800196358],
    [1800196423, 1800197431],
    [1800197656, 1800197749],
    [1091926928, 1800196827],
    [1090055956, 1800197099],
    [1796458236, 1800197748],
    [1796458392, 1800198017],
    [1800197813, 1800197867],
    [1800198002, 1800198316],
    [1800198443, 1800198474],
    [1800198564, 1800198635],
    [1796480970, 1800198402],
    [1087803557, 1800198672],
    [1800183716, 1800198693],
    [1800199162, 1800199243],
    [1800199469, 1800199540],
    [1091049706, 1800199076],
    [1082359651, 1800199413],
    [1082346127, 1800199846],
    [1796477256, 1800200144],
    [1800200553, 1800200636],
    [1089019287, 1800200903],
    [1800201506, 1800201569],
    [1800201301, 1800202048],
    [1784100388, 1800201957],
    [1800202394, 1800202453],
    [1800202512, 1800202580],
    [1800202628, 1800202773],
    [1800203839, 1800204664],
    [1800204937, 1800205026],
    [1800205178, 1800205252],
    [1764448062, 1800203172],
    [1800202889, 1800203074],
    [1800203321, 1800203463],
    [1800203711, 1800203881],
    [1800203898, 1800203949],
    [1800203956, 1800204046],
    [1800204373, 1800204442],
    [1800205155, 1800227717],
    [1768649968, 1800205543],
    [1800205587, 1800205705],
    [1032820471, 1800207259],
    [1800188157, 1800207660],
    [1800206721, 1800208067],
    [1800191129, 1800208190],
    [1796277336, 1800209089],
    [1084539618, 1800209623],
    [1800187544, 1800209631],
    [1088083895, 1800210112],
    [1800187863, 1800210049],
    [1796294195, 1800210478],
    [1793467170, 1800210273],
    [1087988456, 1800210950],
    [1793302937, 1800210997],
    [1792636493, 1800211616],
    [1340613878, 1800213733],
    [1800191858, 1800212858],
    [1800188785, 1800213016],
    [1488458853, 1800213469],
    [1800213048, 1800213381],
    [1338191326, 1800214664],
    [1793903101, 1800215515],
    [1800216703, 1800216986],
    [1800217072, 1800217225],
    [1800217466, 1800217544],
    [1772400219, 1800218484],
    [1800220798, 1800220901],
    [1800221979, 1800222156],
    [1783064876, 1800222748],
    [1793378149, 1800223085],
    [1795131999, 1800223257],
    [1800223855, 1800224138],
    [1795936090, 1800225029],
    [1768708016, 1800225043],
    [1800226101, 1800226506],
    [1800226618, 1800226708],
    [1795020007, 1800225177],
    [1800225437, 1800225546],
    [1800225369, 1800225511],
    [1593965175, 1800225651],
    [1795200981, 1800226362],
    [1800227197, 1800227521],
    [1800227567, 1800227657],
    [1800228164, 1800228377],
    [1800228442, 1800229486],
    [1800229603, 1800229872],
    [1800228503, 1800228849],
    [1795028670, 1800230103],
    [1800230138, 1800230252],
    [1800232098, 1800232197],
    [1800116662, 1800231157],
    [1800233554, 1800235933],
    [1796660529, 1800234515],
    [1800192109, 1800236012],
    [1798540169, 1800236039],
    [1800237889, 1800238162],
    [1796505299, 1804562899],
    [1800237793, 1800239526],
    [1800238431, 1800238639],
    [1800239873, 1800240243],
    [1800240564, 1800242498],
    [1800245056, 1800245223],
    [1800247008, 1800247279],
    [1787249190, 1800250236],
    [1796103534, 1801375057],
    [1096623308, 1800251364],
    [1796826601, 1800253552],
    [1800252630, 1800252784],
    [1800257957, 1800261812],
    [1800262676, 1800262801],
    [1796377920, 1800267314],
    [1800267272, 1800267535],
    [1796510158, 1800269067],
    [1800270031, 1800270167],
    [1800270410, 1800270546],
    [1800270591, 1800270692],
    [1796530580, 1800271088],
    [1800266320, 1800271853],
    [1800271927, 1800272030],
    [1800272078, 1800272461],
    [1800272380, 1800272551],
    [1088121436, 1800276158],
    [1800272928, 1800273012],
    [1026719072, 1800273350],
    [1800273142, 1800273362],
    [1799823956, 1800274970],
    [1800276761, 1800276871],
    [1714919887, 1800277828],
    [1800277952, 1800278369],
    [1714957160, 1800278933],
    [1800279216, 1800279315],
    [1800278945, 1800279016],
    [1800279633, 1800279948],
    [1787168742, 1800280739],
    [1800280551, 1800280772],
    [1800281225, 1800281699],
    [1795082234, 1800281952],
    [1800282168, 1800282355],
    [1409947507, 1800281975],
    [1796057372, 1800283383],
    [1800283639, 1800284127],
    [1800284879, 1800284951],
    [1788248106, 1800286275],
    [1096683426, 1800287099],
    [1780292661, 1800288388],
    [1784760170, 1800289326],
    [1794850303, 1800289850],
    [1792666961, 1800291292],
    [1794965121, 1800292020],
    [1789522743, 1800292126],
    [1772726095, 1800292270],
    [1800292746, 1800293015],
    [1800293151, 1800293255],
    [1800281837, 1800292438],
    [1800336513, 1800425870],
    [1800292751, 1800292888],
    [1800281089, 1800293761],
    [902792664, 1805938715],
    [1782946563, 1800294504],
    [1750769146, 1800294945],
    [1800295063, 1800295178],
    [1800295152, 1800295563],
    [1800295648, 1800295815],
    [1784032038, 1800295780],
    [1800295694, 1800295859],
    [1796739046, 1800296164],
    [1800296338, 1800296920],
    [1800297367, 1800297483],
    [1800297592, 1800298095],
    [1800296481, 1800297053],
    [1782941952, 1800297716],
    [1800297821, 1800298053],
    [1800298123, 1800302993],
    [1800303211, 1800303293],
    [1800298947, 1800299329],
    [1800300099, 1800300801],
    [1742115705, 1800302020],
    [1736943580, 1800303337],
    [1800303492, 1800303591],
    [1800303616, 1800305288],
    [1800305607, 1800305747],
    [1800031856, 1800304285],
    [1782735280, 1800304923],
    [1800305170, 1800305283],
    [1800306592, 1800306738],
    [1785847355, 1800307899],
    [1800307468, 1800307873],
    [1800308095, 1800308216],
    [1714515701, 1800309074],
    [1741724900, 1802009538],
    [1738625562, 1800309312],
    [1704979911, 1800310741],
    [1800311737, 1800311778],
    [1801481757, 1801730036],
    [1549416329, 1800315661],
    [1688013365, 1800315745],
    [1800316544, 1800317028],
    [1773741882, 1800321900],
    [1792420847, 1800338571],
    [1799631536, 1800339373],
    [1794391084, 1800340006],
    [1804549403, 1808608547],
    [1089948803, 1800344111],
    [1082368356, 1800344523],
    [1800354708, 1803216513],
    [1084738066, 1800345599],
    [1091061905, 1800346071],
    [1096688384, 1800347031],
    [1800391381, 1803238744],
    [1770705034, 1800347462],
    [1082489547, 1800348844],
    [1772008644, 1800349709],
    [1096657095, 1800354134],
    [1772004701, 1800356200],
    [1772005191, 1800357117],
    [1772004522, 1800357217],
    [1772004630, 1800357504],
    [1587922163, 1800359919],
    [1800383467, 1800385728],
    [1800359545, 1800363031],
    [1087816239, 1800363422],
    [1091043173, 1800363905],
    [1800375968, 1803216064],
    [1798953289, 1800372648],
    [1796610314, 1800373353],
    [1800373115, 1800375999],
    [1800376155, 1800394336],
    [1800395623, 1800398711],
    [1795629514, 1800405451],
    [1791806322, 1803164751],
    [1694631935, 1800417463],
    [1756087367, 1800434507],
    [1800434587, 1800435059],
    [1770696973, 1805990236],
    [1409969533, 1805954246],
    [1800379448, 1800438551],
    [1800383548, 1800438596],
    [1345287095, 1800438976],
    [1800360449, 1800440915],
    [1800439310, 1800440423],
    [1783749303, 1800439774],
    [902974418, 1806010839],
    [1770640869, 1800446076],
    [1770640832, 1800446137],
    [1084662495, 1800454262],
    [1096676705, 1800447199],
    [1096655103, 1800447620],
    [1096609565, 1800448143],
    [1096676156, 1800448580],
    [1410856369, 1800449294],
    [1800264103, 1800449926],
    [1800403893, 1800461508],
    [1800452907, 1800453842],
    [1800453041, 1800453897],
    [1799501571, 1800461118],
    [1778236566, 1800466312],
    [1774136369, 1800467517],
    [1800485948, 1800486450],
    [1800486874, 1800489145],
    [1800489387, 1800490645],
    [1800485891, 1800499117],
    [1800152379, 1801379033],
    [1406636146, 1803200163],
    [1761473839, 1800509387],
    [1787886064, 1800512842],
    [1789793402, 1800519927],
    [1804547534, 1807323061],
    [1800264004, 1800522066],
    [1801252666, 1803407044],
    [1800263790, 1800522127],
    [1801253982, 1803407097],
    [1800147036, 1800526450],
    [1784128818, 1800527337],
    [1795765920, 1800528016],
    [1726312338, 1800531193],
    [1800532187, 1800535407],
    [1478001782, 1800544733],
    [1087933475, 1800546405],
    [1089116339, 1800547056],
    [1479129271, 1800548520],
    [1800548526, 1800548550],
    [1091958898, 1800549425],
    [1091106242, 1800550060],
    [1800550956, 1800552177],
    [1771143317, 1800552111],
    [1588058881, 1800552600],
    [1772067894, 1800553841],
    [1712747772, 1800555644],
    [1812842439, 1812850608],
    [1773564340, 1800556757],
    [1773935164, 1800557358],
    [1773564324, 1800557636],
    [1773610376, 1800557743],
    [1773577359, 1800557830],
    [1800263935, 1804413557],
    [1773610575, 1800559084],
    [1773845567, 1800559238],
    [1800403917, 1800560912],
    [1789835153, 1800569516],
    [1783751239, 1800570077],
    [1783751203, 1800570481],
    [1559232788, 1800570881],
    [1783751478, 1800571801],
    [1786728670, 1800572006],
    [1787262689, 1800572144],
    [1783751028, 1800572305],
    [1783750466, 1800572531],
    [1797222347, 1800572777],
    [1740543900, 1800573776],
    [1799984498, 1800584802],
    [1344280673, 1800586487],
    [1800598540, 1800599248],
    [1800604673, 1800607528],
    [1800590975, 1800607928],
    [1800615033, 1812830376],
    [1800614946, 1800615988],
    [1800324113, 1801376538],
    [1795725818, 1800623540],
    [1800264035, 1800627410],
    [1795680650, 1800628019],
    [1795680624, 1800628452],
    [1795680577, 1800628598],
    [1795665724, 1800629592],
    [1366101194, 1800667522],
    [1799979414, 1800674334],
    [1796004522, 1800678000],
    [1469775546, 1800680615],
    [1781257035, 1800680852],
    [1703469609, 1800681217],
    [1540871667, 1800681421],
    [1800681589, 1800681781],
    [1597199725, 1800682423],
    [1774388911, 1800683074],
    [1317470938, 1800685478],
    [1800685728, 1800685889],
    [1800687617, 1800687836],
    [1800688579, 1800689093],
    [1800315633, 1800695235],
    [1800447586, 1800696465],
    [1800696134, 1800700253],
    [1788811750, 1800706533],
    [1787040343, 1800706788],
    [1760232522, 1800706955],
    [1799921007, 1800707073],
    [1800182685, 1800707249],
    [1799915054, 1800707266],
    [1797265764, 1800707500],
    [1799922169, 1800707775],
    [1773212597, 1800708051],
    [1684698681, 1800708094],
    [1785076917, 1800708241],
    [1779235822, 1800708755],
    [1800710412, 1800711639],
    [1791827492, 1800714158],
    [1728409881, 1800714615],
    [1773621503, 1800714804],
    [1683348279, 1800714810],
    [1774520933, 1800715005],
    [1603285048, 1800715355],
    [1791515754, 1800715396],
    [1787420418, 1800716655],
    [1808599893, 1808601232],
    [1808601448, 1808605491],
    [1808605643, 1808605732],
    [1787959183, 1800716976],
    [1796719955, 1800719857],
    [1796727841, 1800721860],
    [1800724701, 1800724755],
    [1800725033, 1800725301],
    [1796830960, 1800725895],
    [1800725919, 1800726014],
    [1800726050, 1800726177],
    [1685968205, 1800726380],
    [1800727203, 1800727309],
    [1800727500, 1800727601],
    [1800727674, 1800727970],
    [1800728094, 1800728224],
    [1560005564, 1800729441],
    [1800731618, 1800731751],
    [1800731908, 1800732191],
    [1800733304, 1800733443],
    [1800733599, 1800733671],
    [1800733779, 1800734191],
    [631574246, 1800733831],
    [1800735361, 1800735443],
    [1800735527, 1800735887],
    [1800735926, 1800736105],
    [1800736831, 1800737018],
    [1800737172, 1800739130],
    [1800738098, 1800739630],
    [1800740014, 1800740279],
    [1800740298, 1800740705],
    [1800741262, 1800741640],
    [1791997819, 1800743779],
    [1800747070, 1800747237],
    [1800747272, 1800747289],
    [1800747785, 1800747818],
    [1800747948, 1800748175],
    [1789259744, 1800754978],
    [1723662155, 1800757178],
    [1800352654, 1800768150],
    [1790797213, 1800768479],
    [1503030302, 1800776649],
    [1800776801, 1800776989],
    [1753996136, 1800777237],
    [1800788980, 1800789348],
    [1800789511, 1800791790],
    [1800803310, 1800806418],
    [1800796048, 1802023872],
    [1800803520, 1800803834],
    [1800804029, 1800804329],
    [1800803125, 1800804491],
    [1800804627, 1800804733],
    [1800804910, 1800805218],
    [1777113765, 1800807593],
    [1773658917, 1800811677],
    [1800810162, 1800810805],
    [1800811187, 1800811498],
    [1796844888, 1800815501],
    [1799863717, 1800819790],
    [1800815329, 1800827701],
    [1800827900, 1800827994],
    [1800815393, 1800828901],
    [1800829676, 1800829784],
    [1777211293, 1800847708],
    [1800830606, 1800831588],
    [1800832328, 1800833144],
    [1800833493, 1800833611],
    [1800834083, 1800835163],
    [1800836375, 1800836596],
    [1800838282, 1800838419],
    [1796973344, 1800839809],
    [1797037008, 1800841156],
    [1800841602, 1800843438],
    [1800843920, 1800843991],
    [1800844148, 1800846253],
    [1795256554, 1800841456],
    [1777213703, 1800845533],
    [1800845635, 1800847278],
    [1777211349, 1800850869],
    [1787900843, 1800849592],
    [1800850340, 1800850392],
    [1800850432, 1800850609],
    [1777206483, 1800853730],
    [1797003947, 1800853297],
    [1443035102, 1800853910],
    [1797008933, 1800854018],
    [1797021492, 1800854254],
    [1800855584, 1800855669],
    [1777213680, 1800858046],
    [1709644782, 1800857304],
    [1800857349, 1800857502],
    [1800857603, 1800858068],
    [1800858078, 1800865419],
    [1800858729, 1800858795],
    [1800859011, 1800859250],
    [1777212932, 1800860779],
    [1797084673, 1800860060],
    [1800860387, 1800860464],
    [1800860558, 1800861083],
    [1777214108, 1800863720],
    [1797337300, 1800862020],
    [1797328541, 1800863011],
    [1360521497, 1800864573],
    [1797359325, 1800863918],
    [1800865461, 1800865519],
    [1797359330, 1800863622],
    [1800863748, 1800863883],
    [1800864680, 1800865425],
    [1777208982, 1800866429],
    [1505428588, 1800866381],
    [1570447939, 1800866444],
    [1797366488, 1800866959],
    [1800867089, 1800867249],
    [1800867389, 1800867721],
    [1800867790, 1800871254],
    [1800871601, 1800872832],
    [1800873684, 1800874592],
    [1800875222, 1800879994],
    [1360521775, 1800868814],
    [1799344454, 1800868558],
    [1777207866, 1800869397],
    [1797523292, 1800868817],
    [1360521708, 1800871963],
    [1800871999, 1800872497],
    [1797427872, 1800870068],
    [1800870442, 1800870839],
    [1777212891, 1800870409],
    [1775149375, 1800871243],
    [1797504105, 1800872003],
    [1800872135, 1800872358],
    [1777214496, 1801119472],
    [1777210052, 1801120594],
    [1800872965, 1800873033],
    [1777206130, 1801121511],
    [1797455093, 1800873947],
    [1797137176, 1800874463],
    [1797498955, 1800874934],
    [1800875037, 1800875315],
    [1777211517, 1801122715],
    [1777216218, 1801124003],
    [1482759834, 1800877355],
    [1800877612, 1800878595],
    [1777209634, 1800877098],
    [1800877112, 1800877655],
    [1777205918, 1800877808],
    [1797510967, 1800877927],
    [1800878325, 1800878813],
    [1777210098, 1800878227],
    [1777216132, 1800878850],
    [1797517656, 1800879195],
    [1800879455, 1800880215],
    [1800880319, 1800880563],
    [1787684140, 1800881446],
    [1772187584, 1800880535],
    [1800880628, 1800881178],
    [1800881481, 1800883442],
    [1800883925, 1800885115],
    [1797218964, 1800881112],
    [1800881091, 1800881244],
    [1800881410, 1800881631],
    [1800830215, 1800885332],
    [1800413888, 1800882737],
    [1777749732, 1800882315],
    [1797542055, 1800882686],
    [1772189457, 1800883103],
    [1772186493, 1800883914],
    [1797547046, 1800885609],
    [1772184732, 1800884949],
    [1800884909, 1800885879],
    [1772187223, 1800885530],
    [1797549009, 1800885762],
    [1800885453, 1800886281],
    [1797570110, 1800887463],
    [1800887578, 1800887830],
    [1772611452, 1800887782],
    [1772187329, 1800888419],
    [1800427504, 1800889335],
    [1348471449, 1800891315],
    [1800891389, 1800894098],
    [1780708526, 1800889707],
    [1792620109, 1800897493],
    [1789948957, 1800896478],
    [1800903822, 1800904471],
    [1726450868, 1800906853],
    [1800909132, 1800910642],
    [1800910692, 1800911158],
    [1800912366, 1800913123],
    [1817429759, 1819530262],
    [1800915590, 1800918308],
    [1570637717, 1800915920],
    [1800727565, 1800917814],
    [1798145332, 1800917191],
    [1799209230, 1800917416],
    [1799225860, 1800917627],
    [1797113941, 1800917840],
    [1800920021, 1800923946],
    [1718181841, 1800921058],
    [1800921482, 1800921670],
    [1800921686, 1800922796],
    [1800922837, 1800922902],
    [1800923206, 1800923777],
    [1800925172, 1800932144],
    [1800925746, 1800925869],
    [1800925901, 1800926564],
    [1800926627, 1800927627],
    [1800860151, 1800928564],
    [1800928598, 1800928835],
    [1800929640, 1800930097],
    [1800930422, 1800931558],
    [1800931674, 1800934147],
    [1800943068, 1800944185],
    [1801148079, 1801157365],
    [1803623350, 1803665929],
    [1800929826, 1800931295],
    [1800199497, 1800934142],
    [1800934300, 1800935723],
    [1800936626, 1800938370],
    [1800938494, 1800939345],
    [1800918011, 1800934956],
    [1534148181, 1800935276],
    [1798737673, 1800940909],
    [1800941357, 1800943147],
    [1800943292, 1800944878],
    [1639462804, 1800941154],
    [1800893395, 1800982302],
    [1798744203, 1800947565],
    [1800948525, 1800950601],
    [1800951030, 1800951071],
    [1800153081, 1800954287],
    [1479229552, 1800954779],
    [1800954924, 1800955382],
    [1748037454, 1803397944],
    [1764784712, 1800958162],
    [1800958290, 1800959459],
    [1795834208, 1800958904],
    [782842318, 1800965465],
    [225451178, 1800966637],
    [1764784635, 1800967971],
    [1410641685, 1800970728],
    [1795835724, 1800968769],
    [1564984967, 1800974457],
    [945134717, 1800975268],
    [309946514, 1800976187],
    [309943796, 1800977015],
    [1800976507, 1800976677],
    [1800976716, 1800976754],
    [1800976825, 1800977161],
    [1800977282, 1800977746],
    [922842077, 1800978325],
    [309891443, 1800979588],
    [938529024, 1800980362],
    [309891905, 1800981660],
    [1792417096, 1800982469],
    [309882849, 1800983251],
    [309866476, 1800984178],
    [309866258, 1800985474],
    [309842938, 1800986449],
    [937781867, 1800987661],
    [1800987118, 1800987263],
    [1800987373, 1800987565],
    [309828704, 1800988515],
    [938509229, 1800989392],
    [1423438074, 1800993318],
    [1800989254, 1800989608],
    [938582644, 1800990311],
    [309779429, 1800991889],
    [1053782401, 1800992668],
    [1053782360, 1800993415],
    [1575491952, 1800993833],
    [922849704, 1800994896],
    [1799648093, 1800994697],
    [936934018, 1800995569],
    [1752976000, 1800996663],
    [1053781514, 1800996159],
    [921431159, 1800997103],
    [1755941936, 1800997164],
    [1517936288, 1800997398],
    [1576371813, 1800997546],
    [309769419, 1800998264],
    [1519065778, 1800997939],
    [1746500574, 1800998393],
    [1559107722, 1800998452],
    [1797614076, 1800998584],
    [1800998773, 1800999002],
    [1800999044, 1800999266],
    [1800999453, 1800999594],
    [1800999719, 1801000425],
    [309750011, 1800999150],
    [1656428600, 1800999981],
    [938539711, 1801000967],
    [1796950285, 1801000721],
    [1797630707, 1801000848],
    [309731298, 1801001652],
    [1797632749, 1801001332],
    [1801001455, 1801050363],
    [309725709, 1801002404],
    [939754284, 1801003073],
    [937699563, 1801003657],
    [1801002022, 1801003242],
    [939584990, 1801004262],
    [937680697, 1801005072],
    [309722485, 1801006763],
    [937631073, 1801007313],
    [938061995, 1801008157],
    [937707084, 1801008968],
    [309712044, 1801009755],
    [360362154, 1801010793],
    [309684437, 1801011674],
    [309683033, 1801012448],
    [939587861, 1801012978],
    [309679615, 1801015650],
    [1754439715, 1812851074],
    [866374532, 1801016973],
    [938478462, 1801017550],
    [866372257, 1801018342],
    [309666517, 1801019519],
    [1792837037, 1801019779],
    [1801020171, 1801020727],
    [309660464, 1801020943],
    [1800922233, 1801021023],
    [1441136384, 1801047461],
    [939848059, 1801021755],
    [852376133, 1801022891],
    [309638866, 1801023909],
    [938045421, 1801024807],
    [1801024999, 1801025170],
    [1801025230, 1801025257],
    [1801026043, 1801026232],
    [1801026402, 1801027113],
    [1686578605, 1801026028],
    [1796906500, 1801026997],
    [309624241, 1801027875],
    [939628600, 1801028535],
    [1801027644, 1801029046],
    [1801029504, 1801322740],
    [1802454960, 1802622790],
    [981085821, 1801029350],
    [972134756, 1801030134],
    [921723979, 1801031361],
    [921940350, 1801032461],
    [309609923, 1801033639],
    [309605048, 1801034449],
    [309599759, 1801035353],
    [1791568374, 1801035591],
    [309586759, 1801036157],
    [922587387, 1801038194],
    [1801036618, 1801038225],
    [1801038711, 1801318794],
    [1713433564, 1801037107],
    [1672270266, 1801037416],
    [309576699, 1801039438],
    [309564501, 1801040633],
    [1787870151, 1801040423],
    [927316682, 1801041907],
    [309525714, 1801043554],
    [939846067, 1801044569],
    [309508668, 1801045613],
    [1749218767, 1801046095],
    [309502185, 1801046563],
    [1686578476, 1801050247],
    [1360521929, 1801050795],
    [1801051047, 1801054813],
    [938821395, 1801051101],
    [1797635324, 1801050896],
    [1797688992, 1801051826],
    [937640062, 1801054359],
    [309472822, 1801055563],
    [938683589, 1801056366],
    [939513621, 1801056963],
    [309445229, 1801057958]
]


def test_bulk():
    import time
    for (i, j) in DIFFS:
        print(i, j)
        diff = get_diff(i, j)
        if diff:
            diff.changes()
        time.sleep(0.5)
