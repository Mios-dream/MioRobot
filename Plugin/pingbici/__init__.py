from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from Models.Api.BaseApi import RequestApi, ApiAdapter
from DataType.CQcode import CQcode

plugin = Plugin(
    auther="ranfey",
    name="屏蔽词",
    display_name="屏蔽词",
    version="1.0",
    description="屏蔽词",
    setting={
        # 加载优先级,数字越大优先级越高
        "priority": 100,
        # 插件是否可用启用
        "load": True,
        # 插件回调地址
        "callback_name": "pingbici",
        # 是否阻止后续插件执行
        "prevent_other_plugins": False,
        "event": ["message"],
    },
)

chi = "飞公主"


@plugin.register
async def pingbici(websocket: object, MessageData: GroupMassageData):
    # 开发者命令
    if chi in MessageData.Message[0]:
        api = "delete_msg"
        param = {"message_id": MessageData.Message_ID}
        args = RequestApi(api, param)
        await ApiAdapter.sendActionApi(websocket, args, 5)
