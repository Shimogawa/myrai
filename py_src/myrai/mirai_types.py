from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, List, Type, TypeVar, Union, overload
from py4j.java_gateway import GatewayClient, JavaObject, JavaClass, is_instance_of
from py4j.java_collections import JavaArray, JavaList

from myrai.jvm.java import JavaEnum, Object, gw
from myrai._util import FuncProxy


###### moe.rebuild.myrai


class PyListenerHost(ABC):
    class Java:
        implements = ["moe.rebuild.myrai.PyListenerHost"]

    @abstractmethod
    def onMessage(self, e: MessageEvent):
        raise NotImplementedError

    def handleException(self, m: JavaObject):
        pass

    def onMessageWithStat(self, e: MessageEvent) -> ListeningStatus:
        return ListeningStatus.LISTENING  # type: ignore


class MyraiListenerHost(Object):
    _fqn = "moe.rebuild.myrai.MyraiListenerHost"


###### mirai packages


class MiraiPackage:
    pass


###### net.mamoe.mirai


class BotFactory(Object):
    _fqn = "net.mamoe.mirai.BotFactory"


class Bot(Object):
    _fqn = "net.mamoe.mirai.Bot"


###### net.mamoe.mirai.event


class ListeningStatus(JavaEnum):
    _fqn = "net.mamoe.mirai.event.ListeningStatus"

    @classmethod
    @property
    def LISTENING(cls) -> ListeningStatus:
        return cls.static.LISTENING  # type: ignore

    @classmethod
    @property
    def STOPPED(cls) -> ListeningStatus:
        return cls.static.STOPPED  # type: ignore


class EventPriority(JavaEnum):
    _fqn = "net.mamoe.mirai.event.EventPriority"

    for n in ["HIGHEST", "HIGH", "NORMAL", "LOW", "LOWEST", "MONITOR"]:
        exec(
            f"""
@classmethod
@property
def {n}(cls) -> EventPriority:
    return cls.static.{n}"""
        )


class SimpleListenerHost(Object):
    _fqn = "net.mamoe.mirai.event.SimpleListenerHost"


class Listener(Object):
    _fqn = "net.mamoe.mirai.event.Listener"


class EventChannel(Object):
    _fqn = "net.mamoe.mirai.event.EventChannel"


class Event(Object):
    _fqn = "net.mamoe.mirai.event.Event"


###### net.mamoe.mirai.event.events


class BotEvent(Event):
    _fqn = "net.mamoe.mirai.event.events.BotEvent"


class BotPassiveEvent(BotEvent):
    _fqn = "net.mamoe.mirai.event.events.BotPassiveEvent"


class BotActiveEvent(BotEvent):
    _fqn = "net.mamoe.mirai.event.events.BotActiveEvent"


class GroupEvent(BotEvent):
    _fqn = "net.mamoe.mirai.event.events.GroupEvent"


class GroupOperableEvent(GroupEvent):
    _fqn = "net.mamoe.mirai.event.events.GroupOperableEvent"


class UserEvent(BotEvent):
    _fqn = "net.mamoe.mirai.event.events.UserEvent"


class FriendEvent(UserEvent):
    _fqn = "net.mamoe.mirai.event.events.FriendEvent"


class GroupMemberEvent(GroupEvent, UserEvent):
    _fqn = "net.mamoe.mirai.event.events.GroupMemberEvent"


class MessageEvent(Event):
    _fqn = "net.mamoe.mirai.event.events.MessageEvent"


class UserMessageEvent(MessageEvent):
    _fqn = "net.mamoe.mirai.event.events.UserMessageEvent"


class FriendMessageEvent(UserMessageEvent, FriendEvent):
    _fqn = "net.mamoe.mirai.event.events.FriendMessageEvent"


class GroupAwareMessageEvent(MessageEvent):
    _fqn = "net.mamoe.mirai.event.events.GroupAwareMessageEvent"


class GroupMessageEvent(GroupAwareMessageEvent, GroupEvent):
    _fqn = "net.mamoe.mirai.event.events.GroupMessageEvent"


class GroupTempMessageEvent(GroupAwareMessageEvent, UserMessageEvent):
    _fqn = "net.mamoe.mirai.event.events.GroupTempMessageEvent"


###### net.mamoe.mirai.message.action


class Nudge(Object):
    _fqn = "net.mamoe.mirai.message.action.Nudge"


class BotNudge(Nudge):
    _fqn = "net.mamoe.mirai.message.action.BotNudge"


class UserNudge(Nudge):
    _fqn = "net.mamoe.mirai.message.action.UserNudge"


class MemberNudge(UserNudge):
    _fqn = "net.mamoe.mirai.message.action.MemberNudge"


class FriendNudge(UserNudge):
    _fqn = "net.mamoe.mirai.message.action.FriendNudge"


###### net.mamoe.mirai.message.data


class Message(Object):
    _fqn = "net.mamoe.mirai.message.data.Message"


class SingleMessage(Message):
    _fqn = "net.mamoe.mirai.message.data.SingleMessage"


class ConstrainSingle(SingleMessage):
    _fqn = "net.mamoe.mirai.message.data.ConstrainSingle"


class MessageMetadata(SingleMessage):
    _fqn = "net.mamoe.mirai.message.data.MessageMetadata"


_T_M = TypeVar("_T_M", bound=ConstrainSingle)


class MessageContent(SingleMessage):
    _fqn = "net.mamoe.mirai.message.data.MessageContent"
    # Key: MessageKey

    @classmethod
    @property
    def Key(cls: Type[_T_M]) -> MessageKey[_T_M]:
        return cls._java_class.Key  # type: ignore


class MessageChain(Message):
    _fqn = "net.mamoe.mirai.message.data.MessageChain"


class MessageKey(Generic[_T_M]):
    _fqn = "net.mamoe.mirai.message.data.MessageKey"


class MessageSource(MessageMetadata, ConstrainSingle):
    _fqn = "net.mamoe.mirai.message.data.MessageSource"


class QuoteReply(MessageMetadata, ConstrainSingle):
    _fqn = "net.mamoe.mirai.message.data.QuoteReply"


class PlainText(MessageContent):
    _fqn = "net.mamoe.mirai.message.data.PlainText"


class At(MessageContent):
    _fqn = "net.mamoe.mirai.message.data.At"


class MessageUtils(Object):
    _fqn = "net.mamoe.mirai.message.data.MessageUtils"

    @classmethod
    def newChain(cls, *args):
        return cls.static.newChain(list(args))


###### net.mamoe.mirai.contact


class ContactList(Object):
    _fqn = "net.mamoe.mirai.contact.ContactList"


class ContactOrBot(Object):
    _fqn = "net.mamoe.mirai.contact.ContactOrBot"


class Contact(ContactOrBot):
    _fqn = "net.mamoe.mirai.contact.Contact"


class UserOrBot(ContactOrBot):
    _fqn = "net.mamoe.mirai.contact.UserOrBot"


class User(Contact, UserOrBot):
    _fqn = "net.mamoe.mirai.contact.User"


class Member(User):
    _fqn = "net.mamoe.mirai.contact.Member"


class MemberPermission(JavaEnum):
    _fqn = "net.mamoe.mirai.contact.MemberPermission"

    @classmethod
    def MEMBER(cls):
        return cls.static.MEMBER

    @classmethod
    def ADMINISTRATOR(cls):
        return cls.static.ADMINISTRATOR

    @classmethod
    def OWNER(cls):
        return cls.static.OWNER


class NormalMember(Member):
    _fqn = "net.mamoe.mirai.contact.NormalMember"


class AnonymousMember(Member):
    _fqn = "net.mamoe.mirai.contact.AnonymousMember"


class Group(Contact):
    _fqn = "net.mamoe.mirai.contact.Group"


class Friend(User):
    _fqn = "net.mamoe.mirai.contact.Friend"
