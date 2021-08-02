from html.parser import HTMLParser
from itertools import zip_longest
from difflib import SequenceMatcher


def _merge_strings(a, b):
    ai, bi, l = SequenceMatcher(None, a, b, autojunk=False).find_longest_match()

    # match must include beginning of one sequence and end of at least one sequence
    # to have merge properly calculated
    assert (ai == 0 or bi == 0) and (ai + l == len(a) or bi + l == len(b))

    a_start, overlap, a_end = split_on_indices(a, (ai, ai+l))
    b_start, _, b_end = split_on_indices(b, (bi, bi+l))
    return a_start + b_start + overlap + a_end + b_end


def merge_strings(strings: list[str]):
    # test if all strings are substring of longest
    longest = max(strings, key=lambda x: len(x))
    if all([longest.find(s) >= 0 for s in strings]):
        return longest

    # merge sequences pairwise
    return merge_strings([_merge_strings(a, b) for a, b in zip_longest(strings[:len(strings)//2], 
                                                                       strings[len(strings)//2:], 
                                                                       fillvalue='')])


def _split_on_index(seq, start):
    '''
    helper function to split a string on an index and return both pieces

    :param iterable seq: iterable to split
    :param int start: start of second half of sequence

    :return: split sequence
    '''
    return seq[:start], seq[start:]


def split_on_indices(seq, starts):
    '''
    given a list of indices, return pieces of an iterable split on these indices
    such that joining the pieces return the original iterable

    :param iterable seq: iterable to split
    :param iterable starts: collection of integer indices, must be sorted

    :return tuple: collection of slices
    '''
    first, last = _split_on_index(seq, starts[-1])

    if len(starts) > 1:
        return *split_on_indices(first, starts[:-1]), last
    else:
        return first, last


def pad(seq: str, start: int, end: int, char='-'):
    '''
    add characters to string to pad it to a
    given length, adding characters to the beginning
    to match offset, then remaining characters to end of string

    :param seq: string to pad
    :param start:
    :param end:
    :param char: character to add for padding
    :return: padded string
    '''
    return char * start + seq + char * end


# TODO: restructure to use singleton and reset single instance
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
