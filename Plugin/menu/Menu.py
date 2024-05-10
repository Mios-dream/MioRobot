from plugin_loader import PluginLoaderControl


class Menu:
    def __init__(self):
        pass

    def show_menu(self):
        plugin_data = PluginLoaderControl.plugin_list.keys()
        plugin_list = []
        for plugin in plugin_data:
            plugin_list.append(plugin.plugin.name)
        result = ",".join(plugin_list)
        return result
