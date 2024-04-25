import websockets
import json
from init_config import Config
from log import Log
from Models.Event.EventContral import EventContral
import traceback
from plugin_loader import PluginLoader
import sys


class OneBotReceive:
    plugin = None

    def __init__(self, config: Config) -> None:

        self.config = config

    async def SendMessage(self, msg):
        await self.Websocket.send(msg)

    async def Start(self):
        self.Websocket = await websockets.connect(self.config.Websocket)
        Log.info("websockets连接成功")
        self.plugin = PluginLoader(self.Websocket)
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
                        if MessageData.Post_Type == "message":

                            # 开发者命令
                            if MessageData.Message[0] == "#重载":
                                self.plugin.reload()

                                print("重载成功")

                            await self.plugin.call_back(MessageData)

                except Exception as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    tb = traceback.extract_tb(exc_traceback)

                    Log.error(f"插件处理流程出错:{e}\n行号：{tb[-1][1]}")
