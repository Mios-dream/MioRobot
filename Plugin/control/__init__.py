from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
from plugin_loader import PluginLoaderControl
from log import Log


plugin = Plugin(
    auther="三三",
    name="插件重载插件",
    version="1.0",
    description="重载插件",
    setting={
        # 加载优先级,数字越大优先级越高
        "priority": 100,
        # 插件是否可用启用
        "load": True,
        # 插件回调地址
        "callback_name": "Control",
        # 是否阻止后续插件执行
        "prevent_other_plugins": False,
        "event": ["message"],
    },
)


@plugin.register
async def Control(webscoket: object, MessageData: GroupMassageData) -> None:
    # 开发者命令
    if MessageData.Message[0] == "#重载":
        try:

            PluginLoaderControl.reload()
            await MessageApi.sendGroupMessage(webscoket, MessageData, "重载完成啦！")
            return 0

        except Exception as e:
            Log.error(f"重载失败,错误信息：{e}")
