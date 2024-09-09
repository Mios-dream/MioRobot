from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from Plugin.menu.Menu import Menu
from DataType.CQcode import CQcode

setdata = {
    # 加载优先级,数字越大优先级越高
    "priority": 100,
    # 插件是否可用启用
    "load": True,
    # 插件回调地址
    "callback_name": "menu",
    # 是否阻止后续插件执行
    "prevent_other_plugins": False,
    "event": ["message"],
    "is_hide": True,
}

plugin = Plugin(
    auther="三三",
    name="菜单",
    display_name="菜单",
    version="1.0",
    description="插件菜单",
    setting=setdata,
)


@plugin.register
async def menu(websocket: object, MessageData: GroupMassageData):
    if MessageData.Message[0] == "菜单":
        menu_data = Menu()
        await MessageApi.sendGroupMessage(websocket, MessageData, menu_data.show_menu())
