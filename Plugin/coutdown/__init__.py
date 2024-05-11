from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from datetime import datetime
import random


plugin = Plugin(
    auther="三三",
    name="高考倒计时",
    version="1.0",
    display_name="高考倒计时",
    description="高考倒计时插件",
    setting={
        # 加载优先级,数字越大优先级越高
        "priority": 0,
        # 插件是否可用启用
        "load": True,
        # 插件回调地址
        "callback_name": "countdown",
        # 是否阻止后续插件执行
        "prevent_other_plugins": False,
        "event": ["message"],
    },
)


@plugin.register
async def countdown(websocket: object, MessageData: GroupMassageData):
    # 开发者命令
    if MessageData.Message[0] == "高考倒计时":
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
