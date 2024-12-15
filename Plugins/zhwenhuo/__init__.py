from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
import random
import re
import requests
import json
import jieba

setting_data = {
    # 加载优先级,数字越大优先级越高
    "priority": 20,
    # 插件是否可用启用
    "load": False,
    # 插件回调地址
    "callback_name": "zhwenhuo",
    # 是否阻止其他插件执行
    "prevent_other_plugins": False,
    "event": ["message"],
}
author_data = "然飞 ranfey"
name_data = "zhwenhuo"
display_name_data = "攻击性拉满"
version_data = "1.0"
description_data = "攻击性拉满"
developer_setting_data = {
    # 是否记录运行时间
    "count_runtime": False,
    # 运行时间阈值，超过则输出警告
    "runtime_threshold": 0.5,
    # 是否允许高时间消耗，如果为否，则会在运行时间过长时输出警告，警告时间默认为0.5秒
    "allow_high_time_cost": False,
}

plugin = Plugin(
    author=author_data,
    name=name_data,
    display_name=display_name_data,
    version=version_data,
    description=description_data,
    setting=setting_data,
    developer_setting=developer_setting_data,
)

# 对方qq号
qqt = ""


@plugin.register
async def zhwenhuo(websocket: object, MessageData: GroupMassageData, Trigger):
    bbb = random.randint(1, 3)
    if qqt in MessageData.QQ:
        words = jieba.lcut(MessageData.Message[0])
        ii = random.randint(1, len(words)) - 1
        word = words[ii]
        aaa = word + "?该闭嘴了"
        if bbb == 2:
            Trigger.run()
            await MessageApi.sendGroupMessage(websocket, MessageData, aaa)
