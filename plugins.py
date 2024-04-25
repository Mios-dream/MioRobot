class Plugin:
    """
    插件基类
    """

    # 作者
    auther = None
    # 插件名称
    name = None
    # 插件版本
    version = None
    # 插件描述
    description = None

    setting = {
        # 加载优先级
        "priority": 0,
        # 插件是否可用启用
        "load": False,
        # 插件回调地址
        "callback_name": "",
    }

    def __init__(self, **info):
        # 初始化插件信息
        self.auther = info.get("auther")
        self.name = info.get("name")
        self.version = info.get("version")
        self.description = info.get("description")
        self.setting = info.get("setting")

    def register(self, plugin):
        # 注册插件

        def wrapper(*args, **kwargs):

            result = plugin(*args, **kwargs)

            return result

        return wrapper
