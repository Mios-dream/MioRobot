from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
from Plugin.weather.weather import Weather
import base64
import re


plugin = Plugin(
    auther="三三",
    name="天气查询",
    version="1.0",
    display_name="天气查询",
    description="天气查询",
    setting={
        # 加载优先级,数字越大优先级越高
        "priority": 0,
        # 插件是否可用启用
        "load": True,
        # 插件回调地址
        "callback_name": "weather_forcast",
        # 是否阻止后续插件执行
        "prevent_other_plugins": False,
        "event": ["message"],
    },
)


@plugin.register
async def weather_forcast(websocket: object, MessageData: GroupMassageData):

    if MessageData.Message[0] == "天气查询":
        await MessageApi.sendGroupMessage(
            websocket,
            MessageData,
            "只要发送\n天气 <城市名>\n即可查询阁下城市的天气啦！",
        )

    data = re.search(r"^天气 (.*)", MessageData.Message[0])
    if data:
        img_data = Weather(data.group(1))
        if img_data.is_true_city:
            img_data = base64.b64encode(img_data.image()).decode()

            await MessageApi.sendGroupMessage(
                websocket, MessageData, CQcode.img(f"base64://{img_data}")
            )
        else:
            await MessageApi.sendGroupMessage(
                websocket,
                MessageData,
                "阁下输入的城市不存在，请换一个城市再试试！",
            )
