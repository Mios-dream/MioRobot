from Models.Context.MessageContextBuild import MessageContextBuild
from Models.Event.EventControl import EventAdapter
from Core.GroupControl import GroupControl
from Core.PluginLoader import PluginLoader, PluginLoaderControl
from Core.config import Config
from Utils.WebsocketControl import WebsocketControl
from Net.AppHttp import appHttp
from Utils.Logs import Log
import sys
import time
import uvicorn
import traceback
import asyncio


class CoreServer:
    """
    核心服务用于启动
    ws连接
    apiHttp连接
    """

    # 插件加载器实例
    plugin: PluginLoader
    # 配置信息
    config: Config

    def __init__(self, config: Config):
        self.config = config

    async def start(self):
        """
        启动ws连接
        """
        try:
            # 连接websocket
            await WebsocketControl.connect(config)
            # 导入单例插件类
            self.plugin = PluginLoaderControl
            # 调用插件的初始化方法
            self.plugin.loading()
            # 初始化群管理类
            GroupControl.init(self.plugin.getPluginsName())
            # 调用接受方法
            await self.receive()

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb = traceback.extract_tb(exc_traceback)
            # 查看详细错误信息
            Log.error(
                f"ws连接错误\n文件路径: {tb[-1].filename} \n行号：{tb[-1].lineno} \n错误源码:{traceback.format_exc()}\n错误信息为: {e}"
            )
            Log.error("websockets连接失败，请检查配置")
            Log.info("将在10秒后尝试重新连接")
            time.sleep(10)
            await self.start()

    async def httpStart(self):
        """
        开启http管理服务
        """
        retry_count = 0
        MAX_RETRIES = 3

        while retry_count < MAX_RETRIES:
            try:
                Log.info("正在开启 API 服务......")

                # 创建 uvicorn 配置
                config = uvicorn.Config(
                    appHttp,
                    host="0.0.0.0",
                    port=int(self.config.uvicornPort),
                    reload=False,
                )

                # 创建服务器实例
                server = uvicorn.Server(config)

                # 在后台任务中运行服务器
                self._http_task = asyncio.create_task(server.serve())
                await self._http_task

            except asyncio.CancelledError:
                Log.info("HTTP 服务被取消")
                break
            except KeyboardInterrupt:
                Log.info("HTTP 服务接收到键盘中断")
                break
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                tb = traceback.extract_tb(exc_traceback)
                Log.error(
                    f"HTTP 服务启动失败\n文件路径: {tb[-1].filename} \n行号: {tb[-1].lineno}\n错误信息: {e}"
                )
                retry_count += 1

                if retry_count < MAX_RETRIES:
                    Log.info(
                        f"将在10秒后尝试重新连接 (尝试次数: {retry_count}/{MAX_RETRIES})"
                    )
                    # 使用可中断的等待
                    try:
                        await asyncio.wait_for(asyncio.sleep(10), timeout=None)
                    except KeyboardInterrupt:
                        break
                else:
                    Log.error("达到最大重试次数，放弃启动 HTTP 服务")
                    break

        if retry_count >= MAX_RETRIES:
            raise Exception("HTTP 服务启动失败")

    async def receive(self):
        """
        接收消息
        """
        while True:
            # 接收消息
            context: str = await WebsocketControl.websocket.recv()  # type: ignore
            # 判断是否为空
            if context.isspace():
                continue

            # 处理消息
            messageData = EventAdapter.EventControl(context)
            # 构建消息上下文
            messageContext = MessageContextBuild.build(messageData)
            # 过滤错误消息
            if messageContext is None:
                continue

            try:
                # 调用插件
                await self.plugin.callBack(messageContext)

            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                tb = traceback.extract_tb(exc_traceback)

                Log.error(
                    f"插件处理流程出错\n文件路径: {tb[-1].filename} \n行号：{tb[-1].lineno} \n错误源码:{traceback.format_exc()}\n错误信息为: {e}"
                )


config = Config()
coreServer = CoreServer(config)
