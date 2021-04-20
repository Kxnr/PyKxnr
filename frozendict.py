from collections import abc
import copy

# adapted from https://github.com/slezica/python-frozendict

# TODO: more conservative approach to
# limit deep copies
def copy_mutable():
    pass


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
            self._hash = hash(repr(self))
        return self._hash
