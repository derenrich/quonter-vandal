from quonter_vandal.revision_listing import get_revisions


def test_get_revisions():
    title = "Q28587782"
    rvstartid = 1942074309
    rvendid = 1419596909
    revisions = get_revisions(title, rvstartid, rvendid)
    assert (len(revisions) == 2)
    assert (revisions[0].user == "BrokenSegue")
    assert (revisions[0].timestamp == "2023-07-29T00:49:15Z")
    assert (revisions[0].comment ==
            "/* wbsetaliases-add:1|en */ legal challenge to Executive Order 13769")
    assert (revisions[0].tags == ["wikidata-ui"])

    assert (revisions[1].user == "BrokenSegue")
    assert (revisions[1].timestamp == "2023-07-29T00:49:14Z")
    assert (revisions[1].comment ==
            "/* wbsetlabel-set:1|en */ legal challenges to the Trump travel ban")
    assert (revisions[1].tags == ["wikidata-ui"])
