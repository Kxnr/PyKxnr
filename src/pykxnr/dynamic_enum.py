from enum import EnumMeta
from typing import List, Tuple, Any

# sadly, this doesn't seem to work
# the subclasses aren't dropped when I'd expect them to, and so 
# remain reachable outside of their expected lifetime.
# more testing needed, as this may be an artifact of ipython keeping refs alive


class DynamicEnum(EnumMeta):
    def init_values(cls, values: List[Tuple[str, Any]]):
        return cls(f"{cls.__name__}_Implementation", values)

    def __call__(self, *args, **kwargs):
        existing_subclass = next(iter(self.__subclasses__()), None)
        if existing_subclass is not None:                                                          
            return existing_subclass(*args, **kwargs)
        return super().__call__(*args, **kwargs)

    def __getitem__(self, item):
        existing_subclass = next(iter(self.__subclasses__()), None)

        if existing_subclass is not None:                                                          
            return existing_subclass.__getitem__(item)
        return super().__getitem__(item)

    def __getattr__(self, item):
        existing_subclass = next(iter(self.__subclasses__()), None)
        if existing_subclass is not None:
            return EnumMeta.__getattr__(existing_subclass, item)
        return EnumMeta.__getattr__(self, item)

