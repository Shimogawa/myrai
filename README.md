# Myrai

[![build](https://github.com/Shimogawa/myrai/actions/workflows/build.yml/badge.svg)](https://github.com/Shimogawa/myrai/actions/workflows/build.yml)
[![PyPI](https://img.shields.io/pypi/v/myrai)](https://pypi.org/project/myrai/)

用 Python (>=3.9) 写你熟悉的 [`mirai-core`][mirai-core]！（WIP）

使用了 [`py4j`][py4j]。自带一个接口的 jar 文件，并且会自己启动。可以设置使用其它 jar 文件或不从 Python 端启动。

## 简介

为了用 Python 连接 `mirai-core`，现在需要经过 [`mirai-api-http`][mah]。通用方法是使用 [`mirai-console-loader`][mcl] 进行启动，这样太麻烦（需要额外的软件与插件）。为了节省这些麻烦，直接通过 `py4j` 利用 socket 实现了 Python 与 `mirai-core` 的交互，节省了中间使用 HTTP 的麻烦。

至于为什么是 3.9 版本或以上……因为 3.9 好！3.8 没有什么很特别的更新，而 3.7 的支持结束时间是 2023/6/27。

## 使用方法

### 前提条件

- Python 3.9+
- Java 11+

### 安装

```sh
pip install myrai
```

### 初始化

```py
import myrai

myrai.init()
# ========
bot = myrai.start_bot(114514, "password")  # qq 和 password
# -------- 或者
import hashlib
bot = myrai.start_bot(
    114514,
    hashlib.md5("password".encode("utf-8")).digest()  # 用 MD5
)
# ========
bot.login()
```

### 初始化完成后

使用方式与 `mirai-core` 一模一样。在 `mirai_types` 中提供了所有（WIP）在 `mirai-core` 中有的类。在 `java` 中提供了一部分会经常使用的 Java 类。

这些类大多用作代码提示，因为运行时它们的类型都不一样，都是 `py4j` 的 `JavaClass`，`JavaObject` 等。

使用 `.new` 可以创建它的 Java 对象，使用 `.static` 能获取到它的类对象。所以想要调用静态方法和其它的方法可以这样：

```py
def listener(e: MessageEvent):
    e.getSender().sendMessage(
        MessageUtils.static.newChain(
            [
                QuoteReply.new(e.getMessage()),
                PlainText.new("hi"),
            ]
        )
    )
```

**注意：有些 Java 静态方法 / 成员为了方便使用，可以在 Python 类上直接调用静态方法 / 变量 (实际使用了 classmethod 和 property)。这些方法会有代码提示。没有代码提示的静态方法请使用 `.static`。如果你没有代码提示或不放心一直报错，那就使用 `.static` 调用静态成员。例如：**

```py
MessageUtils.newChain(...)  # OK
MessageUtils.static.newChain(...)  # OK
MessageUtils.static.buildMessageChain(...)  # OK

MessageUtils.buildMessageChain(...)  # 不OK
```

> 由于这个新特性（将 `@classmethod` 和 `@property` 用在一起）的不稳定性，Python 可能在后续版本中废弃这个写法（见 [issue](https://github.com/python/cpython/issues/89519)）。所以 `myrai` 的后续版本中也会修改这个用法并降低可使用的 Python 版本。

### 收尾

```py
myrai.close()
```

建议使用 `atexit`。

```py
import atexit
import myrai

atexit.register(myrai.close)
```

[py4j]: https://github.com/py4j/py4j
[mirai-core]: https://github.com/mamoe/mirai
[mah]: https://github.com/project-mirai/mirai-api-http
[mcl]: https://github.com/iTXTech/mirai-console-loader
