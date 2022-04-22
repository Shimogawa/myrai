import subprocess
import time
from typing import Callable, Optional, Type, TypeVar

import myrai.jvm.java as java
from myrai.mirai_types import MiraiPackage, Bot, Event

from importlib.resources import files

VERSION = "0.0.2"

_T_EVENT = TypeVar("_T_EVENT", bound=Event)

_DEFAULT_JAR = str(files("myrai").joinpath(f"resources/myrai-{VERSION}.jar"))


class Mirai:
    def __init__(self) -> None:
        self._java_proc: subprocess.Popen = None  # type: ignore
        self._started = False

    @property
    def started(self) -> bool:
        return self._started

    def get_mirai_pkg(self) -> MiraiPackage:
        return java.gw.jvm.net.mamoe.mirai

    def start(
        self,
        use_bundled=True,
        bridge_jar_file: Optional[str] = None,
        java_cmd: str = "java",
        **kwargs,
    ):
        if self._started:
            return
        if use_bundled:
            self._java_proc = subprocess.Popen(
                [
                    java_cmd,
                    "-jar",
                    bridge_jar_file if bridge_jar_file else _DEFAULT_JAR,
                ],
                **kwargs,
            )
            time.sleep(1)
            if self._java_proc.poll() is not None:
                raise RuntimeError("Cannot start Java backend")

        for i in range(5):
            try:
                java.start_gw()
                break
            except:
                if i == 4:
                    self.close()
                    raise RuntimeError("Cannot connect to Java backend")
                time.sleep(1)
        self._started = True

    def close(self):
        if not self._started:
            return
        java.close_gw()
        if self._java_proc:
            time.sleep(2)
            self._java_proc.terminate()
            self._java_proc = None
        self._started = False


mirai = Mirai()
gw = java.gw


def init(**kwargs):
    mirai.start(**kwargs)


def start_bot(qq: int, passwd: str) -> Bot:
    if not mirai.started:
        raise RuntimeError("call init() first")
    return mirai.get_mirai_pkg().BotFactory.INSTANCE.newBot(qq, passwd)


def close():
    mirai.close()


def subscribe_always(bot: Bot, event: Type[_T_EVENT], fn: Callable[[_T_EVENT], None]):
    bot.getEventChannel().subscribeAlways(
        java.get_class_by_name(event._fqn), java.Consumer(fn)
    )
