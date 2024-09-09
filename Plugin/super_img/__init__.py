from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
from Plugin.super_img.super import do_super_resolution, running
import base64
import aiohttp
import json

setdata = {
    # 加载优先级,数字越大优先级越高
    "priority": 0,
    # 插件是否可用启用
    "load": True,
    # 插件回调地址
    "callback_name": "super_img",
    # 是否阻止其他插件执行
    "prevent_other_plugins": False,
    "event": ["message"],
}

plugin = Plugin(
    auther="三三",
    name="图片超分",
    version="1.0",
    description="超分图片",
    display_name="图片超分",
    setting=setdata,
    developer_setting={
        # 允许高耗时操作
        "allow_high_time_cost": True,
    },
)


@plugin.register
async def super_img(websocket: object, MessageData: GroupMassageData):
    # 读取qq缓存
    with open("Plugin/super_img/cacha/cacha.json", "r+") as f:
        data = json.loads(f.read())
        f.close()
    # 强制转换成字符串，防止错误读取
    QQ = str(MessageData.QQ)

    if MessageData.Message[0] == "图片超分":
        if running:
            await MessageApi.sendGroupMessage(
                websocket, MessageData, "还有图片正在超分，请阁下再等一下吧"
            )
            return 0
        if MessageData.Images:
            data[QQ] = False
            with open("Plugin/super_img/cacha/cacha.json", "w+") as f:
                f.write(json.dumps(data))
                f.close()

            await MessageApi.sendGroupMessage(websocket, MessageData, "图片正在处理中")
            async with aiohttp.ClientSession() as session:
                async with session.get(url=MessageData.Images[0]) as resp:
                    img_data = await resp.read()
            if img_data:
                img_data = await do_super_resolution(img_data)
                if isinstance(img_data, str):
                    await MessageApi.sendGroupMessage(
                        websocket, MessageData, "超分失败，图片太大"
                    )
                else:
                    img_data = base64.b64encode(img_data).decode()

                    await MessageApi.sendGroupMessage(
                        websocket, MessageData, CQcode.img(f"base64://{img_data}")
                    )
            else:
                await MessageApi.sendGroupMessage(
                    websocket, MessageData, "图片url存在问题，请稍后重试"
                )

        else:
            await MessageApi.sendGroupMessage(websocket, MessageData, "阁下请携带图片")
            data[QQ] = True
            with open("Plugin/super_img/cacha/cacha.json", "w+") as f:
                f.write(json.dumps(data))
                f.close()

    elif data.get(QQ, False):

        if MessageData.Images:
            data[QQ] = False
            with open("Plugin/super_img/cacha/cacha.json", "w+") as f:
                f.write(json.dumps(data))
                f.close()

            await MessageApi.sendGroupMessage(websocket, MessageData, "图片正在处理中")
            # await MessageApi.sendGroupMessage(
            #     websocket, MessageData, MessageData.Images[0]
            # )
            async with aiohttp.ClientSession() as session:
                async with session.get(url=MessageData.Images[0]) as resp:
                    img_data = await resp.read()
            if img_data:
                img_data = await do_super_resolution(img_data)
                if isinstance(img_data, str):
                    await MessageApi.sendGroupMessage(
                        websocket, MessageData, "超分失败，图片太大"
                    )
                else:
                    img_data = base64.b64encode(img_data).decode()

                    await MessageApi.sendGroupMessage(
                        websocket, MessageData, CQcode.img(f"base64://{img_data}")
                    )
            else:
                await MessageApi.sendGroupMessage(
                    websocket, MessageData, "图片url存在问题，请稍后重试"
                )

        else:
            data[QQ] = False
            with open("Plugin/super_img/cacha/cacha.json", "w+") as f:
                f.write(json.dumps(data))
                f.close()
