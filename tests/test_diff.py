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


DIFFS = [
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
    [1838959194, 1863121443],
    [1786267319, 1831665948],
    [1816162621, 1831898672],
    [1365665665, 1831921535],
    [1813357669, 1831961359],
    [1834337741, 1836028013],
    [1913178355, 1913308189],
    [1817754583, 1818569034],
    [1831961719, 1831961763],
    [1832483740, 1832496158],
    [1833538468, 1834190747],
    [1834336441, 1836028815],
    [1871240301, 1871528399],
    [1875773457, 1877328901],
    [1879161335, 1880999701],
    [1881999277, 1909243630],
    [1913177182, 1913308967],
    [1813201784, 1818569856],
    [1818835628, 1830533803],
    [1831959573, 1831962154],
    [1832483857, 1832495627],
    [1832605556, 1833524323],
    [1833538294, 1834190476],
    [1834336155, 1836028160],
    [1871239833, 1871528562],
    [1873402997, 1875488201],
    [1875774381, 1877328796],
    [1879144576, 1880999871],
    [1882943577, 1909243025],
    [1913177741, 1913308408],
    [1915133354, 1916940352],
    [1786223550, 1831986119],
    [1869219493, 1904035853],
    [1904169829, 1924311241],
    [1831299925, 1832009056],
    [1832195169, 1832195513],
    [1832372900, 1832373138],
    [1832336840, 1832503158],
    [1832571324, 1832571859],
    [1832604381, 1832638407],
    [1833538020, 1834190947],
    [1834536756, 1836028382],
    [1864723677, 1867024741],
    [1871239465, 1871528704],
    [1875772122, 1877329350],
    [1879162890, 1880999159],
    [1881998948, 1909243170],
    [1818319757, 1818347991],
    [1830212868, 1830234049],
    [1832546661, 1911058656],
    [1827339959, 1832768503],
    [1823720529, 1832768980],
    [1832962519, 1832967730],
    [1808999960, 1833094512],
    [1769543383, 1833122255],
    [1798742807, 1833143049],
    [1814296840, 1833294625],
    [1814722334, 1833437382],
    [1530182398, 1833503181],
    [1371393376, 1833549174],
    [1788158782, 1833533634],
    [1848942581, 1854915127],
    [1862833482, 1888181725],
    [1743920161, 1833626191],
    [1826792540, 1833695431],
    [1775210053, 1834663759],
    [1833759541, 1876864034],
    [1786627241, 1839304180],
    [1397916330, 1833795253],
    [1828827543, 1833851736],
    [1797079164, 1804821352],
    [1805531994, 1807425473],
    [1807856206, 1808412940],
    [1808503959, 1809513906],
    [1809520465, 1828625546],
    [1828971679, 1830046627],
    [1830047735, 1833451202],
    [1833726384, 1833865367],
    [1845831623, 1846885910],
    [1859208041, 1859921784],
    [1894538864, 1898545301],
    [1911016469, 1911325868],
    [1916044984, 1916779328],
    [1827628433, 1833964152],
    [1867875607, 1869811285],
    [1680340576, 1833967315],
    [1826922366, 1833969095],
    [1722868212, 1833971729],
    [1717833315, 1834016786],
    [1768171508, 1834063068],
    [1807304233, 1834079922],
    [1865116911, 1899485423],
    [1815228763, 1834134981],
    [1813200611, 1813342304],
    [1817325575, 1834191465],
    [1913180162, 1913307678],
    [1683474559, 1834410184],
    [1775117748, 1834452990],
    [1762507605, 1834475349],
    [1831733409, 1834588869],
    [1586423146, 1834609209],
    [1833365382, 1834643932],
    [1826088010, 1834646789],
    [1806356719, 1817518014],
    [1828223975, 1834655668],
    [1867486164, 1868842749],
    [1868889209, 1872580430],
    [1872591224, 1873197681],
    [1883119979, 1889943265],
    [1924893028, 1925491935],
    [1785400206, 1858462385],
    [1834683937, 1834684608],
    [767781705, 1834712836],
    [767775963, 1834714634],
    [1782291985, 1834917059],
    [1714194596, 1834922904],
    [1832821728, 1834923169],
    [1834944868, 1834945356],
    [1858247113, 1865260902],
    [1866238562, 1874087786],
    [1664398060, 1835002300],
    [1834590990, 1835022048],
    [1829733457, 1835063032],
    [1826816827, 1835065660],
    [1835066133, 1835067370],
    [1817770385, 1835071140],
    [1842596285, 1854207749],
    [1854402733, 1855905490],
    [1816711175, 1835091505],
    [1834648168, 1835098536],
    [1569652875, 1835110160],
    [1812763929, 1835137383],
    [1791589611, 1835178293],
    [1796315600, 1835229763],
    [1833521522, 1835234286],
    [1738057168, 1835284563],
    [1681313437, 1835298650],
    [1554063051, 1835299777],
    [1819331523, 1835324677],
    [1817604432, 1835327423],
    [1779064162, 1835340339],
    [1808424490, 1813203722],
    [1834244757, 1835344269],
    [1913744607, 1914285873],
    [1923698831, 1924249823],
    [1778596104, 1835345368],
    [1820729693, 1835369040],
    [1588565282, 1835371124],
    [1757339702, 1835375998],
    [1511560068, 1835387352],
    [1825392770, 1835412653],
    [1834390025, 1835456769],
    [941875044, 1835505625],
    [1784964910, 1835552067],
    [1829339111, 1835563280],
    [1830794660, 1835605515],
    [1809360282, 1835634715],
    [1835716670, 1835716674],
    [1724160946, 1835740208],
    [1829782493, 1835743204],
    [1822091113, 1835836548],
    [1790885766, 1835897873],
    [1692773110, 1857948463],
    [1857970481, 1858073220],
    [1913623150, 1929951480],
    [1761444944, 1835924435],
    [1813202085, 1813341792],
    [1813346637, 1813352834],
    [1831676670, 1831959736],
    [1833538340, 1834190564],
    [1834337201, 1836028273],
    [1871239567, 1871528654],
    [1873403846, 1875487922],
    [1875772927, 1877328943],
    [1879162530, 1880999305],
    [1913178143, 1913308297],
    [1813201152, 1813343922],
    [1813360209, 1818569429],
    [1830373005, 1831959165],
    [1833538594, 1834190357],
    [1834336286, 1836029132],
    [1864722414, 1867024295],
    [1871240001, 1871528466],
    [1873403590, 1875487981],
    [1875772702, 1877329030],
    [1879144680, 1880999753],
    [1881999445, 1909243742],
    [1913177331, 1913308863],
    [1831628435, 1836105160],
    [1861042551, 1895248697],
    [1825641930, 1869592600],
    [1870509320, 1872517861],
    [1826976883, 1836205850],
    [1787663271, 1836224946],
    [1836301870, 1836302960],
    [1565679442, 1836359592],
    [1836410953, 1836410961],
    [1761436976, 1836450581],
    [1781809575, 1862942462],
    [1833447606, 1836483816],
    [1835758203, 1836588640],
    [1830630392, 1836636355],
    [1712636170, 1836652054],
    [1782179927, 1836934578],
    [1862475048, 1862655001],
    [1789599075, 1837004078],
    [1787171876, 1837036751],
    [1811513645, 1837069918],
    [1877945196, 1878804564],
    [1767856023, 1837138254],
    [1817894529, 1837160191],
    [1787149041, 1837186491],
    [1796030462, 1844057601],
    [1572123679, 1837245508],
    [1824646888, 1837300593],
    [1829696130, 1837339781],
    [1837340044, 1839711206],
    [1791254127, 1837393351],
    [1420787049, 1837504519],
    [1826609348, 1837561505],
    [1699015236, 1837612383],
    [1804175046, 1847314430],
    [1810121423, 1837971773],
    [1836112677, 1838034825],
    [1848685158, 1851394895],
    [1894165335, 1901254164],
    [1813276101, 1838114264],
    [1746334864, 1838126162],
    [1372716889, 1838126594],
    [1838141723, 1838216684],
    [1747008787, 1838236382],
    [1796390552, 1838378778],
    [1838390016, 1838390176],
    [1373464266, 1838462419],
    [1793740221, 1838477068],
    [1731837326, 1838527647],
    [1683334928, 1838554891],
    [1625373907, 1838562285],
    [1829916368, 1838580071],
    [1565320691, 1838592171],
    [1710585218, 1838592364],
    [1719747949, 1838609758],
    [1834058228, 1838631136],
    [1823484735, 1838643222],
    [1725550050, 1838792112],
    [1826572966, 1838837540],
    [1765212474, 1838839698],
    [1717953915, 1838890171],
    [1831243481, 1838989116],
    [1839157501, 1839157778],
    [1819629054, 1839189975],
    [1884172573, 1910151579],
    [1812444406, 1839238756],
    [1639661290, 1839281645],
    [1839283975, 1870142605],
    [1886241108, 1898714606],
    [1821266200, 1839284247],
    [1773780720, 1839322627],
    [1827963999, 1839329300],
    [1839391508, 1839870886],
    [1839969302, 1846939689],
    [1839347858, 1839348444],
    [1834518055, 1839382725],
    [1788279977, 1839387216],
    [1716899122, 1839426933],
    [1836579588, 1839631924],
    [1828251097, 1839689688],
    [1839710465, 1839713099],
    [1813554768, 1839713138],
    [1839788491, 1839788589],
    [1799509639, 1839812003],
    [1839849137, 1839849369],
    [1693010256, 1839946843],
    [1550868529, 1839962873],
    [1656934260, 1839971782],
    [1824617212, 1839971986],
    [1585874840, 1840047068],
    [1837397902, 1840276484],
    [1377115542, 1840333523],
    [1763816141, 1840458855],
    [1804442569, 1840469159],
    [1866790715, 1868367777],
    [1781732043, 1840482261],
    [1681928186, 1840705177],
    [1743024870, 1840737822],
    [1830385468, 1840761563],
    [1738980073, 1814691362],
    [1836032474, 1840764456],
    [958451062, 1840835007],
    [1840834513, 1840837914],
    [1837250773, 1840892239],
    [1840892014, 1840892888],
    [1818794138, 1840963348],
    [1753629647, 1841153573],
    [1797018497, 1878809583],
    [1794698640, 1841394432],
    [1794743965, 1809333704],
    [1823278917, 1823642460],
    [1826268431, 1832184102],
    [1832475695, 1833437850],
    [1835140725, 1841177707],
    [1841411046, 1841411566],
    [1841426219, 1841518418],
    [1851292344, 1855926821],
    [1893103747, 1896287319],
    [1900753863, 1901669911],
    [1902496454, 1906742359],
    [1918165249, 1924045317],
    [1924890143, 1925721609],
    [1727805570, 1841502321],
    [1801911621, 1841589559],
    [1668809444, 1841667880],
    [1828162053, 1841675358],
    [1734987696, 1841682302],
    [1519555035, 1841801725],
    [1776250700, 1841892151],
    [1177512094, 1841896279],
    [1351876362, 1841904505],
    [1813693363, 1841915419],
    [1821118308, 1841946110],
    [1841563460, 1841984501],
    [1803898236, 1842018885],
    [1532235310, 1842057155],
    [1763646346, 1842065295],
    [1788242454, 1842103607],
    [1867456213, 1908219674],
    [1779745208, 1842104281],
    [1830912310, 1842127800],
    [1755193970, 1913206704],
    [1836393585, 1842325730],
    [1834146346, 1842346647],
    [1797779451, 1842419355],
    [1682955560, 1842446819],
    [1831718534, 1900967579],
    [1818486472, 1819683087],
    [1832301361, 1842493773],
    [1852039006, 1864335328],
    [1891805388, 1893583646],
    [1896544982, 1896818121],
    [1824151189, 1832834228],
    [1832864349, 1835514132],
    [1835876884, 1838882516],
    [1838893915, 1842261682],
    [1842267818, 1842505060],
    [1007227119, 1842562756],
    [1830497685, 1842563392],
    [1564350094, 1842585436],
    [1809340986, 1842645358],
    [1842686692, 1842687074],
    [1787509458, 1803202707],
    [1834867024, 1837327287],
    [1841737542, 1842740185],
    [1754084255, 1842749720],
    [1842823161, 1842823202],
    [1801017205, 1842835521],
    [1842359239, 1842835756],
    [1799963345, 1842855953],
    [1771359105, 1842863036],
    [1810080731, 1833596448],
    [1835538737, 1842871773],
    [1843729890, 1846909880],
    [1911566361, 1921643442],
    [1793816612, 1842878877],
    [1723614801, 1822159383],
    [1827517788, 1828688784],
    [1832849875, 1833494930],
    [1843012526, 1870123111],
    [1683739328, 1843022489],
    [1781976234, 1843079620],
    [1693697535, 1843084495],
    [1794231076, 1846325831],
    [1860401189, 1889064623],
    [1789137480, 1843172311],
    [1819329912, 1837069530],
    [1840891572, 1863670226],
    [1865238970, 1885970946],
    [1898528271, 1906730062],
    [1791121328, 1843222511],
    [1801069889, 1843224519],
    [1779204186, 1843325867],
    [1825119514, 1843392184],
    [1616514956, 1843433148],
    [1790983758, 1843511828],
    [1838916786, 1843567703],
    [1811243871, 1843594520],
    [1843152997, 1843648146],
    [1810883726, 1843727828],
    [1532615664, 1868285888],
    [1811099395, 1843873598],
    [1833513037, 1843959915],
    [1641266740, 1843962431],
    [1827974648, 1831072698],
    [1842069484, 1843580081],
    [1843658719, 1843993157],
    [1812692744, 1843989572],
    [1651012891, 1844059645],
    [1832233904, 1844129354],
    [1693923446, 1844132712],
    [1839514271, 1844201637],
    [1882975352, 1900534684],
    [1900686578, 1900943992],
    [1901002775, 1902448174],
    [1904695381, 1904699160],
    [1749519796, 1844208546],
    [1828972057, 1844320715],
    [1827478163, 1844348987],
    [1579686667, 1844358570],
    [1789405683, 1844368679],
    [1736505311, 1844378211],
    [1714569689, 1844387611],
    [1790748519, 1814459287],
    [1826599765, 1874787317],
    [1399709533, 1844411470],
    [1773753951, 1844451265],
    [1844273101, 1844468495],
    [1835058288, 1844470336],
    [1896668489, 1900192708],
    [1900398281, 1913269379],
    [1843483940, 1844539226],
    [1813439666, 1904638674],
    [1832452152, 1839759215],
    [1839769015, 1844495773],
    [1844571392, 1844791866],
    [1781979464, 1844729290],
    [1844739202, 1844739258],
    [1550396662, 1844764481],
    [1844319976, 1844778137],
    [1675003331, 1844805225],
    [1774243160, 1844810043],
    [1840878693, 1844820928],
    [1852449780, 1856240453],
    [1778855922, 1834043281],
    [1834118531, 1872152674],
    [1550363960, 1844922350],
    [1823829781, 1844931350],
    [1844931184, 1870542906],
    [1832725767, 1844993350],
    [1828113163, 1845001905],
    [1825696013, 1894712288],
    [733330772, 1845050766],
    [1651587755, 1845057085],
    [1767006532, 1845063988],
    [1840427988, 1845081475],
    [1841064742, 1845090527],
    [1730038711, 1845104048],
    [1839930412, 1845134874],
    [1347197351, 1845062269],
    [1845230233, 1845432926],
    [1299751265, 1845433317],
    [1380038435, 1845436514],
    [1795518473, 1845465514],
    [1842715338, 1845472733],
    [1840662631, 1845490839],
    [1811860603, 1845530900],
    [1319891518, 1845549597],
    [1319891509, 1845550209],
    [1836503940, 1845566672],
    [1669649780, 1845617916],
    [1750869600, 1845619356],
    [1835534560, 1845660358],
    [1683627103, 1855579897],
    [1839125506, 1845674112],
    [1828380956, 1838997491],
    [1843593319, 1884448500],
    [1826587142, 1845844586],
    [1845899162, 1845899268],
    [1717915204, 1845917767],
    [1842399999, 1845948665],
    [1842399889, 1845949305],
    [1774142641, 1846002922],
    [1826636882, 1846025864],
    [1867541267, 1869743834],
    [1876522667, 1879044709],
    [1639410555, 1846069742],
    [1785535084, 1846079368],
    [1835814381, 1846104933],
    [1846126659, 1846141510],
    [1824025023, 1846196531],
    [1842954706, 1846212177],
    [1833562029, 1846219226],
    [1853726932, 1857563931],
    [1870098474, 1910702622],
    [1825178900, 1846242247],
    [1812030038, 1846268102],
    [1844904163, 1846359214],
    [1755884923, 1846362577],
    [1780327641, 1846413300],
    [1800572133, 1843815366],
    [1843916998, 1846443291],
    [1843183076, 1846455425],
    [1587082421, 1846500751],
    [1845206525, 1851179427],
    [1748291035, 1846523323],
    [1674934929, 1846528170],
    [1338109651, 1846639386],
    [1832032826, 1846643498],
    [1738403308, 1846662413],
    [1838659853, 1846670892],
    [1873692714, 1878016616],
    [1825813034, 1846689514],
    [1831452504, 1846686649],
    [1689052415, 1846855376],
    [1831438352, 1846869121],
    [1792876055, 1846926223],
    [1509956739, 1846944923],
    [1833452881, 1846969164],
    [1896141282, 1918574044],
    [1760304177, 1871612122],
    [1897211342, 1897797805],
    [1903355244, 1908917893],
    [1790966740, 1847061916],
    [1769654510, 1847178873],
    [1812892682, 1847196748],
    [1859287759, 1888084051],
    [1834511170, 1847200803],
    [1870161938, 1901830826],
    [1826347367, 1845425649],
    [1845454117, 1847203490],
    [1855170910, 1870150615],
    [1783397819, 1847212255],
    [1420878675, 1847232432],
    [1798598676, 1847232848],
    [1845724488, 1846527606],
    [1846531595, 1846631168],
    [1846650998, 1846835360],
    [1846835945, 1847257278],
    [1805551225, 1806694094],
    [1807531846, 1814145593],
    [1814665106, 1829000191],
    [1839207018, 1842720870],
    [1843034383, 1847335482],
    [1846775734, 1852002566],
    [1821153395, 1847394500],
    [1771642583, 1847452203],
    [1839337821, 1847453222],
    [1860198676, 1899354191],
    [1899774097, 1900573326],
    [1840747725, 1847477472],
    [1590224364, 1847503602],
    [1830394975, 1842417965],
    [1843068860, 1847522836],
    [1847705020, 1853814028],
    [1854853938, 1871950430],
    [1876445682, 1924940930],
    [1836114193, 1847552383],
    [1719551019, 1847645105],
    [1742029278, 1809501940],
    [1817701740, 1849963319],
    [1850108187, 1904739243],
    [1411834615, 1847709495],
    [1497278521, 1847716125],
    [1686304883, 1847731856],
    [1833829376, 1853629470],
    [1568229111, 1847884534],
    [1827451403, 1847927379],
    [1847935858, 1847938047],
    [1789420563, 1847958461],
    [1846442162, 1847974172],
    [1875887842, 1892768933],
    [1834705610, 1847992625],
    [1876269089, 1877610995],
    [1844630640, 1847254214],
    [1847284826, 1848020483],
    [1848025439, 1848025784],
    [1787176502, 1848026511],
    [1848065218, 1848099853],
    [1789214346, 1848209098],
    [1745683558, 1848277786],
    [1790712291, 1870570415],
    [1800025532, 1848570785],
    [1845963109, 1848730152],
    [1835072049, 1848749799],
    [1839396607, 1848759539],
    [1843139558, 1848910036],
    [1847199417, 1847936933],
    [1847937034, 1847937197],
    [1848611687, 1848930061],
    [1848942580, 1848943031],
    [1857862119, 1894139879],
    [1894369983, 1899001358],
    [1843254371, 1848951048],
    [1571936085, 1848969633],
    [1658322262, 1848972901],
    [1836347409, 1848975080],
    [1589282741, 1849271866],
    [1756011976, 1849452348],
    [1836547898, 1850348388],
    [1849713792, 1849714247],
    [1741113942, 1849813743],
    [1807287283, 1849984369],
    [1805761156, 1807721906],
    [1807792588, 1811248494],
    [1848847335, 1850010602],
    [1913558673, 1913857028],
    [1717768945, 1850038000],
    [1838755739, 1850185538],
    [1822912498, 1850217075],
    [1730330935, 1850235097],
    [1726159563, 1850364347],
    [1794984102, 1809307371],
    [1809318720, 1810164549],
    [1810352644, 1813971946],
    [1848831526, 1850381872],
    [1873683784, 1874759923],
    [1913648101, 1914342071],
    [1918877853, 1918879097],
    [1811023730, 1850430291],
    [1847664174, 1850466496],
    [1790938848, 1813948492],
    [1820740685, 1850674632],
    [1850675738, 1850677054],
    [1877262628, 1886710614],
    [1826529852, 1851018925],
    [1888385262, 1893066530],
    [1839755900, 1839758332],
    [1840018887, 1851171168],
    [1824965933, 1851180615],
    [1851387407, 1851388858],
    [1585882504, 1851389062],
    [1766742617, 1851437636],
    [1827215698, 1851460241],
    [1747486883, 1851496947],
    [1806501340, 1824732438],
    [1824769525, 1834461086],
    [1834476691, 1869780796],
    [1851535688, 1851537047],
    [1531027314, 1851573105],
    [1799427131, 1851579466],
    [1768544576, 1831919331],
    [1832302192, 1851709322],
    [1695379305, 1831919120],
    [1832302213, 1851709606],
    [1695379312, 1831919571],
    [1832302139, 1851709857],
    [1831205163, 1831205404],
    [1839915346, 1851710821],
    [1852845228, 1887818629],
    [1778642369, 1851736764],
    [1852090550, 1852091038],
    [1852719682, 1852721058],
    [1852724997, 1854221131],
    [1854222658, 1875630199],
    [1875634173, 1882734800],
    [1882876726, 1883007667],
    [1883010787, 1884193460],
    [1884194401, 1884195106],
    [1884195410, 1884196315],
    [1884197603, 1884198167],
    [1821353152, 1851999541],
    [1785074215, 1852005837],
    [1848868962, 1852020478],
    [1151548563, 1852046262],
    [1846536300, 1852075461],
    [1894361705, 1894361828],
    [1851613679, 1852099410],
    [1842248348, 1846169438],
    [1846323711, 1852134973],
    [1884157571, 1897938073],
    [1852154232, 1852154336],
    [1850750425, 1856672380],
    [1895563917, 1898247689],
    [1822348895, 1852175709],
    [1829288363, 1840640074],
    [1840681714, 1846851755],
    [1846856724, 1852212150],
    [1850243873, 1852210914],
    [1851509325, 1852235754],
    [1852343575, 1901212043],
    [1902307445, 1924059404],
    [1810966932, 1872013722],
    [1892011248, 1904770529],
    [1904776745, 1910939217],
    [1828614981, 1839430867],
    [1839530935, 1847663391],
    [1847682909, 1848388509],
    [1852172434, 1852434169],
    [1793107219, 1920888845],
    [1775238079, 1852593218],
    [1665959501, 1852612558],
    [1818544789, 1820312079],
    [1836426349, 1852810840],
    [1899318495, 1906581591],
    [1906869895, 1911167887],
    [1838856756, 1852643926],
    [1817457165, 1852663322],
    [1792401823, 1852704537],
    [1840086217, 1886797023],
    [1852763752, 1852769772],
    [1843455229, 1852874803],
    [1849893639, 1853008952],
    [1855135055, 1866960444],
    [1882022553, 1885881707],
    [1895811267, 1896839680],
    [1841184509, 1857852882],
    [1848846478, 1853362005],
    [1844960481, 1853463165],
    [1891470981, 1896146625],
    [1812520696, 1853464465],
    [1803799215, 1819654103],
    [1839169287, 1847917221],
    [1853471318, 1853471657],
    [1773077202, 1853497578],
    [1828043495, 1906719791],
    [1742987606, 1853545730],
    [1884109322, 1884256278],
    [1891108202, 1896605950],
    [1810676531, 1887258477],
    [1826272191, 1890825725],
    [1813374072, 1853619412],
    [1537462701, 1853663646],
    [1852773092, 1854263925],
    [1853830275, 1853830282],
    [1269610834, 1853869904],
    [1779870659, 1839793346],
    [1839832250, 1853891689],
    [1779901231, 1853901351],
    [1772698669, 1854124526],
    [1854175687, 1854195042],
    [1854389860, 1854389997],
    [1833825163, 1854404047],
    [1845240159, 1854529051],
    [1779224263, 1854565651],
    [1841513344, 1854574638],
    [1844001130, 1854683682],
    [1854753398, 1854753480],
    [1846291389, 1854863498],
    [1772265215, 1854912598],
    [1843546780, 1854966433],
    [1650635384, 1855020321],
    [1835906282, 1855021608],
    [1890296756, 1896746307],
    [1851688470, 1855074258],
    [1718342219, 1839887506],
    [1839949702, 1858587358],
    [1853509343, 1854161847],
    [1855126256, 1855126409],
    [1899165263, 1899165354],
    [1899165643, 1899165873],
    [1792779564, 1855127149],
    [1820457738, 1826368408],
    [1835861596, 1855160522],
    [1846258266, 1855161561],
    [1866714138, 1875137163],
    [1844098220, 1855174460],
    [1855204487, 1855204671],
    [1855323739, 1855323885],
    [1831116193, 1855354151],
    [1834087810, 1855462635],
    [1711692166, 1855471839],
    [1804357947, 1855475704],
    [1830779193, 1855500042],
    [1841912435, 1855625289],
    [1854130692, 1855643412],
    [1810783474, 1855834469],
    [1488293729, 1856164983],
    [1755543222, 1856365212],
    [1656965628, 1856466330],
    [1724144910, 1856491363],
    [1824104027, 1856499009],
    [1848909781, 1856512239],
    [1873646211, 1886878310],
    [1896035707, 1897939065],
    [1764148931, 1856573737],
    [1811245371, 1856782196],
    [1733958882, 1856816542],
    [1588344817, 1857133259],
    [1649812864, 1857149035],
    [1630613587, 1857209199],
    [1839280820, 1857236578],
    [1809340254, 1857289244],
    [1830184570, 1854170567],
    [1854298165, 1857295932],
    [1913680037, 1927977799],
    [1747285755, 1857365025],
    [1541090201, 1857367652],
    [1851689667, 1857391997],
    [1803202337, 1857423695],
    [1841868442, 1857449589],
    [1826935363, 1857534128],
    [1377494805, 1857665041],
    [1592504039, 1857779844],
    [1732228421, 1857893197],
    [1816043566, 1819006982],
    [1853438765, 1854210747],
    [1854253839, 1879024501],
    [1895381004, 1898551853],
    [1821194487, 1857940793],
    [1755169241, 1882788223],
    [1314719862, 1858023219],
    [1794124746, 1858031344],
    [1839834366, 1858046036],
    [1786949361, 1858087746],
    [1848172710, 1858128318],
    [1827136861, 1858146595],
    [1740988114, 1858192505],
    [1747028025, 1858341710],
    [1688622107, 1858355558],
    [1862415426, 1894938009],
    [1747665700, 1858372467],
    [1810817112, 1858376977],
    [1609019249, 1858402320],
    [1466840278, 1858442038],
    [1858638626, 1858638773],
    [1703923755, 1858647749],
    [1766931247, 1858647944],
    [1843565148, 1876420208],
    [1390274769, 1858683439],
    [1828692171, 1874687979],
    [1798916947, 1858885026],
    [1513743262, 1858895977],
    [1791754479, 1896850278],
    [1858240096, 1881550971],
    [1858693127, 1859036429],
    [1637278053, 1859104742],
    [1781459305, 1859181695],
    [1859195624, 1859195809],
    [1726011184, 1859262586],
    [1710633530, 1859324378],
    [1775913472, 1859339676],
    [1724806089, 1859342988],
    [1828847004, 1859636980],
    [1862978180, 1878871640],
    [1850515452, 1859687486],
    [1817321946, 1819626833],
    [1849158748, 1859758221],
    [1859797917, 1882936842],
    [1841957917, 1859854209],
    [1783918014, 1859896359],
    [1763205173, 1859911447],
    [1859961836, 1859962404],
    [1824791374, 1860114209],
    [1792325330, 1825469962],
    [1858139932, 1874194656],
    [1850834754, 1860144354],
    [1851101151, 1860171711],
    [1789252441, 1826861375],
    [1834527579, 1860213374],
    [1858934490, 1860371104],
    [1859742203, 1860467192],
    [1860000047, 1860473698],
    [1846674112, 1860500582],
    [1774908566, 1860758401],
    [1832445819, 1860774497],
    [1860769681, 1860774513],
    [1860779629, 1860782441],
    [1895913310, 1906665063],
    [1854884611, 1860917430],
    [1859856454, 1861008973],
    [1791117380, 1861108976],
    [1898795223, 1898795227],
    [1623506862, 1861184305],
    [1847800939, 1861252613],
    [1807522006, 1821538845],
    [1858751092, 1861290818],
    [1861300844, 1861305716],
    [1861306302, 1861306638],
    [1596369044, 1861375839],
    [1858951269, 1861379717],
    [1858950985, 1910976628],
    [1812517887, 1861446202],
    [1861757445, 1861757842],
    [1832064836, 1861938428],
    [1858457224, 1862000927],
    [1882014143, 1886748916],
    [1688911356, 1862314926],
    [1827812374, 1862336323],
    [1841507261, 1862427031],
    [1807658988, 1875768937],
    [1889283749, 1889285794],
    [1862597258, 1862597491],
    [1842031778, 1862687775],
    [1750346353, 1862758528],
    [1756172006, 1862906320],
    [1811173303, 1862948032],
    [1847837166, 1864292326],
    [1857036597, 1862961567],
    [1862919000, 1862967394],
    [1422086174, 1863064240],
    [1857558597, 1862487436],
    [1862592659, 1863128200],
    [1716346750, 1863131417],
    [1824613064, 1831313315],
    [1831606907, 1914575436],
    [1731186343, 1863166996],
    [1640876004, 1863232639],
    [1859196502, 1863234051],
    [1851385043, 1863291749],
    [1773996031, 1863376126],
    [1809027473, 1863432856],
    [1851458188, 1863588702],
    [1855115534, 1863710302],
    [1824460852, 1863729626],
    [1862329663, 1863836715],
    [1828704451, 1836050428],
    [1862021423, 1911522772],
    [1795948661, 1863903974],
    [1863987392, 1906821936],
    [1845755771, 1864094404]
]


def test_bulk():
    import time
    for (i, j) in DIFFS:
        print(i, j)
        diff = get_diff(i, j)
        if diff:
            diff.changes()
        time.sleep(0.5)
