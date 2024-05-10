from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from Plugin.menu.Menu import Menu
from DataType.CQcode import CQcode

plugin = Plugin(
    auther="三三",
    name="菜单",
    version="1.0",
    description="插件菜单",
    setting={
        # 加载优先级,数字越大优先级越高
        "priority": 100,
        # 插件是否可用启用
        "load": True,
        # 插件回调地址
        "callback_name": "menu",
        # 是否阻止后续插件执行
        "prevent_other_plugins": False,
        "event": ["message"],
    },
)


menu_data = """
┍       菜单     ┐\r
    🌸图片超分🌸\r
    🌸幻影坦克🌸\r
    🌸高考倒计时🌸\r
└                       ┘\r
=================\r
"""


@plugin.register
async def menu(websocket: object, MessageData: GroupMassageData):
    if MessageData.Message[0] == "菜单":
        menu_data = Menu()
        await MessageApi.sendGroupMessage(
            websocket, MessageData, "插件列表\n" + menu_data.show_menu()
        )
