from itertools import groupby


def grouped(iterable, key):
    return groupby(sorted(iterable, key=key), key=key)


def unique(iterable):
    return [i for n, i in enumerate(iterable) if i not in iterable[n + 1:]]