from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from Plugin.menu.Menu import Menu
from DataType.CQcode import CQcode
import re


setting_data = {
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
auther_data = "三三"
name_data = "菜单"
display_name_data = "菜单"
version_data = "1.0"
description_data = "菜单"
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


@plugin.register
async def menu(websocket: object, MessageData: GroupMassageData, Trigger):
    if MessageData.Message[0] == "菜单":
        Trigger.run()
        menu_data = Menu(display_number=10)
        await MessageApi.sendGroupMessage(websocket, MessageData, menu_data.show_menu())

        if menu_data.page_number > 1:
            await MessageApi.sendGroupMessage(
                websocket,
                MessageData,
                CQcode.at(MessageData.QQ)
                + ' 这是第1页菜单,总共{}页,发送"第2页"可以查看其他菜单哦'.format(
                    menu_data.page_number
                ),
            )

    elif num := re.match(r"第(\d+)页", MessageData.Message[0]):
        menu_data = Menu(display_number=10)
        data = menu_data.show_menu(page_num=int(num.group(1)))
        await MessageApi.sendGroupMessage(
            websocket,
            MessageData,
            data if data else CQcode.at(MessageData.QQ) + " 没有更多了",
        )
