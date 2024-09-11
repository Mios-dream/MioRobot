from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
from plugin_loader import PluginLoaderControl
from log import Log

setting_data = {
    # 加载优先级,数字越大优先级越高
    "priority": 100,
    # 插件是否可用启用
    "load": True,
    # 插件回调地址
    "callback_name": "Control",
    # 是否阻止后续插件执行
    "prevent_other_plugins": False,
    "event": ["message"],
}
auther_data = "三三"
name_data = "插件重载"
display_name_data = "插件重载"
version_data = "1.0"
description_data = "重载插件"
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
async def Control(websocket: object, MessageData: GroupMassageData, Trigger) -> None:
    # 开发者命令
    if MessageData.Message[0] == "#重载":
        Trigger.run()
        try:

            PluginLoaderControl.reload()
            await MessageApi.sendGroupMessage(websocket, MessageData, "重载完成啦！")
            return 0

        except Exception as e:
            Log.error(f"重载失败,错误信息：{e}")
