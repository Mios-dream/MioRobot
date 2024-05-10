import websockets
import json
from init_config import Config
from log import Log
from Models.Event.EventContral import EventContral
import traceback
from plugin_loader import PluginLoaderControl
import sys
import time


class OneBotReceive:
    plugin = None

    def __init__(self, config: Config) -> None:

        self.config = config

    async def Start(self):
        try:
            self.Websocket = await websockets.connect(self.config.Websocket)
            Log.info("websockets连接成功")
            # 导入单例插件类
            self.plugin = PluginLoaderControl
            # 调用插件的初始化方法
            self.plugin.loading()

            await self.Receive()
        except Exception as e:
            Log.error("websockets连接失败，请检查配置")
            Log.info("将在10秒后尝试重新连接")
            time.sleep(10)
            await self.Start()

    async def Receive(self):
        while True:
            # 接收消息
            context = await self.Websocket.recv()
            # 判断是否为空
            if not context.isspace():
                # 将收到的消息转换为json对象
                obj = json.loads(context)
                # 输出收到的消息到控制台
                Log.adapter(obj)

                # 处理消息
                MessageData = EventContral(obj)
                try:
                    if MessageData:
                        # 调用插件的接收方法
                        await self.plugin.call_back(
                            self.Websocket, MessageData.Post_Type, MessageData
                        )

                except Exception as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    tb = traceback.extract_tb(exc_traceback)

                    Log.error(f"插件处理流程出错:{e}\n行号：{tb[-1][1]}")
