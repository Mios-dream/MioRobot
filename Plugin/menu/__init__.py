from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi


plugin = Plugin(
    auther="三三",
    name="菜单",
    version="1.0",
    description="插件菜单",
    setting={
        # 加载优先级,数字越大优先级越高
        "priority": 0,
        # 插件是否可用启用
        "load": False,
        # 插件回调地址
        "callback_name": "menu",
        # 是否阻止后续插件执行
        "prevent_other_plugins": False,
        "event": ["message"],
    },
)


@plugin.register
async def menu(websocket: object, MessageData: GroupMassageData):
    if MessageData.Message[0] == "菜单":
        ...
