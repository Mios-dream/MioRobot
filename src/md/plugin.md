# 进阶

------

## 插件编写

所有插件都放在Plugin文件夹中

插件的结构应为

```
Plugin  插件文件夹
   ├─plugin_1   插件1
   │   ├─__init__.py    初始化文件
   │   ├─metadata.json  插件信息文件
   │   └─other.py   其他文件
   └─plugin_2   插件1
      ├─__init__.py 初始化文件
      ├─metadata.json   插件信息文件
      └─other.py    其他文件
```

所有的插件都必须包含 **__ init __.py**



测试插件示例

```python
from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi

plugin = Plugin(
    author="三三",
    name="简单的消息测试",
    version="1.0",
    description="简单的消息测试",
    setting={
        # 加载优先级,数字越大优先级越高
        "priority": 0,
        # 插件是否可用启用
        "load": True,
        # 插件回调地址，需要和后面的方法对应
        "callback_name": "test",
        # 是否阻止后续插件执行
        "prevent_other_plugins": False,
        #监听事件的类型
        "event": ["message"],
    },
)


@plugin.register
async def test(websocket: object, MessageData: GroupMassageData, Trigger):

    if MessageData.Message[0] == "测试":
 
        await MessageApi.sendGroupMessage(websocket,MessageData,"测试成功")
```



### 流程

1，首先我们需要导入插件的基类`Plugin`,并设置插件的基本信息

```python
from plugins import Plugin

plugin = Plugin(
    #作者
    author="三三",
    #插件名
    name="简单的消息测试",
    #插件版本
    version="1.0",
    #插件描述
    description="简单的消息测试",
    setting={
        # 加载优先级,数字越大优先级越高
        "priority": 0,
        # 插件是否可用启用
        "load": True,
        # 插件回调地址，需要和后面的方法对应
        "callback_name": "test",
        # 是否阻止后续插件执行
        "prevent_other_plugins": False,
        #监听事件的类型
        "event": ["message"],
    },
)
```



2，注册插件

将`plugin.register`作为插件主体的装饰器，`test`即为插件的入口，和上面的`callback_name`对应

插件的传参是固定的，不可以更改

```python
@plugin.register
async def test(websocket: object, MessageData: GroupMassageData, Trigger):
```

`async`关键字表示这个插件是异步的，插件的入口必须使用异步

`websocket`为websocket连接对象，用于给消息api传参

`MessageData`为上报信息，具体可以查看`GroupMassageData`中的内容



3，发送简单的消息

```python
@plugin.register
async def test(websocket: object, MessageData: GroupMassageData, Trigger):
    #如果上报消息为测试，则发送测试成功
    if MessageData.Message[0] == "测试":
    await MessageApi.sendGroupMessage(websocket,MessageData,"测试成功")
    
```

`MessageApi.sendGroupMessage()`是异步方法，需要通过`await`调用，详细传参请见`sendGroupMessage()`说明


使用Trigger.run来标记插件是否运行