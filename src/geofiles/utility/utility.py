from typing import Iterable


def pairwise(iterable: Iterable):
    """
    Method for a pairwise access of an iterable
    :param iterable: to be iterated
    :returns: (x, y) pairs of iterable
    """

    a = iter(iterable)
    return zip(a, a)