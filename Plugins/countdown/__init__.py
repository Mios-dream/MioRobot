from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from datetime import datetime
import random

setting_data = {
    # 加载优先级,数字越大优先级越高
    "priority": 0,
    # 插件是否可用启用
    "load": True,
    # 插件回调地址
    "callback_name": "countdown",
    # 是否阻止后续插件执行
    "prevent_other_plugins": False,
    "event": ["message"],
}
author_data = "三三"
name_data = "高考倒计时"
display_name_data = "高考倒计时"
version_data = "1.0"
description_data = "高考倒计时插件"
developer_setting_data = {
    # 是否记录运行时间
    "count_runtime": False,
    # 运行时间阈值，超过则输出警告
    "runtime_threshold": 0.5,
    # 是否允许高时间消耗，如果为否，则会在运行时间过长时输出警告，警告时间默认为0.5秒
    "allow_high_time_cost": False,
}

plugin = Plugin(
    author=author_data,
    name=name_data,
    display_name=display_name_data,
    version=version_data,
    description=description_data,
    setting=setting_data,
    developer_setting=developer_setting_data,
)


@plugin.register
async def countdown(websocket: object, MessageData: GroupMassageData, Trigger):
    # 开发者命令
    if MessageData.Message[0] == "高考倒计时":
        Trigger.run()
        # 获取当前日期
        Today = datetime.now()
        year = Today.year
        # 高考开始日期
        GaokaoStartDate = datetime(year, 6, 7)

        # 计算剩余天数，注意需要将datetime对象转换为date对象进行计算
        RemainingDays = (GaokaoStartDate.date() - Today.date()).days

        if RemainingDays > 0:
            reply = [
                f"距离高考还有{RemainingDays}天！",
                [f"距离高考还有{RemainingDays}天！", "“为世上所以美好而战”", "加油!"],
            ]
            await MessageApi.sendGroupMessage(
                websocket, MessageData, random.choice(reply)
            )
        elif RemainingDays > -3:

            await MessageApi.sendGroupMessage(websocket, MessageData, "阁下，高考加油!")
        else:
            year = Today.year + 1
            GaokaoStartDate = datetime(year, 6, 7)

            RemainingDays = (GaokaoStartDate.date() - Today.date()).days
            reply = [
                f"距离高考还有{RemainingDays}天！",
                [f"距离高考还有{RemainingDays}天！", "“为世上所以美好而战”", "加油!"],
            ]
            await MessageApi.sendGroupMessage(
                websocket, MessageData, random.choice(reply)
            )

        return 0
