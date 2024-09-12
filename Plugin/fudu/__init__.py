from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
import requests

setting_data = {
    # 加载优先级,数字越大优先级越高
    "priority": 100,
    # 插件是否可用启用
    "load": False,
    # 插件回调地址
    "callback_name": "fudu",
    # 是否阻止其他插件执行
    "prevent_other_plugins": False,
    "event": ["message"],
}
auther_data = "然飞 ranfey"
name_data = "主动复读"
display_name_data = "主动复读"
version_data = "1.0"
description_data = "主动复读"
developer_setting_data = {
    # 是否记录运行时间
    "count_runtime": False,
    # 运行时间阈值，超过则输出警告
    "runtime_threshold": 0.5,
    # 是否允许高时间消耗，如果为否，则会在运行时间过长时输出警告，警告时间默认为0.5秒
    "allow_high_time_cost": False,
}

plugin = Plugin(
    auther=auther_data,
    name=name_data,
    display_name=display_name_data,
    version=version_data,
    description=description_data,
    setting=setting_data,
    developer_setting=developer_setting_data,
)


class TTemp(object):
    temp0 = ""
    tempQQ = ""

    def setFuduTemp(self, MessageData: GroupMassageData):
        TTemp.temp0 = MessageData.RowMessage
        TTemp.tempQQ = MessageData.QQ

    def setFudu000(self):
        TTemp.temp0 = ""
        TTemp.tempQQ = ""


GroupClass = {}


def copyGroup(MessageData: str):
    GroupClass.setdefault(MessageData, TTemp())


@plugin.register
async def fudu(websocket: object, MessageData: GroupMassageData, Trigger):
    GroupTT = str(MessageData.Group)
    copyGroup(GroupTT)
    if (
        GroupClass[GroupTT].temp0 == MessageData.RowMessage
        and GroupClass[GroupTT].tempQQ != MessageData.QQ
    ):
        await MessageApi.sendGroupMessage(
            websocket, MessageData, MessageData.RowMessage
        )
        Trigger.run()
        GroupClass[GroupTT].setFudu000()
    else:
        GroupClass[GroupTT].setFuduTemp(MessageData)
