from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from plugin_loader import PluginLoaderControl

setting_data = {
    # 加载优先级,数字越大优先级越高
    "priority": 0,
    # 插件是否可用启用
    "load": True,
    # 插件回调地址
    "callback_name": "test",
    # 是否阻止后续插件执行
    "prevent_other_plugins": False,
    "event": ["message"],
    # 是否在菜单隐藏,为True时将不会在简易菜单中显示
    "is_hide": True,
}
auther_data = "三三"
name_data = "简单的消息测试"
display_name_data = "测试"
version_data = "1.0"
description_data = "简单的消息测试"
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
async def test(websocket: object, MessageData: GroupMassageData):
    # 开发者命令
    if MessageData.Message[0] == "测试":

        await MessageApi.sendGroupMessage(
            websocket,
            MessageData,
            "当前插件数量{},插件加载耗时{:.4f}秒".format(
                PluginLoaderControl.plugin_num, PluginLoaderControl.plugin_load_time
            ),
        )
