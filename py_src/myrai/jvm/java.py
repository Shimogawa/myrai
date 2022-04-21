from __future__ import annotations
from typing import Any, Callable, Generic, Type, TypeVar, Union

from py4j.java_gateway import (
    JavaGateway,
    JavaClass,
    JavaObject,
    is_instance_of as iio,
)
from py4j.java_collections import JavaArray, JavaList


from myrai._util import FuncProxy

_gw: JavaGateway = None

_T = TypeVar("_T", bound="Object")


class Object(JavaClass, JavaObject):
    _fqn = "java.lang.Object"

    @classmethod
    @property
    def _java_class(cls: Type[_T]) -> _T:
        return eval(f"_gw.jvm.{cls._fqn}")

    @classmethod
    @property
    def static(cls: Type[_T]) -> _T:
        return cls._java_class  # type: ignore

    @classmethod
    @property
    def _class(cls: Type[_T]) -> JavaObject:
        return cls._java_class._java_lang_class  # type: ignore

    @classmethod
    def new(cls: Type[_T], *args) -> _T:
        return cls._java_class(*args)

    def equals(self, other: Object) -> bool:
        ...

    def toString(self) -> str:
        ...


_T_OBJECT = TypeVar("_T_OBJECT", bound=Object)


def start_gw():
    global _gw
    if _gw is not None:
        return
    _gw = JavaGateway(start_callback_server=True, auto_convert=True)


def close_gw():
    global _gw
    if _gw is None:
        return
    _gw.close(close_callback_server_connections=True)
    _gw = None


def is_gw_started() -> bool:
    return _gw is not None


def get_gw():
    return _gw


gw: JavaGateway = FuncProxy(get_gw)


def get_class(py4j_cls: JavaClass) -> JavaObject:
    return py4j_cls._java_lang_class


def get_class_by_name(fqn: str) -> JavaObject:
    return _gw.jvm.py4j.reflection.ReflectionUtil.classForName(fqn)


def is_instance_of(obj: _T_OBJECT, type: Type[_T_OBJECT]) -> bool:
    return iio(_gw, obj, type._java_class)


def new_array(cls: Union[Type[_T_OBJECT], JavaClass], *dimensions: int) -> JavaArray:
    return gw.new_array(
        cls if isinstance(cls, JavaClass) else get_class_by_name(cls._fqn), *dimensions
    )


def array_of(cls: Union[Type[_T_OBJECT], JavaClass], *items: _T_OBJECT):
    arr = gw.new_array(
        cls if isinstance(cls, JavaClass) else get_class_by_name(cls._fqn), len(items)
    )
    for i in range(len(items)):
        arr[i] = items[i]
    return arr


_S = TypeVar("_S")
_R = TypeVar("_R")


class Consumer(Generic[_S]):
    class Java:
        implements = ["java.util.function.Consumer"]

    def __init__(self, func: Callable[[_S], None]) -> None:
        self._func = func

    def accept(self, obj):
        self._func(obj)


class Predicate(Generic[_S]):
    class Java:
        implements = ["java.util.function.Predicate"]

    def __init__(self, func: Callable[[_S], bool]) -> None:
        self._func = func

    def accept(self, obj):
        return self._func(obj)


class Function(Generic[_S, _R]):
    class Java:
        implements = ["java.util.function.Function"]

    def __init__(self, func: Callable[[_S], _R]) -> None:
        self._func = func

    def apply(self, obj):
        return self._func(obj)


class Optional(Object, Generic[_S]):
    def isEmpty(self) -> bool:
        ...

    def get(self) -> _S:
        ...

    def orElse(self, other: _S) -> _S:
        ...
