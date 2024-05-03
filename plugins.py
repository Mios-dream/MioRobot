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
    }

    def __init__(self, **info):
        # 初始化插件信息
        self.auther = info.get("auther")
        self.name = info.get("name")
        self.version = info.get("version")
        self.description = info.get("description")
        # 设置插件默认信息,很pythonic的字典合并方法
        self.setting = {**self.default_setting, **info.get("setting")}
        # self.setting = info.get("setting")

    def register(self, plugin):
        # 注册插件

        def wrapper(*args, **kwargs):

            result = plugin(*args, **kwargs)

            return result

        return wrapper
