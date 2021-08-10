from unittest import TestCase
from pykxnr.string_tools import *

class TestStringMethods(TestCase):
    def test_split_on_indices(self):
        test_str = 'a' * 10
        self.assertEqual(split_on_indices(test_str, (5,)), ('a' * 5, 'a' * 5))
        self.assertEqual(split_on_indices(test_str, (2, 6)), ('a' * 2, 'a' * 4, 'a' * 4))
        self.assertEqual(split_on_indices(test_str, (2, 10)), ('a' * 2, 'a' * 8, ''))
        self.assertEqual(split_on_indices(test_str, (0, 10)), ('', test_str, ''))

    def test_pad(self):
        test_str = 'a' * 10
        offset = 3
        l = 20
        padded = pad(test_str, offset, l-offset-len(test_str), char='-')
        self.assertEqual(padded.find(test_str), offset)
        self.assertEqual(len(padded), l)

    def test_merge_strings(self):
        strings = ['abbccdd', 'bbcc', 'ccddeeff', 'aabbcc']
        self.assertEqual(merge_strings(strings), 'aabbccddeeff')
