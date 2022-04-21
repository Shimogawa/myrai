from __future__ import annotations
from typing import Any, Callable, Generic, Type, TypeVar, Union

from py4j.java_gateway import JavaGateway, JavaClass, JavaObject, is_instance_of as iio
from py4j.java_collections import JavaArray, JavaList


from myrai._util import FuncProxy

_gw: JavaGateway = None


_T_OBJECT = TypeVar("_T_OBJECT", bound="Object")
_T_ENUM = TypeVar("_T_ENUM", bound="JavaEnum")


class JavaClassObject(Generic[_T_OBJECT], JavaObject):
    ...


class Object(JavaClass, JavaObject):
    __cached_java_class = None
    _fqn = "java.lang.Object"

    @classmethod
    @property
    def _java_class(cls: Type[_T_OBJECT]) -> _T_OBJECT:
        if cls.__cached_java_class is None:
            cls.__cached_java_class = eval(f"_gw.jvm.{cls._fqn}")
        return cls.__cached_java_class

    @classmethod
    @property
    def static(cls: Type[_T_OBJECT]) -> _T_OBJECT:
        return cls._java_class  # type: ignore

    @classmethod
    @property
    def _class(cls: Type[_T_OBJECT]) -> JavaClassObject:
        return cls._java_class._java_lang_class  # type: ignore

    @classmethod
    def new(cls: Type[_T_OBJECT], *args) -> _T_OBJECT:
        return cls._java_class(*args)

    def equals(self, other: Object) -> bool:
        ...

    def hashCode(self) -> int:
        ...

    def toString(self) -> str:
        ...


class JavaEnum(Object):
    _fqn = "java.lang.Enum"

    @classmethod
    def valueOf(cls: Type[_T_ENUM], name: str) -> _T_ENUM:
        ...

    @classmethod
    def values(cls) -> JavaArray:
        ...

    def ordinal(self) -> int:
        ...

    def name(self) -> str:
        ...


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


_T = TypeVar("_T")
_R = TypeVar("_R")


class Consumer(Generic[_T]):
    class Java:
        implements = ["java.util.function.Consumer"]

    def __init__(self, func: Callable[[_T], None]) -> None:
        self._func = func

    def accept(self, obj: _T):
        self._func(obj)


class Predicate(Generic[_T]):
    class Java:
        implements = ["java.util.function.Predicate"]

    def __init__(self, func: Callable[[_T], bool]) -> None:
        self._func = func

    def accept(self, obj: _T) -> bool:
        return self._func(obj)


class Function(Generic[_T, _R]):
    class Java:
        implements = ["java.util.function.Function"]

    def __init__(self, func: Callable[[_T], _R]) -> None:
        self._func = func

    def apply(self, obj: _T) -> _R:
        return self._func(obj)


class Function1(Generic[_T, _R]):
    class Java:
        implements = ["kotlin.jvm.functions.Function1"]

    def __init__(self, func: Callable[[_T], _R]) -> None:
        self._func = func

    def invoke(self, obj: _T) -> _R:
        return self._func(obj)


class Throwable(Object):
    def getMessage(self) -> str:
        ...

    def getLocalizedMessage(self) -> str:
        ...

    def getCause(self) -> Throwable:
        ...

    def printStackTrace(self) -> None:
        ...


class Optional(Object, Generic[_T]):
    def isEmpty(self) -> bool:
        ...

    def get(self) -> _T:
        ...

    def orElse(self, other: _T) -> _T:
        ...


class JavaStream(Generic[_T]):
    def filter(self, pred: Predicate[_T]) -> JavaStream[_T]:
        ...

    def map(self, func: Function[_T, _R]) -> JavaStream[_R]:
        ...

    def forEach(self, action: Consumer[_T]) -> None:
        ...

    def toArray(self) -> JavaArray:
        ...

    def findFirst(self) -> Optional[_T]:
        ...


class JavaCollection:
    def stream(self) -> JavaStream:
        ...
