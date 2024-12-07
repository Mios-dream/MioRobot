from abc import ABC, abstractmethod
from enum import Enum


class EventType(Enum):
    GroupMessage = "GroupMessage"
    FriendMessage = "FriendMessage"


class PluginSetting:
    # 插件优先级
    _priority: int = 0
    # 是否加载
    _load: bool = True
    # 是否启用
    _enable: bool = True
    # 监听事件列表
    _event: list[EventType]
    # 是否在菜单隐藏,为True时将不会在简易菜单中显示
    _hide: bool = True

    @property
    def priority(self) -> int:
        return self._priority

    @priority.setter
    def priority(self, priority: int) -> None:
        self._priority = priority

    @property
    def load(self) -> bool:
        return self._load

    @load.setter
    def load(self, load: bool) -> None:
        self._load = load

    @property
    def enable(self) -> bool:
        return self._enable

    @enable.setter
    def enable(self, enable: bool) -> None:
        self._enable = enable

    @property
    def event(self) -> list[EventType]:
        return self._event

    @event.setter
    def event(self, event: list[EventType]) -> None:
        self._event = event

    @property
    def hide(self) -> bool:
        return self._hide

    @hide.setter
    def hide(self, hide: bool) -> None:
        self._hide = hide


class DeveloperSetting:
    # 是否启用debug模式
    _debug: bool = False
    # 是否记录插件运行时间
    _countRuntime: bool = False
    # 运行时间阈值，超过则输出警告
    _runtimeThreshold: float = 0.5

    @property
    def debug(self) -> bool:
        return self._debug

    @debug.setter
    def debug(self, debug: bool) -> None:
        self._debug = debug

    @property
    def countRuntime(self) -> bool:
        return self._countRuntime

    @countRuntime.setter
    def countRuntime(self, countRuntime: bool) -> None:
        self._countRuntime = countRuntime

    @property
    def runtimeThreshold(self) -> float:
        return self._runtimeThreshold

    @runtimeThreshold.setter
    def runtimeThreshold(self, runtimeThreshold: float) -> None:
        self._runtimeThreshold = runtimeThreshold


class Plugin(ABC):
    # 插件作者
    _author: str
    # 插件名称
    _name: str
    # 简易菜单展示名称
    _displayName: str
    # 插件描述
    _description: str
    # 插件版本
    _version: str
    # 插件设置
    _setting: PluginSetting
    # 开发者设置
    _developerSetting: DeveloperSetting

    def __init__(self):

        self._setting: PluginSetting = PluginSetting()

        self._developerSetting: DeveloperSetting = DeveloperSetting()

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, author: str) -> None:
        self._author = author

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def displayName(self) -> str:
        return self._displayName

    @displayName.setter
    def displayName(self, displayName: str) -> None:
        self._displayName = displayName

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        self._description = description

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, version: str) -> None:
        self._version = version

    @property
    def setting(self) -> PluginSetting:
        return self._setting
    
    @setting.setter
    def setting(self, setting: PluginSetting) -> None:
        self._setting = setting

    @property
    def developerSetting(self) -> DeveloperSetting:
        return self._developerSetting
    
    @developerSetting.setter
    def developerSetting(self, developerSetting: DeveloperSetting) -> None:
        self._developerSetting = developerSetting



    @abstractmethod
    def init(self) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def dispose(self) -> None:
        pass
