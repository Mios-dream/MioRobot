from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
from Plugin.photo_tank.PhotomTank import phantom_tank_from_url

setting_data = {
    # 加载优先级,数字越大优先级越高
    "priority": 0,
    # 插件是否可用启用
    "load": True,
    # 插件回调地址
    "callback_name": "photo_tank",
    # 是否阻止后续插件执行
    "prevent_other_plugins": False,
    "event": ["message"],
}
author_data = "三三"
name_data = "幻影坦克"
display_name_data = "幻影坦克"
version_data = "1.0"
description_data = "生成幻影坦克图片"
developer_setting_data = {
    # 是否记录运行时间
    "count_runtime": False,
    # 运行时间阈值，超过则输出警告
    "runtime_threshold": 0.5,
    # 是否允许高时间消耗，如果为否，则会在运行时间过长时输出警告，警告时间默认为0.5秒
    "allow_high_time_cost": False,
}

plugin = Plugin(
    author=author_data,
    name=name_data,
    display_name=display_name_data,
    version=version_data,
    description=description_data,
    setting=setting_data,
    developer_setting=developer_setting_data,
)


@plugin.register
async def photo_tank(websocket: object, MessageData: GroupMassageData, Trigger):
    if MessageData.Message[0] == "幻影坦克":
        Trigger.run()

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

    if MessageData.Message[0] == "幻彩坦克":
        Trigger.run()
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
