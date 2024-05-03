from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
from Plugin.ai_chat.tts import tts_text
from Plugin.ai_chat.fastchat import chat_fastapi
import random


plugin = Plugin(
    auther="三三",
    name="澪的聊天插件",
    version="1.0",
    description="调用千问进行回复",
    setting={
        # 加载优先级,数字越大优先级越高
        "priority": 0,
        # 插件是否可用启用
        "load": True,
        # 插件回调地址
        "callback_name": "AiChat",
        # 是否阻止后续插件执行
        "prevent_other_plugins": False,
        "event": ["message"],
    },
)


@plugin.register
async def AiChat(webscoket: object, MessageData: GroupMassageData) -> None:
    # 以/开头为指令
    if MessageData.Message[0]:
        if MessageData.Message[0][0] == "/":
            # 调用fastchat进行回复
            response = await chat_fastapi(MessageData.Message[0][1:])
            # 回复语音的概率
            random_num = 0.3
            # 如果回复超过30字或者随机数小于0.3则只回复文字
            if (len(response.encode("utf-8")) // 4 > 30) or (
                random.random() >= random_num
            ):
                await MessageApi.sendGroupMessage(
                    webscoket, MessageData, f"{CQcode.at(MessageData.QQ)} {response}"
                ),

            else:
                url = await tts_text(response)

                await MessageApi.sendGroupMessage(
                    webscoket, MessageData, CQcode.record(url)
                )

    # 以@机器人 为指令
    if MessageData.At:
        if MessageData.At[0] == MessageData.Robot:

            # 调用fastchat进行回复
            response = await chat_fastapi(MessageData.Message[0])
            # 回复语音的概率
            random_num = 0

            # 如果回复超过30字或者随机数小于0.3则只回复文字
            if (len(response.encode("utf-8")) // 4 > 30) or (
                random.random() >= random_num
            ):

                await MessageApi.sendGroupMessage(
                    webscoket, MessageData, f"{CQcode.at(MessageData.QQ)} {response}"
                ),

            else:
                url = await tts_text(response)

                await MessageApi.sendGroupMessage(
                    webscoket, MessageData, CQcode.record(url)
                )
