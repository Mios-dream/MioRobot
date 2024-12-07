from typing import Union
from DataType.GroupMassageData import GroupMassageData
import asyncio
import json
from Utils.Logs import Log
import websockets
from Models.Api.BaseApi import RequestApi, ApiAdapter


class MessageApi:

    def __init__(self) -> None:
        pass

    @staticmethod
    async def sendGroupMessage(
        websocket: websockets.WebSocketClientProtocol,
        MessageData: GroupMassageData,
        message: Union[str, list, list[dict]],
        is_node: bool = False,
    ) -> str:
        """
        发送群消息
        @param websocket: websocket对象
        @param MessageData: 群消息数据
        @param message: 要发送是消息内容
        @param is_node: 是否为转发消息

        @return: 接口返回结果

        说明：
        当message为字符串时，直接发送字符串

        当message为列表时，依次发送列表中的消息，间隔一秒

        当message为字典时，发送字典中的消息，字典中必须包含"message"键
        值为要发送的消息内容，time为发送消息的时间间隔，默认为1秒

        当is_node为True时，发送节点消息，message为字符串或列表，字符串时为单条消息，列表时为多条转发消息
        """
        # 实现发送消息的逻辑
        api = "send_group_msg" if not is_node else "send_group_forward_msg"

        # 判断是否为转发消息
        if not is_node:
            # 判断message是否为字符串
            if isinstance(message, (str, int, float, bool)):
                # 构建消息
                param = {"message": message, "group_id": MessageData.Group}
                args = RequestApi(api, param)
                return await ApiAdapter.sendActionApi(websocket, args, 5)

            # 判断message是否为列表
            elif all(isinstance(item, (str, int, float)) for item in message):
                # 依次发送列表中的消息，间隔一秒
                for item in message:
                    # 构建消息
                    param = {"message": item, "group_id": MessageData.Group}
                    args = RequestApi(api, param)
                    response = await ApiAdapter.sendActionApi(websocket, args, 5)
                    # 等待一秒，或许无用？
                    await asyncio.sleep(1)
                return response
            # 判断message是否为字典
            elif all(isinstance(item, dict) for item in message):
                # 发送字典中的消息，自定义时间间隔
                for item in message:
                    # 构建消息
                    param = {"message": item["message"], "group_id": MessageData.Group}
                    args = RequestApi(api, param)
                    response = await ApiAdapter.sendActionApi(websocket, args, 5)
                    # 等待一秒，或许无用？
                    await asyncio.sleep(item.get("time", 1))
                return response
            else:
                Log.error("发送的消息不符合规范")
        else:
            # 转发消息的构建
            messagechains = []
            messagedata = {
                "type": "node",
                "data": {"content": ""},
            }
            # 判断message是否为字符串
            if isinstance(message, (str, int, float, bool)):
                messagedata["data"]["content"] = message
                messagechains.append(messagedata)
                # 构建消息
                param = {"message": messagechains, "group_id": MessageData.Group}
                args = RequestApi(api, param)
                return await ApiAdapter.sendActionApi(websocket, args, 5)
            # 判断message是否为列表
            elif all(isinstance(item, (str, int, float)) for item in message):

                for item in message:
                    messagedata["data"]["content"] = item
                    messagechains.append(messagedata)
                # 构建消息
                param = {"message": messagechains, "group_id": MessageData.Group}
                args = RequestApi(api, param)
                return await ApiAdapter.sendActionApi(websocket, args, 5)

            else:
                Log.error("发送的消息不符合规范")

    @staticmethod
    async def sendPrivateMessage(
        websocket: object,
        MessageData: GroupMassageData,
        message: Union[str, list, list[dict]],
        is_node: bool = False,
    ):
        raise NotImplementedError
