from plugin_loader import PluginLoaderControl
import random


class Menu:
    display_number = 5
    plugin_list = []
    add_yiyan = True

    def __init__(self):
        # 清空插件列表
        self.plugin_list.clear()
        plugin_data = PluginLoaderControl.plugin_list.keys()
        # 添加插件
        for plugin in plugin_data:
            if not plugin.plugin.setting["is_hide"]:
                self.plugin_list.append(plugin.plugin.display_name)
        self.plugin_list = sorted(self.plugin_list, key=len)

    def yiyan(self):
        """
        随机一言
        """
        with open("Plugin\menu\yiyan.txt", "r", encoding="UTF-8") as f:
            data = random.choice(f.readlines())
        return data

    def show_menu(self):
        """
        显示菜单
        """
        display_list = []
        title = "┍          菜单        ┐\n"
        end = "└                         ┘"
        # 添加菜单文字
        display_list.append(title)
        # 添加插件
        for plugin in self.plugin_list:
            # 计算空格
            back = " " * max(9 - len(plugin), 1)
            display_list.append(f"{back}🌸{plugin}🌸\n")
        # 添加尾部
        display_list.append(end)
        # 显示一言
        if self.add_yiyan:
            display_list.append("\n============\n")
            display_list.append(self.yiyan())
            return "".join(display_list)
