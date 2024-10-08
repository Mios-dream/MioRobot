from typing import Callable


class Plugin:
    """
    插件基类
    """

    # 作者
    author = None
    # 插件名称
    name = None
    # 插件展示名称，用于简易菜单展示
    display_name = None
    # 插件版本
    version = None
    # 插件描述
    description = None
    # 插件设置
    default_setting = {
        # 加载优先级
        "priority": 0,
        # 插件是否可用启用
        "load": False,
        # 插件回调地址
        "callback_name": "",
        # 是否阻止其他后续插件执行
        "prevent_other_plugins": False,
        # 需要监听的事件
        "event": [],
        # 是否在菜单隐藏,为True时将不会在简易菜单中显示
        "is_hide": False,
    }
    # 开发者设置
    developer_setting = {
        # 是否记录运行时间
        "count_runtime": False,
        # 运行时间阈值，超过则输出警告
        "runtime_threshold": 0.5,
        # 是否允许高时间消耗，如果为否，则会在运行时间过长时输出警告，警告时间默认为0.5秒
        "allow_high_time_cost": False,
    }

    def __init__(self, **info):
        # 初始化插件信息
        self.author = info.get("author")
        self.name = info.get("name")
        self.version = info.get("version")
        self.description = info.get("description")
        self.display_name = info.get("display_name")
        # 设置插件默认信息,安全的字典合并方法
        self.setting = {**self.default_setting, **info.get("setting", {})}
        self.developer_setting = {
            **self.developer_setting,
            **info.get("developer_setting", {}),
        }

    def register(self, plugin: Callable) -> Callable:
        # 注册插件

        def wrapper(*args, **kwargs):

            result = plugin(*args, **kwargs)

            return result

        return wrapper
