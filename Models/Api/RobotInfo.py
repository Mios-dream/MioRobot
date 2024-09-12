import websockets
from Models.Api.BaseApi import RequestApi, ApiAdapter
import json


class RobotInfo:

    @staticmethod
    async def get_robot_info():
        """
        获取机器人信息
        """
        raise NotImplementedError

    @staticmethod
    async def get_group_list(websocket: websockets.WebSocketClientProtocol) -> str:

        param = {"no_cache": False}
        args = RequestApi("get_group_list", param)
        return await ApiAdapter.sendActionApi(websocket, args, 5)
