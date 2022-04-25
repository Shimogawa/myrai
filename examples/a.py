import sys
import atexit

sys.path.append("py_src")

from myrai.mirai import init, start_bot, subscribe_always, close, gw
from myrai.mirai_types import (
    At,
    EventPriority,
    ListeningStatus,
    MessageChain,
    MessageEvent,
    MessageUtils,
    PlainText,
    MessageContent,
    QuoteReply,
)
from myrai.jvm import java

init()
atexit.register(close)

bot = start_bot(int(sys.argv[1]), sys.argv[2])
bot.login()


def listener(e: MessageEvent):
    e.getSender().sendMessage(
        MessageUtils.static.newChain(
            [QuoteReply.new(e.getMessage()), PlainText.new("hi")]
        )
    )


# bot.getEventChannel().subscribeAlways(
#     mirai.get_mirai_pkg().event.events.MessageEvent._java_lang_class,
#     java.Consumer(listener),
# )

subscribe_always(bot, MessageEvent, listener)
