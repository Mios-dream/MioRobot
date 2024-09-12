from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
from Plugin.photom_tank.PhotomTank import phantom_tank_from_url
import websockets
from Plugin.menu.TextMenu import TextMenu


plugin = Plugin(
    auther="三三",
    name="幻影坦克",
    display_name="幻影坦克",
    version="1.0",
    description="生成幻影坦克图片",
    setting={
        # 加载优先级,数字越大优先级越高
        "priority": 0,
        # 插件是否可用启用
        "load": True,
        # 插件回调地址
        "callback_name": "photo_tank",
        # 是否阻止后续插件执行
        "prevent_other_plugins": False,
        "event": ["message"],
    },
)


@plugin.register
async def photo_tank(
    websocket: websockets.WebSocketClientProtocol, MessageData: GroupMassageData
):

    if MessageData.Message[0] == "幻影坦克":
        data = TextMenu(["生成幻影坦克", "生成幻彩坦克"], add_yiyan=False)
        await MessageApi.sendGroupMessage(websocket, MessageData, data.show_menu())

    if MessageData.Message[0] == "生成幻影坦克":
        # 如果图片数量大于等于2
        if len(MessageData.Images) == 2:

            await MessageApi.sendGroupMessage(websocket, MessageData, "正在生成中...")
            # 生成图片
            imagedata = await phantom_tank_from_url(
                MessageData.Images[0], MessageData.Images[1]
            )

            # 发送图片
            await MessageApi.sendGroupMessage(
                websocket, MessageData, CQcode.img(f"base64://{imagedata}")
            )
        else:
            await MessageApi.sendGroupMessage(
                websocket, MessageData, "请阁下携带两张图片"
            )
        # 中断后续回复
        return 0

    if MessageData.Message[0] == "生成幻彩坦克":
        # 如果图片数量大于等于2
        if len(MessageData.Images) == 2:
            await MessageApi.sendGroupMessage(websocket, MessageData, "正在生成中...")
            # 生成图片
            imagedata = await phantom_tank_from_url(
                MessageData.Images[0], MessageData.Images[1], True
            )
            # 发送图片
            await MessageApi.sendGroupMessage(
                websocket, MessageData, CQcode.img(f"base64://{imagedata}")
            )
        else:
            await MessageApi.sendGroupMessage(
                websocket, MessageData, "请阁下携带两张图片"
            )

        # 中断后续回复
        return 0
