import os
from importlib import import_module, reload
from typing import Any
from Utils.Logs import Log
from DataType.MessageData import MessageData
import traceback
import sys
import time
import websockets


class Plugin_trigger:
    """
    标记插件的触发
    """

    callbackName: str
    runtime: list[float] = []

    def __init__(self, callbackName:str):
        self.callbackName = callbackName

    def run(self):
        self.runtime.append(time.time())


class PluginLoader:
    """
    插件加载器
    """

    # 单例模式
    _instance = None
    # 插件路径
    _plugin_path_list = os.listdir("Plugin")
    # 插件对象字典
    plugin_list = {}
    # 插件回调函数名列表,用于检查重复
    plugin_name_list = []

    # 加载的插件数量
    plugin_num = 0

    # 触发记录对象列表
    trigger_list = {}

    # 性能警告阈值,单位为秒
    performance_warning_threshold = 1
    # 全部插件初始化加载时间
    plugin_load_time = 0

    # 全部插件调用耗时记录
    plugin_call_time_all = 0

    # 单插件调用耗时记录
    plugin_call_time = {}

    def __new__(cls, *args:Any, **kwargs:Any):
        if not cls._instance:
            cls._instance = super(PluginLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):  # 防止__init__方法的重复调用
            self._plugin_path_list = os.listdir("Plugin")
            self.plugin_list = {}
            self.plugin_name_list = []
            self.plugin_num = 0
            self._initialized = True

    def loading(self) -> None:
        """
        加载插件
        """
        # 统计加载插件的时间
        start_time = time.time()

        for plugin_name in self._plugin_path_list:
            try:
                # 导入模块
                plugin_model = reload(import_module(f"Plugin.{plugin_name}"))
                # 获取优先级
                priority = plugin_model.plugin.setting["priority"]
                # 获取回调函数名
                callback_name = plugin_model.plugin.setting["callback_name"]

                self.trigger_list[callback_name] = Plugin_trigger(callback_name)

                # 检查是否开启插件
                if not plugin_model.plugin.setting["load"]:
                    Log.info(f"插件 {plugin_name} 未开启,跳过加载")
                    continue

                # 检查是否存在回调函数
                if not hasattr(plugin_model, callback_name):
                    Log.plugin_error(
                        plugin_name,
                        f"在加载({plugin_name})时，发现回调函数{callback_name}不存在，请检查回调函数名",
                    )
                    continue

                # 检查是否重复
                if plugin_name in self.plugin_name_list:
                    Log.plugin_error(
                        plugin_name,
                        f"在加载{plugin_name}时，发现重复的回调函数名{callback_name},请修改回调函数名,确保其唯一",
                    )
                    continue

                # 将插件实例添加到字典中
                self.plugin_list[plugin_model] = priority

                # 记录回调函数名
                self.plugin_name_list.append(callback_name)

                # 记录加载的插件数量
                self.plugin_num += 1

            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                tb = traceback.extract_tb(exc_traceback)

                Log.plugin_error(
                    plugin_name,
                    f"加载插件 {plugin_name} 失败。\n文件路径: {tb[-1].filename} \n行号：{tb[-1].lineno} \n错误源码:{traceback.format_exc()}\n错误信息为: {e}",
                )

        # 将插件按照优先级排序
        self.plugin_list = dict(
            sorted(self.plugin_list.items(), key=lambda item: item[1], reverse=True)
        )
        Log.info(f"成功加载了{self.plugin_num}个插件")

        self.plugin_load_time = time.time() - start_time
        Log.info(f"加载插件耗时: {self.plugin_load_time}秒")

    def reload(self) -> None:
        """
        重新加载插件
        """
        # 删除旧插件
        # 插件路径
        self._plugin_path_list = os.listdir("Plugin")

        # 插件回调函数对象字典
        self.plugin_list = {}
        # 插件回调函数名列表,用于检查重复
        self.plugin_name_list = []
        # 全部插件调用耗时记录
        self.plugin_call_time = {}
        # 加载的插件数量
        self.plugin_num = 0

        Log.info("正在重新加载插件")

        # 重新加载插件
        self.loading()

        Log.info("重载成功")

    async def call_back(
        self,
        websocket: websockets.WebSocketClientProtocol,
        Post_Type: str,
        data: MessageData,
    ) -> None:
        """
        调用插件
        """

        # 统计插件调用的时间
        start_time = time.time()
        # 遍历插件回调函数对象字典
        for plugin_model in self.plugin_list.keys():

            try:
                # 获取插件名
                plugin_name:str = plugin_model.plugin.name
                # 获取回调函数名
                callback_name = plugin_model.plugin.setting["callback_name"]
                # 获取开发者设置
                developer_setting = plugin_model.plugin.developer_setting
                # 判断是否在插件的监听事件中
                if Post_Type in plugin_model.plugin.setting["event"]:

                    # 记录插件运行时间
                    if plugin_model.plugin.developer_setting["count_runtime"]:
                        start_time = time.time()

                    # 调用插件
                    callback = eval(f"plugin_model.{callback_name}")
                    code = await callback(
                        websocket, data, self.trigger_list[callback_name]
                    )

                    # 记录插件运行时间
                    if developer_setting["count_runtime"]:
                        # 统计插件运行时间
                        runtime = time.time() - start_time
                        # 将插件运行时间添加到字典中
                        self.plugin_call_time[plugin_name] = runtime
                        if (
                            runtime > developer_setting["runtime_threshold"]
                            and not developer_setting["allow_high_time_cost"]
                        ):
                            Log.warning(
                                f"插件({plugin_name})运行耗时: {runtime}秒,性能较低，请检查插件!"
                            )

                    # 判断检查，是否有插件返回了非0的状态码
                    # 0为触发，1为未触发，-1为插件错误
                    if code == 0:
                        # 触发并中断后续插件的调用
                        Log.info(f"插件({plugin_name})触发成功")
                        break
                    elif code == -1:
                        # 插件错误
                        Log.plugin_error(
                            plugin_name,
                            f"插件({plugin_name})触发失败,插件内部错误",
                        )
                        break

            except Exception as e:
                _exc_type, _exc_value, exc_traceback = sys.exc_info()
                tb = traceback.extract_tb(exc_traceback)

                Log.plugin_error(
                    plugin_name,
                    f"调用插件 {plugin_name} 失败。\n文件路径: {tb[-1].filename} \n行号：{tb[-1].lineno} \n错误源码:{traceback.format_exc()}\n错误信息为: {e}",
                )

        # 统计插件调用的时间
        self.plugin_call_time = time.time() - start_time
        if self.plugin_call_time > self.performance_warning_threshold:
            Log.warning(
                f"插件调用耗时: {self.plugin_call_time}秒,性能较低，请检查插件!"
            )


# 单例初始化
PluginLoaderControl = PluginLoader()
