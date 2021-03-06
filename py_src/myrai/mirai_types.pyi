from __future__ import annotations
from abc import ABC, abstractmethod
from typing import (
    Any,
    Generic,
    List,
    NoReturn,
    Type,
    TypeVar,
    Union,
    overload,
    Optional,
)
from py4j.java_gateway import JavaObject
from py4j.java_collections import JavaArray, JavaList

from myrai.jvm.java import (
    Consumer,
    Function,
    Function1,
    JavaClassObject,
    JavaEnum,
    Object,
    JavaCollection,
)

###### moe.rebuild.myrai

class PyListenerHost(ABC):
    @abstractmethod
    def onMessage(self, e: MessageEvent): ...
    def handleException(self, m: JavaObject): ...
    def onMessageWithStat(self, e: MessageEvent): ...

class MyraiListenerHost(SimpleListenerHost):
    @classmethod
    def new(cls, py_host: PyListenerHost) -> MyraiListenerHost: ...  # type: ignore[override]

###### mirai package

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

###### net.mamoe.mirai

class BotFactory:
    INSTANCE: BotFactory

    def newBot(
        self, qq: int, password: Union[str, bytes], conf: JavaObject = None
    ) -> Bot: ...

class Bot(UserOrBot):
    def getEventChannel(self) -> EventChannel[BotEvent]: ...
    def login(self) -> None: ...
    def close(self) -> None: ...
    def getAsFriend(self) -> Friend: ...
    def getGroup(self, group_id: int) -> Optional[Group]: ...
    def getGroupOrFail(self, group_id: int) -> Group: ...
    def getFriend(self, id: int) -> Optional[Friend]: ...
    def getFriendOrFail(self, id: int) -> Friend: ...
    def getGroups(self) -> ContactList[Group]: ...
    def getFriends(self) -> ContactList[Friend]: ...
    def join(self) -> None: ...
    def isOnline(self) -> bool: ...
    def nudge(self) -> BotNudge: ...

###### net.mamoe.mirai.event

_T_EVENT = TypeVar("_T_EVENT", bound="Event")

class ListeningStatus(JavaEnum):
    LISTENING: ListeningStatus
    STOPPED: ListeningStatus

class EventPriority(JavaEnum):
    HIGHEST: EventPriority
    HIGH: EventPriority
    NORMAL: EventPriority
    LOW: EventPriority
    LOWEST: EventPriority
    MONITOR: EventPriority

class SimpleListenerHost(Object):
    def cancelAll(self) -> None: ...

class Listener(Object, Generic[_T_EVENT]):
    def getPriority(self) -> EventPriority: ...
    def onEvent(self, e: _T_EVENT) -> ListeningStatus: ...

class EventChannel(Generic[_T_EVENT], Object):
    __E_EC = TypeVar("__E_EC", bound=Event)

    def subscribeAlways(
        self, event_cls: JavaClassObject, func: Consumer[_T_EVENT]
    ) -> Listener[_T_EVENT]: ...
    def subscribeOnce(
        self, event_cls: JavaClassObject, func: Consumer[_T_EVENT]
    ) -> Listener[_T_EVENT]: ...
    def filter(self, filt: Function1[_T_EVENT, bool]) -> EventChannel[_T_EVENT]: ...
    def filterIsInstance(
        self, jclass: JavaClassObject[__E_EC]
    ) -> EventChannel[__E_EC]: ...
    def subscribe(
        self, event_cls: JavaClassObject, func: Function[_T_EVENT, ListeningStatus]
    ) -> Listener[_T_EVENT]: ...
    def registerListenerHost(self, host: SimpleListenerHost) -> None: ...

class Event(Object):
    def isIntercepted(self) -> bool: ...
    def intercept(self): ...

###### net.mamoe.mirai.event.events

class BotEvent(Event):
    def getBot(self) -> Bot: ...

class BotPassiveEvent(BotEvent): ...
class BotActiveEvent(BotEvent): ...

class GroupEvent(BotEvent):
    def getGroup(self) -> Group: ...

class GroupOperableEvent(GroupEvent):
    def getOperator(self) -> Optional[Member]: ...

class UserEvent(BotEvent):
    def getUser(self) -> User: ...

class FriendEvent(UserEvent):
    def getFriend(self) -> Friend: ...
    def getUser(self) -> Friend: ...

class GroupMemberEvent(GroupEvent, UserEvent):
    def getMember(self) -> Member: ...
    def getUser(self) -> Member: ...

class MessageEvent(BotPassiveEvent):
    def getSubject(self) -> Contact: ...
    def getMessage(self) -> MessageChain: ...
    def getSender(self) -> Contact: ...
    def getSenderName(self) -> str: ...
    def getTime(self) -> int: ...

class UserMessageEvent(MessageEvent):
    def getSubject(self) -> User: ...

class FriendMessageEvent(UserMessageEvent, FriendEvent):
    def getSender(self) -> Friend: ...
    def getSubject(self) -> Friend: ...

class GroupAwareMessageEvent(MessageEvent):
    def getGroup(self) -> Group: ...

class GroupMessageEvent(GroupAwareMessageEvent, GroupEvent):
    def getPermission(self) -> MemberPermission: ...
    def getSender(self) -> Member: ...
    def getSubject(self) -> Group: ...

class GroupTempMessageEvent(GroupAwareMessageEvent, UserMessageEvent):
    def getSender(self) -> NormalMember: ...
    def getSubject(self) -> NormalMember: ...

###### net.mamoe.mirai.message.action

class Nudge(Object):
    def getTarget(self) -> UserOrBot: ...
    def sendTo(self, receiver: Contact) -> bool: ...

class BotNudge(Nudge):
    def getTarget(self) -> Bot: ...

class UserNudge(Nudge): ...

class MemberNudge(UserNudge):
    def getTarget(self) -> NormalMember: ...

class FriendNudge(UserNudge):
    def getTarget(self) -> Friend: ...

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

class MessageChain(Message, JavaList, JavaCollection[_T_M]):
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
    def new(cls, src: MessageChain) -> QuoteReply: ...  # type: ignore[override]
    def getSource(self) -> MessageSource: ...

class PlainText(MessageContent):
    @classmethod
    def new(cls, msg: str) -> PlainText: ...  # type: ignore[override]

class At(MessageContent):
    @classmethod
    def new(cls, target: int) -> At: ...  # type: ignore[override]
    def getTarget(self) -> int: ...

class MessageUtils(Object):
    @classmethod
    @overload
    def newChain(cls, *msgs: Message) -> MessageChain: ...
    @classmethod
    @overload
    def newChain(cls, lst: Union[List[Message], JavaList]) -> MessageChain: ...

###### net.mamoe.mirai.contact

_C = TypeVar("_C", bound="Contact")

class ContactList(Generic[_C], Object, JavaCollection[_C]):
    def get(self, id: int) -> Optional[_C]: ...
    def getOrFail(self, id: int) -> _C: ...
    def getSize(self) -> int: ...
    def contains(self, id: int) -> bool: ...
    def remove(self, id: int) -> bool: ...

class ContactOrBot(Object):
    def getBot(self) -> Bot: ...
    def getId(self) -> int: ...
    def getAvatarUrl(self) -> str: ...

class Contact(ContactOrBot):
    def sendMessage(self, msg: Union[Message, str]) -> Any: ...

class UserOrBot(ContactOrBot):
    def getNick(self) -> str: ...
    def nudge(self) -> Nudge: ...

class User(Contact, UserOrBot):
    def getRemark(self) -> str: ...
    def queryProfile(self): ...
    def nudge(self) -> UserNudge: ...

class Member(User):
    def getGroup(self) -> Group: ...
    def getPermission(self) -> MemberPermission: ...
    def getNameCard(self) -> str: ...
    def getSpecialTitle(self) -> str: ...
    def mute(self, duration_secs: int) -> None: ...
    def nudge(self) -> MemberNudge: ...

class MemberPermission(JavaEnum):
    MEMBER: MemberPermission
    ADMINISTRATOR: MemberPermission
    OWNER: MemberPermission

    def getLevel(self) -> int: ...

class NormalMember(Member):
    def getMuteTimeRemaining(self) -> int: ...
    def isMuted(self) -> bool: ...
    def getJoinTimestamp(self) -> int: ...
    def getLastSpeakTimestamp(self) -> int: ...
    def unmute(self) -> None: ...
    def kick(self, msg: str, block: bool = False) -> None: ...
    def modifyAdmin(self, operation: bool) -> None: ...

class AnonymousMember(Member):
    def getAnonymousId(self) -> str: ...
    def sendMessage(self, msg: Union[Message, str]) -> NoReturn: ...

class Group(Contact):
    def getName(self) -> str: ...

class Friend(User):
    def delete(self) -> None: ...
    def nudge(self): ...
