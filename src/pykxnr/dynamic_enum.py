#####
# Placeholder models that serve as enums. The actual values that they can take on are
# filled in at runtime and stored on flask.g so that the values have the same lifetime
# as the context that creates them.
#####
class DynamicEnum(Enum):
    """
    Since our enum values are stored as a database type and their values defined by the
    database schema, we need to create our enums at runtime and tie the lifetimes of these
    enums to the application context. We need this last piece because we, strictly speaking,
    don't have any guarantee that the enum values from the previous context are valid in
    the current context--we must re-initialize them.

    To accomplish this, init_values creates a dynamic subclass of the current enum with
    the given values and stores a weakref to this instance (through __subclasses__). This
    subclass is substituted for the base class for 1) attribute lookup 2) 'construction', ie Enum(somevalue), and 3) __getitem__. The lifetime of the Enum returned from init_values is determined by the calling context. When it is dropped, the Enum will revert to its default state.
    """
    @classmethod
    def init_values(cls, values: List[Tuple[str, Any]]):
        pass

    def __call__(self, *args, **kwargs):
        existing_subclass, *_ = type(self).__subclasses__()

        if existing_subclass:
            return existing_subclass(*args, **kwargs)

        return super().__call__(*args, **kwargs)

    def __getitem__(self, item):
        existing_subclass, *_ = type(self).__subclasses__()

        if existing_subclass:
            return existing_subclass["item"]

        return super().__members__[item]

    def __getattribute__(self, item):
        existing_subclass, *_ = type(self).__subclasses__()

        if existing_subclass:
            object.__getattribute__(existing_subclass, item)

        return super().__getattribute__(item)
