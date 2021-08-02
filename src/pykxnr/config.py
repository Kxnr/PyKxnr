import configparser
import json
import pathlib
import os
from .frozendict import frozendict


def load_configuration(path: str):
    if not os.path.exists(path):
        raise Exception("config not found")

    _, config_type = os.path.splitext(path)
    if config_type == '.json':
        JsonConfig.load(path)
    elif config_type == '.ini':
        IniConfig.load(path)
    else:
        raise Exception(f"config type '{config_type}' not supported.")


class ClassPropertyDescriptor(object):

    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


class ClassPropertyMetaClass(type):
    def __setattr__(self, key, value):
        obj = None
        if key in self.__dict__:
            obj = self.__dict__.get(key)

        if obj and type(obj) is ClassPropertyDescriptor:
            return obj.__set__(self, value)

        return super(ClassPropertyMetaClass, self).__setattr__(key, value)


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return ClassPropertyDescriptor(func)


def make_closure(val):
    def closure(*args, **kwargs):
        return val
    return closure


class ConfigComponent(ClassPropertyMetaClass):
    def load(cls, config: dict):
        for k, v in config.items():
            if isinstance(v, dict):
                nested = ConfigComponent(k, (), {})
                nested.load(v)
                setattr(cls, k, classproperty(make_closure(nested)))
            else:
                setattr(cls, k, classproperty(make_closure(v)))
                
    def freeze(cls):
        def deep_freeze(cls, k):
            val = getattr(cls, k)
            if isinstance(val, ConfigComponent):
                return val.freeze()
            return val

        return frozendict({k: deep_freeze(cls, k) for k, v in cls.__dict__.items()
                           if isinstance(v, ClassPropertyDescriptor)})


class Config(metaclass=ConfigComponent):
    def __init__(self):
        raise Exception("Config allows class access only")


class JsonConfig(Config):
    @staticmethod
    def load(path: pathlib.Path):
        with open(path, 'r') as f:
            config = json.load(f)
        Config.load(config)


class IniConfig(Config):
    @staticmethod
    def load(path: pathlib.Path):
        config = configparser.parse(path)
        super().load(config)
