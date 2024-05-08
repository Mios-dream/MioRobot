from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi


plugin = Plugin(
    auther="三三",
    name="复读机",
    version="1.0",
    description="复读机",
    setting={
        # 加载优先级,数字越大优先级越高
        "priority": 0,
        # 插件是否可用启用
        "load": False,
        # 插件回调地址
        "callback_name": "fudu",
        # 是否阻止后续插件执行
        "prevent_other_plugins": False,
        "event": ["message"],
    },
)


temp = {}


@plugin.register
async def fudu(websocket: object, MessageData: GroupMassageData):

    if MessageData.Message[0]:
        # 查询QQ是否在复读机缓存中
        if MessageData.QQ in temp.keys():
            # 判断是否是复读，只根据QQ判断
            if temp[MessageData.QQ] == MessageData.Message[0]:
                # 发送复读
                await MessageApi.sendGroupMessage(
                    websocket, MessageData, MessageData.Message[0]
                )
            else:
                # 缓存消息
                temp[MessageData.QQ] = MessageData.Message[0]
        else:
            # 缓存消息
            temp[MessageData.QQ] = MessageData.Message[0]

        # 清除缓存，防止内存溢出
        if len(temp) > 1000:
            temp.clear()
