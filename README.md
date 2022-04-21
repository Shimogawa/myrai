# Myrai

用 Python 写你熟悉的 `mirai-core`！（WIP）

使用了 `py4j`。自带一个接口的 jar 文件，并且会自己启动。可以设置使用其它 jar 文件或不从 Python 端启动。

## 使用方法

### 初始化

```py
import myrai

myrai.init()
bot = myrai.start_bot(114514, "1919810")  # qq and password
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

**注意：绝对不能直接在 Python 类上调用静态方法，会报错！一定要使用 `.static`。**

### 收尾

```py
myrai.close()
```

建议使用 `atexit`。

```py
import atexit
import myrai

...

atexit.register(myrai.close)
```
