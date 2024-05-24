from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
import random
import re
import requests
import json
import jieba

plugin = Plugin(
    auther="然飞 ranfey",
    name="zhwenhuo",
    version="1.0",
    display_name="zhwenhuo",
    description="zhwenhuo",
    setting={
        # 加载优先级,数字越大优先级越高
        "priority": 20,
        # 插件是否可用启用
        "load": False,
        # 插件回调地址
        "callback_name": "zhwenhuo",
        # 是否阻止其他插件执行
        "prevent_other_plugins": False,
        "event": ["message"],
    },
)

# 对方qq号
qqt = ""


@plugin.register
async def zhwenhuo(websocket: object, MessageData: GroupMassageData):
    bbb = random.randint(1, 3)
    if qqt in MessageData.QQ:
        words = jieba.lcut(MessageData.Message[0])
        ii = random.randint(1, len(words)) - 1
        word = words[ii]
        aaa = word + "?该闭嘴了"
        if bbb == 2:
            await MessageApi.sendGroupMessage(websocket, MessageData, aaa)
