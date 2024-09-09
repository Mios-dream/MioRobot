from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
import re
import requests
import json

setting_data = {
    # 加载优先级,数字越大优先级越高
    "priority": 20,
    # 插件是否可用启用
    "load": True,
    # 插件回调地址
    "callback_name": "fabing",
    # 是否阻止其他插件执行
    "prevent_other_plugins": False,
    "event": ["message"],
}
auther_data = "然飞 ranfey"
name_data = "发病文学"
display_name_data = "发病文学"
version_data = "1.0"
description_data = "发病文学"
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


def remove_exclamation_marks(s):
    # 正则表达式匹配字符串开头和结尾的 '！' 或 '!'
    # 在目标后加！！或!! 触发发病
    pattern = r"^[！!]+|[！!]+$"
    # 替换匹配的部分为空字符串
    result = re.sub(pattern, "", s)
    return result


def fetch_url_content(name):
    base_url = "http://api.krumio.com/faden?name="
    url = base_url + name
    response = requests.get(url)
    if response.status_code == 200:
        try:
            # 将响应文本解析为 JSON
            data = json.loads(response.text)
            # 返回特定的键值
            return data.get("text", '键"text"不存在')
        except json.JSONDecodeError:
            return "JSON解析错误"
    else:
        return "请求失败，状态码：" + str(response.status_code)


@plugin.register
async def fabing(websocket: object, MessageData: GroupMassageData):
    if "!!" in MessageData.Message[0] or "！！" in MessageData.Message[0]:
        name = remove_exclamation_marks(MessageData.Message[0])
        aaa = str(fetch_url_content(name))
        await MessageApi.sendGroupMessage(websocket, MessageData, aaa)
        print(aaa)
