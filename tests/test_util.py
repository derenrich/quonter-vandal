from quonter_vandal.util import grouper


def test_grouper():
    res = grouper(3, list(range(10)))
    assert len(res) == 4
    assert list(res) == [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9,)]

    res = grouper(2, list(range(10)))
    assert len(res) == 5
    assert list(res) == [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]
