import uuid
import json
import asyncio
from Models.Event.EventContral import EventAdapter
import websockets
from Utils.Task import Task


class RequestApi:
    """
    API消息构建基类
    """

    echo: str
    # 请求参数
    params: object
    # 请求接口
    action: str

    def __init__(self, action, args):
        self.echo = uuid.uuid1().__str__()
        self.action = action
        self.params = args


class ApiAdapter:
    """
    发送api请求的基类
    """

    # 发送API请求
    @staticmethod
    async def sendActionApi(
        websocket: websockets.WebSocketClientProtocol, api: RequestApi, timeOut: int = 3
    ):
        # 构建API消息
        msg = json.dumps(api, default=lambda obj: obj.__dict__, ensure_ascii=False)
        # 创建任务
        task = Task(api.echo)

        # 注册回调函数
        EventAdapter.OnNext.append(task)

        # 发送API消息
        await websocket.send(msg)
        try:
            # 等待回调函数返回结果
            obj = await asyncio.wait_for(task.fut, timeout=timeOut)
            return obj
        except asyncio.TimeoutError:
            print("api请求超时")
            # 请求超时
            return None
        finally:
            # 从列队中移除
            EventAdapter.OnNext.remove(task)
