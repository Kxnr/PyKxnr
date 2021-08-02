from collections import abc
import pickle
import copy

# adapted from https://github.com/slezica/python-frozendict

# TODO: more conservative approach to
# limit deep copies
def copy_mutable():
    pass

def hash_mutable(item):
    try:
        return hash(item)
    except TypeError:
        p = pickle.dumps(item)
        return hash(p)

class frozendict(abc.Mapping):
    dict_cls = dict

    def __init__(self, *args, **kwargs):
        args = copy.deepcopy(args)
        kwargs = copy.deepcopy(kwargs)

        self._dict = self.dict_cls(*args, **kwargs)
        self._hash = None
        
    def __setitem__(self, key, value):
        raise TypeError("frozendict is immutable")

    def __getitem__(self, key):
        return copy.deepcopy(self._dict[key])

    def __contains__(self, key):
        return key in self._dict

    def copy(self, **add_or_replace):
        return self.__class__(self, **add_or_replace)

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self._dict}>'

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(frozenset(hash_mutable(a) for a in self.items()))

        return self._hash

if __name__ == "__main__":
    test_dict = {'int': 1, 
                 'dict': {'a': "words", 1: 163}, 
                 'tup': (11, 'word', [1, 'a', 6]),
                 'list': [156, 'yydk', 223]}

    test_1 = frozendict(test_dict)
    test_2 = frozendict(**test_dict)

    assert hash(test_1) == hash(test_2)
