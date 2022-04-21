from __future__ import annotations
from typing import Any, Generic, List, Type, TypeVar, Union, overload
from py4j.java_gateway import JavaObject, JavaClass
from py4j.java_collections import JavaArray, JavaIterator, JavaList

from myrai.jvm.java import Consumer, Function, Object, Optional, Predicate

_T = TypeVar("_T")
_R = TypeVar("_R")

class JavaStream(Generic[_T]):
    def filter(self, pred: Predicate[_T]) -> JavaStream[_T]: ...
    def map(self, func: Function[_T, _R]) -> JavaStream[_R]: ...
    def forEach(self, action: Consumer[_T]) -> None: ...
    def toArray(self) -> JavaArray: ...
    def findFirst(self) -> Optional[_T]: ...

class JavaCollection:
    def stream(self): ...

class MiraiPackage:
    contact: contact
    event: event
    message: message
    BotFactory: BotFactory
    Bot: Bot

class contact:
    Contact: Contact

class event:
    events: events
    Event: Event

class message:
    data: message_data

class message_data:
    pass

class events:
    MessageEvent: MessageEvent

class BotFactory:
    INSTANCE: BotFactory

    def newBot(self, qq: int, password: str, conf: JavaObject = None) -> Bot: ...

class Bot(Object):
    def getId(self) -> int: ...
    def getEventChannel(self) -> EventChannel: ...
    def login(self): ...

class EventChannel(Object):
    def subscribeAlways(self, event_cls: JavaObject, func: Consumer): ...

class Event(Object):
    isIntercepted: bool

    def intercept(self): ...

class BotEvent(Event):
    def getBot(self) -> Bot: ...

class BotPassiveEvent(BotEvent): ...
class BotActiveEvent(BotEvent): ...
class GroupEvent(BotEvent): ...

class MessageEvent(BotPassiveEvent):
    def getSubject(self) -> Contact: ...
    def getMessage(self) -> MessageChain: ...
    def getSender(self) -> Contact: ...
    def getSenderName(self) -> str: ...
    def getTime(self) -> int: ...

###### net.mamoe.mirai.message.data

class Message(Object):
    def contentToString(self) -> str: ...
    def plus(
        self, msg: Union[str, Message, JavaArray, List[str], List[Message]]
    ) -> MessageChain: ...
    def contentEquals(
        self, other: Union[str, Message], ignore_case: bool, strict: bool = False
    ): ...

class SingleMessage(Message): ...
class ConstrainSingle(SingleMessage): ...
class MessageMetadata(SingleMessage): ...

_T_M = TypeVar("_T_M", bound=SingleMessage)

class MessageContent(SingleMessage):
    @classmethod
    @property
    def Key(cls: Type[_T_M]) -> MessageKey[_T_M]: ...

class MessageChain(Message, JavaList, JavaCollection):
    @overload
    def get(self, idx: int) -> SingleMessage: ...
    @overload
    def get(self, idx: MessageKey[_T_M]) -> _T_M: ...
    def contains(self, msg_key: MessageKey[_T_M]) -> bool: ...

class MessageKey(Generic[_T_M]): ...

class MessageSource(MessageMetadata, ConstrainSingle):
    def getBotId(self) -> int: ...
    def getTime(self) -> int: ...
    def getFromId(self) -> int: ...
    def getTargetId(self) -> int: ...
    def getOriginalMessage(self) -> MessageChain: ...

class QuoteReply(MessageMetadata, ConstrainSingle):
    @classmethod
    def new(cls, src: MessageChain) -> QuoteReply: ...
    def getSource(self) -> MessageSource: ...

class PlainText(MessageContent):
    @classmethod
    def new(cls, msg: str) -> PlainText: ...

class At(MessageContent):
    @classmethod
    def new(cls, target: int) -> At: ...
    def getTarget(self) -> int: ...

class MessageUtils(Object):
    @classmethod
    @overload
    def newChain(cls, *msgs: Message) -> MessageChain: ...
    @classmethod
    @overload
    def newChain(cls, lst: Union[List[Message], JavaList]) -> MessageChain: ...

###### net.mamoe.mirai.contact

class ContactOrBot(Object):
    def getBot(self) -> Bot: ...
    def getId(self) -> int: ...
    def getAvatarUrl(self) -> str: ...

class Contact(ContactOrBot):
    def sendMessage(self, msg: Union[Message, str]) -> Any: ...

class UserOrBot(ContactOrBot):
    def getNick(self) -> str: ...
    def nudge(self): ...

class User(Contact, UserOrBot):
    def getRemark(self) -> str: ...
    def queryProfile(self): ...
