from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
from Plugin.photom_tank.PhotomTank import phantom_tank_from_url


plugin = Plugin(
    auther="三三",
    name="幻影坦克",
    version="1.0",
    description="生成幻影坦克图片",
    setting={
        # 加载优先级,数字越大优先级越高
        "priority": 0,
        # 插件是否可用启用
        "load": True,
        # 插件回调地址
        "callback_name": "photo_tank",
    },
)


@plugin.register
async def photo_tank(websocket: object, MessageData: GroupMassageData):
    if MessageData.Message[0] == "幻影坦克":
        if len(MessageData.Images) == 2:
            await MessageApi.sendGroupMessage(websocket, MessageData, "正在生成中...")
            imagedata = await phantom_tank_from_url(
                MessageData.Images[0], MessageData.Images[1]
            )
            await MessageApi.sendGroupMessage(
                websocket, MessageData, CQcode.img(f"base64://{imagedata}")
            )
        else:
            await MessageApi.sendGroupMessage(
                websocket, MessageData, "请阁下携带两张图片"
            )

    if MessageData.Message[0] == "幻彩坦克":
        if len(MessageData.Images) == 2:
            await MessageApi.sendGroupMessage(websocket, MessageData, "正在生成中...")
            imagedata = await phantom_tank_from_url(
                MessageData.Images[0], MessageData.Images[1], True
            )
            await MessageApi.sendGroupMessage(
                websocket, MessageData, CQcode.img(f"base64://{imagedata}")
            )
        else:
            await MessageApi.sendGroupMessage(
                websocket, MessageData, "请阁下携带两张图片"
            )
