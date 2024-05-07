from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
import requests


plugin = Plugin(
    auther="ranfey",
    name="复读",
    version="1.0",
    description="复读",
    setting={
        # 加载优先级,数字越大优先级越高
        "priority": 100,
        # 插件是否可用启用
        "load": True,
        # 插件回调地址
        "callback_name": "fudu",
        # 是否阻止其他插件执行
        "prevent_other_plugins": False,
        "event": ["message"],
    },
)


class TTemp(object):
    temp0=""
    tempQQ=""
    def setFuduTemp(self,MessageData:GroupMassageData):
        TTemp.temp0=MessageData.RowMessage
        TTemp.tempQQ=MessageData.QQ
    def setFudu000(self):
        TTemp.temp0=""
        TTemp.tempQQ=""
GroupClass={}
def copyGroup(MessageData:str):
    GroupClass.setdefault(MessageData, TTemp())
@plugin.register
async def fudu(websocket: object, MessageData: GroupMassageData):
    GroupTT=str(MessageData.Group)
    copyGroup(GroupTT)
    if(GroupClass[GroupTT].temp0 == MessageData.RowMessage and GroupClass[GroupTT].tempQQ!=MessageData.QQ):
        await MessageApi.sendGroupMessage(websocket, MessageData,MessageData.RowMessage)
        GroupClass[GroupTT].setFudu000()
    else:
        GroupClass[GroupTT].setFuduTemp(MessageData)