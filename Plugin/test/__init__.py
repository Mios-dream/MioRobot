from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from plugin_loader import PluginLoaderControl

plugin = Plugin(
    auther="三三",
    name="简单的消息测试",
    version="1.0",
    description="简单的消息测试",
    setting={
        # 加载优先级,数字越大优先级越高
        "priority": 0,
        # 插件是否可用启用
        "load": True,
        # 插件回调地址
        "callback_name": "test",
        # 是否阻止后续插件执行
        "prevent_other_plugins": False,
        "event": ["message"],
    },
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
