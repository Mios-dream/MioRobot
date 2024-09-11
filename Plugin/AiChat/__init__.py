from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
from Plugin.AiChat.tts import tts_text
from Plugin.AiChat.fastchat import chat_fastapi
import random

setting_data = {
    # 加载优先级,数字越大优先级越高
    "priority": 0,
    # 插件是否可用启用
    "load": True,
    # 插件回调地址
    "callback_name": "AiChat",
    # 是否阻止后续插件执行
    "prevent_other_plugins": False,
    "event": ["message"],
    "is_hide": False,
}
auther_data = "三三"
name_data = "澪的聊天插件"
display_name_data = "澪的聊天"
version_data = "1.0"
description_data = "调用千问进行回复"
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
async def AiChat(websocket: object, MessageData: GroupMassageData, Trigger) -> None:
    # 以/开头为指令
    if MessageData.Message[0]:
        if MessageData.Message[0][0] == "/":
            Trigger.run()
            # 调用fastchat进行回复
            response = await chat_fastapi(MessageData.Message[0][1:])
            # 回复语音的概率
            random_num = 0
            # 如果回复超过30字或者随机数小于0.3则只回复文字
            if (len(response.encode("utf-8")) // 4 > 30) or (
                random.random() >= random_num
            ):
                await MessageApi.sendGroupMessage(
                    websocket, MessageData, f"{CQcode.at(MessageData.QQ)} {response}"
                ),

            else:
                url = await tts_text(response)

                await MessageApi.sendGroupMessage(
                    websocket, MessageData, CQcode.record(url)
                )
            # 中断后续回复
            return 0

    # 以@机器人 为指令
    if MessageData.At:
        if MessageData.At[0] == MessageData.Robot:
            Trigger.run()

            # 调用fastchat进行回复
            response = await chat_fastapi(MessageData.Message[0])
            # 回复语音的概率
            random_num = 0

            # 如果回复超过30字或者随机数小于0.3则只回复文字
            if (len(response.encode("utf-8")) // 4 > 30) or (
                random.random() >= random_num
            ):

                await MessageApi.sendGroupMessage(
                    websocket, MessageData, f"{CQcode.at(MessageData.QQ)} {response}"
                ),

            else:
                url = await tts_text(response)

                await MessageApi.sendGroupMessage(
                    websocket, MessageData, CQcode.record(url)
                )
            # 中断后续回复
            return 0
