from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from Models.Api.BaseApi import RequestApi, ApiAdapter
from DataType.CQcode import CQcode

setting_data = {
    # 加载优先级,数字越大优先级越高
    "priority": 100,
    # 插件是否可用启用
    "load": True,
    # 插件回调地址
    "callback_name": "pingbici",
    # 是否阻止后续插件执行
    "prevent_other_plugins": False,
    "event": ["message"],
}
auther_data = "ranfey"
name_data = "屏蔽词"
display_name_data = "屏蔽词"
version_data = "1.0"
description_data = "屏蔽词"
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

chi = "飞公主"


@plugin.register
async def pingbici(websocket: object, MessageData: GroupMassageData, Trigger):
    # 开发者命令
    if chi in MessageData.Message[0]:
        Trigger.run()
        api = "delete_msg"
        param = {"message_id": MessageData.Message_ID}
        args = RequestApi(api, param)
        await ApiAdapter.sendActionApi(websocket, args, 5)
