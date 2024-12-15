import os
import importlib.util
import sys
from typing import Any
from types import ModuleType
from Utils.Logs import Log
from DataType.MessageData import MessageData
import traceback
import time
from websockets import WebSocketServerProtocol
from Plugin import *


class PluginTrigger:
    """
    标记插件的触发
    """

    callbackName: str
    runtime: list[float] = []

    def __init__(self, callbackName: str):
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
    _pluginPath: str = "Plugin"
    # 插件调用优先级字典
    pluginList: dict[str, int] = {}
    # 插件对象字典
    pluginObjectList: dict[str, Plugin] = {}

    # 加载的插件数量
    pluginNum: int = 0

    # 触发记录对象列表
    pluginRunCount: dict[str, int] = {}

    # 全部插件初始化加载时间
    pluginLoadTime: float = 0

    # 全部插件调用耗时记录
    pluginCallTimeAll: float = 0

    # 单插件调用耗时记录
    pluginCallTime: dict[str, float] = {}

    def __new__(cls, *args: Any, **kwargs: Any):
        if not cls._instance:
            cls._instance = super(PluginLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):  # 防止__init__方法的重复调用
            self._initialized = True

    def _loadPluginsFromDir(self) -> dict[str, ModuleType]:
        """
        从指定路径加载插件
        读取插件目录，返回一个字典，键为插件名称，值为插件模块

        Return: dict[str, ModuleType]
        """
        modules: dict[str, ModuleType] = {}
        for pluginName in os.listdir(self._pluginPath):
            fullPath = os.path.join(self._pluginPath, pluginName)
            try:
                if os.path.isdir(fullPath) and os.path.isfile(
                    os.path.join(fullPath, "__init__.py")
                ):

                    moduleName = f"{os.path.basename(self._pluginPath)}.{pluginName}"
                    spec = importlib.util.spec_from_file_location(
                        moduleName, os.path.join(fullPath, "__init__.py")
                    )
                    if spec is None:
                        Log.error(f"无法找到模块 {moduleName} 的规格")
                        continue
                    if spec.loader is None:
                        Log.error(f"模块 {moduleName} 的加载器为 None")
                        continue
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    modules[moduleName] = module

            except Exception as e:
                _, _, exc_traceback = sys.exc_info()
                tb = traceback.extract_tb(exc_traceback)
                Log.pluginError(
                    pluginName,
                    f"加载插件 {pluginName} 失败。\n文件路径: {tb[-1].filename} \n行号：{tb[-1].lineno} \n错误源码:{traceback.format_exc()}\n错误信息为: {e}",
                )

        return modules

    # def _callMethodInClasses(self, classes: dict[str, Any], method_name: str, *args: Any, **kwargs: Any) -> dict[str, Any]:
    #     """
    #     调用类中的方法
    #     parameters：
    #     classes: Dict[str, Any] 类字典
    #     method_name: str 方法名
    #     args: Any 参数列表
    #     kwargs: Any 关键字参数

    #     Return: dict[str, Any] 方法返回值
    #     """
    #     results: dict[str, Any] = {}
    #     for class_name, instance in classes.items():
    #         method = getattr(instance, method_name, None)
    #         if callable(method):
    #             results[class_name] = method(*args, **kwargs)
    #         else:
    #             Log.error(f"{method_name}方法在类{class_name}中不存在")
    #     return results

    def _loadClassesFromModule(self, module: ModuleType) -> Plugin | None:
        """
        从模块中加载继承自指定基类的所有类
        parameters：
        module: ModuleType 模块

        Return:  Plugin | None 类对象
        """
        instance: Plugin | None = None
        for name, obj in module.__dict__.items():
            if isinstance(obj, type) and issubclass(obj, Plugin) and obj is not Plugin:
                try:
                    instance = obj()
                except Exception as e:
                    _, _, exc_traceback = sys.exc_info()
                    tb = traceback.extract_tb(exc_traceback)

                    Log.error(
                        f"实例化类 {name} 失败。\n文件路径: {tb[-1].filename} \n行号：{tb[-1].lineno} \n错误源码:{traceback.format_exc()}\n错误信息为: {e}",
                    )

                break
        return instance

    def reloadPlugins(self) -> None:
        """
        热重载插件
        """
        # 清空现有插件数据
        self.pluginObjectList.clear()
        self.pluginList.clear()
        self.pluginNum = 0
        self.pluginLoadTime = 0
        self.pluginCallTimeAll = 0
        self.pluginCallTime.clear()

        # 统计加载插件的时间
        startTime = time.time()

        # 重新加载插件
        for pluginName, pluginModel in self._loadPluginsFromDir().items():
            try:
                # 动态重新加载模块
                importlib.reload(pluginModel)
                # 加载模块中的类
                classes = self._loadClassesFromModule(pluginModel)
                if classes is None:
                    continue
                if classes.init():
                    Log.error(f"插件 {pluginName} 配置信息初始化失败")
                    continue
                # 添加到插件对象列表
                self.pluginObjectList[pluginName] = classes
                # 添加到插件调用优先级列表
                self.pluginList[pluginName] = classes.setting.priority
                # 插件数量增加
                self.pluginNum += 1
            except Exception as e:
                Log.error(
                    f"插件 {pluginName} 初始化失败，请检查插件是否正确安装，错误信息为：{e}"
                )
                continue

        # 将插件按照优先级排序
        self.pluginList = dict(
            sorted(self.pluginList.items(), key=lambda item: item[1], reverse=True)
        )
        # 统计插件加载时间
        self.pluginLoadTime = time.time() - startTime
        Log.info(f"成功重新加载了{self.pluginNum}个插件")
        Log.info(f"重新加载插件耗时: {self.pluginLoadTime}秒")

    # def load(self) -> None:
    #     """
    #     加载插件
    #     """
    #     # 统计加载插件的时间
    #     startTime = time.time()

    #     for pluginName, pluginModel in self._loadPluginsFromDir().items():
    #         try:
    #             # 加载模块中的类
    #             classes = self._loadClassesFromModule(pluginModel)
    #             if classes is None:
    #                 continue
    #             # 添加到插件对象列表
    #             self.pluginObjectList[pluginName] = classes
    #             # 添加到插件调用优先级列表
    #             self.pluginList[pluginName] = classes.setting.priority
    #             # 插件数量增加
    #             self.pluginNum += 1
    #         except Exception as e:
    #             Log.error(f"插件 {pluginName} 初始化失败，请检查插件是否正确安装，错误信息为：{e}")
    #             continue

    #     # 将插件按照优先级排序
    #     self.pluginList = dict(
    #         sorted(self.pluginList.items(),
    #                key=lambda item: item[1], reverse=True)
    #     )
    #     # 统计插件加载时间
    #     self.pluginLoadTime = time.time() - startTime
    #     Log.info(f"成功加载了{self.pluginNum}个插件")
    #     Log.info(f"加载插件耗时: {self.pluginLoadTime}秒")

    async def callBack(
        self,
        PostType: EventType,
        data: MessageData,
    ) -> None:
        """
        调用插件
        """

        for pluginName, pluginModel in self.pluginObjectList:
            try:

                if await self.pluginObjectList[pluginName].run():
                    # 调用插件
                    if not (await self.pluginObjectList[pluginName].dispose()):
                        Log.error(f"插件 {pluginName} 运行失败")
                        continue
                    if pluginName not in self.pluginRunCount:
                        self.pluginRunCount[pluginName] = 0
                    self.pluginRunCount[pluginName] += 1
                    Log.info(f"插件{pluginName}调用成功")
            except Exception as e:
                Log.error(
                    msg=f"插件 {pluginName} 失败，请检查插件是否正确使用，错误信息为：{e}"
                )
                continue


# 单例初始化
PluginLoaderControl = PluginLoader()
