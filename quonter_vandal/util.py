from itertools import zip_longest
from typing import List, Tuple  # for Python 3.x


def grouper(n, iterable) -> List[Tuple]:
    res = list(zip_longest(*[iter(iterable)]*n, fillvalue=None))
    if not res:
        return []
    res[-1] = tuple(filter(lambda x: x is not None, res[-1]))
    return res


def clip_list(l: List, n: int) -> List:
    if len(l) <= n:
        return l
    return l[:n]
