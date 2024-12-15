from PluginLoader import PluginLoaderControl
from Plugin.menu.TextMenu import TextMenu


class Menu(TextMenu):
    """
    总菜单
    """

    # 菜单每页显示数量
    display_number = 10
    # 菜单页数
    page_number = 0
    # 菜单显示的文字列表
    menu_list = []
    # 是否显示一言
    add_yiyan = True
    # 标题
    title = "菜单"

    def __init__(self, display_number: int = 5, add_yiyan: bool = True):
        menu_list = []
        self.add_yiyan = add_yiyan
        self.display_number = display_number
        # 清空插件列表
        self.menu_list.clear()
        plugin_data = PluginLoaderControl.plugin_list.keys()
        # 添加插件
        for plugin in plugin_data:
            if not plugin.plugin.setting["is_hide"]:
                menu_list.append(plugin.plugin.display_name)
        menu_list = sorted(menu_list, key=len)

        self.menu_list = [
            menu_list[i : i + self.display_number]
            for i in range(0, len(menu_list), self.display_number)
        ]
        # 计算页数
        self.page_number = len(self.menu_list)


if __name__ == "__main__":
    menu = Menu()
    print(menu.show_menu(1))
