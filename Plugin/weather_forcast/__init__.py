from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
from Plugin.weather_forcast.weather import Weather
import base64
import re

setting_data = {
    # 加载优先级,数字越大优先级越高
    "priority": 0,
    # 插件是否可用启用
    "load": True,
    # 插件回调地址
    "callback_name": "weather_forcast",
    # 是否阻止后续插件执行
    "prevent_other_plugins": False,
    "event": ["message"],
}
auther_data = "三三"
name_data = "天气查询"
display_name_data = "天气查询"
version_data = "1.0"
description_data = "天气查询"
developer_setting_data = {
    # 是否记录运行时间
    "count_runtime": False,
    # 运行时间阈值，超过则输出警告
    "runtime_threshold": 0.5,
    # 是否允许高时间消耗，如果为否，则会在运行时间过长时输出警告，警告时间默认为0.5秒
    "allow_high_time_cost": False,
}

plugin = Plugin(
    auther=auther_data,
    name=name_data,
    display_name=display_name_data,
    version=version_data,
    description=description_data,
    setting=setting_data,
    developer_setting=developer_setting_data,
)


@plugin.register
async def weather_forcast(websocket: object, MessageData: GroupMassageData, Trigger):
    data = re.search(r"^天气 (.*)", MessageData.Message[0])
    if data:
        img_data = Weather(data.group(1))
        if img_data.is_true_city:
            img_data = base64.b64encode(img_data.image()).decode()
            Trigger.run()

            await MessageApi.sendGroupMessage(
                websocket, MessageData, CQcode.img(f"base64://{img_data}")
            )
        else:
            Trigger.run()
            await MessageApi.sendGroupMessage(
                websocket,
                MessageData,
                "阁下输入的城市不存在，请换一个城市再试试！",
            )
