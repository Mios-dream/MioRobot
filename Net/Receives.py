import websockets
import json
from init_config import Config
from log import Log
from Models.Event.EventContral import EventContral
import traceback
from plugin_loader import PluginLoaderControl
import sys


class OneBotReceive:
    plugin = None

    def __init__(self, config: Config) -> None:

        self.config = config

    async def Start(self):
        self.Websocket = await websockets.connect(self.config.Websocket)
        Log.info("websockets连接成功")
        # 导入单例插件类
        self.plugin = PluginLoaderControl
        self.plugin.loading()
        await self.Receive()

    async def Receive(self):
        while True:
            context = await self.Websocket.recv()
            if not context.isspace():
                obj = json.loads(context)
                # 输出收到的消息到控制台
                Log.adapter(obj)

                # 处理消息
                MessageData = EventContral(obj)
                try:
                    if MessageData:

                        await self.plugin.call_back(
                            self.Websocket, MessageData.Post_Type, MessageData
                        )

                except Exception as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    tb = traceback.extract_tb(exc_traceback)

                    Log.error(f"插件处理流程出错:{e}\n行号：{tb[-1][1]}")
