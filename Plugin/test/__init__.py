from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from plugin_loader import PluginLoaderControl
setting_data = {'priority': 0, 'load': False, 'callback_name': 'test',
    'prevent_other_plugins': False, 'event': ['message'], 'is_hide': True}
auther_data = '三三'
name_data = '简单的消息测试'
display_name_data = '测试'
version_data = '1.0'
description_data = '简单的消息测试'
developer_setting_data = {'count_runtime': False, 'runtime_threshold': 0.5,
    'allow_high_time_cost': False}
plugin = Plugin(auther=auther_data, name=name_data, display_name=
    display_name_data, version=version_data, description=description_data,
    setting=setting_data, developer_setting=developer_setting_data)


@plugin.register
async def test(websocket: object, MessageData: GroupMassageData):
    if MessageData.Message[0] == '测试':
        await MessageApi.sendGroupMessage(websocket, MessageData,
            '当前插件数量{},插件加载耗时{:.4f}秒'.format(PluginLoaderControl.plugin_num,
            PluginLoaderControl.plugin_load_time))
