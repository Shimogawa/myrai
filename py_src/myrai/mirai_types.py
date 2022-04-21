from __future__ import annotations
from typing import Generic, Type, TypeVar, Union, overload
from py4j.java_gateway import GatewayClient, JavaObject, JavaClass, is_instance_of
from py4j.java_collections import JavaArray, JavaList

from myrai.jvm.java import Consumer, Object, gw
from myrai._util import FuncProxy


class MiraiPackage:
    pass


class BotFactory(Object):
    pass


class Bot(Object):
    pass


class EventChannel(Object):
    pass


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


class MessageEvent(Event):
    _fqn = "net.mamoe.mirai.event.events.MessageEvent"


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
        return cls._java_class.Key


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


###### net.mamoe.mirai.contact


class ContactOrBot(Object):
    _fqn = "net.mamoe.mirai.contact.ContactOrBot"


class Contact(ContactOrBot):
    _fqn = "net.mamoe.mirai.contact.Contact"


class UserOrBot(ContactOrBot):
    _fqn = "net.mamoe.mirai.contact.UserOrBot"


class User(Contact, UserOrBot):
    _fqn = "net.mamoe.mirai.contact.User"
