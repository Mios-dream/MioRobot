import os
from importlib import import_module, reload
from log import Log
from DataType.MessageData import MessageData
import traceback
import sys


class PluginLoader:
    """
    插件加载器
    """

    # 插件路径
    _plugin_list = os.listdir("Plugin")
    # 插件回调函数对象字典
    _plugin_recall_list = {}
    # 插件回调函数名列表,用于检查重复
    plugin_name_list = []
    # 加载的插件数量
    plugin_num = 0
    # 单例模式
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PluginLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):  # 防止__init__方法的重复调用
            self._plugin_list = os.listdir("Plugin")
            self._plugin_recall_list = {}
            self.plugin_name_list = []
            self.plugin_num = 0
            self._initialized = True

    def loading(self) -> None:
        """
        加载插件
        """
        for plugin_name in self._plugin_list:
            try:
                # 导入模块
                plugin_model = reload(import_module(f"Plugin.{plugin_name}"))

                # 获取优先级
                priority = plugin_model.plugin.setting["priority"]
                # 获取回调函数名
                callback_name = plugin_model.plugin.setting["callback_name"]

                # 检查是否开启插件
                if not plugin_model.plugin.setting["load"]:
                    Log.info(f"插件 {plugin_name} 未开启,跳过加载")
                    continue

                # 检查是否存在回调函数
                if not hasattr(plugin_model, callback_name):
                    Log.error(
                        f"在加载({plugin_name})时，发现回调函数{callback_name}不存在，请检查回调函数名"
                    )
                    continue

                # 检查是否重复
                if plugin_name in self.plugin_name_list:
                    Log.error(
                        f"在加载{plugin_name}时，发现重复的回调函数名{callback_name},请修改回调函数名,确保其唯一"
                    )
                    continue

                # 将需要回调函数的模块添加到字典中
                self._plugin_recall_list[plugin_model] = priority
                # 记录回调函数名
                self.plugin_name_list.append(callback_name)

                # 记录加载的插件数量
                self.plugin_num += 1

            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                tb = traceback.extract_tb(exc_traceback)

                Log.error(
                    f"加载插件 {plugin_name} 失败。\n行号：{tb[-1][1]}\n错误信息为: {e}"
                )

        # 按照优先级排序
        self.sorted_dict = dict(
            sorted(
                self._plugin_recall_list.items(), key=lambda item: item[1], reverse=True
            )
        )
        Log.info(f"成功加载了{self.plugin_num}个插件")

    def reload(self) -> None:
        """
        重新加载插件
        """
        # 删除旧插件
        # 插件路径
        self._plugin_list = os.listdir("Plugin")

        # 插件回调函数对象字典
        self._plugin_recall_list = {}
        # 插件回调函数名列表,用于检查重复
        self.plugin_name_list = []

        # 加载的插件数量
        self.plugin_num = 0

        Log.info("正在重新加载插件")

        # 重新加载插件
        self.loading()

        Log.info("重载成功")

    async def call_back(self, websocket, Post_Type, data: MessageData) -> None:
        """
        调用插件
        """

        # 遍历插件回调函数对象字典
        for plugin_model in self.sorted_dict.keys():

            try:
                # 获取插件名
                plugin_name = plugin_model.plugin.name
                # 获取回调函数名
                callback_name = plugin_model.plugin.setting["callback_name"]

                if Post_Type in plugin_model.plugin.setting["event"]:
                    # 调用插件
                    callback = eval(f"plugin_model.{callback_name}")
                    code = await callback(websocket, data)
                    # 判断检查是否需要中断其他插件
                    if code == 0:
                        break

                # 检查是否需要中断其他插件
                # if plugin_model.plugin.setting["prevent_other_plugins"]:
                #     break

            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                tb = traceback.extract_tb(exc_traceback)

                Log.error(
                    f"调用插件 {plugin_name} 失败。\n行号：{tb[-1][1]} \n错误信息为: {e}"
                )


# 单例初始化
PluginLoaderControl = PluginLoader()
