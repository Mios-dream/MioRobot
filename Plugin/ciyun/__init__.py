from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
import requests
import jieba
from wordcloud import WordCloud
import json
import os

plugin = Plugin(
    auther="然飞 ranfey",
    name="生成词云",
    display_name="生成词云",
    version="1.0",
    description="生成词云",
    setting={
        # 加载优先级,数字越大优先级越高
        "priority": 100,
        # 插件是否可用启用
        "load": False,
        # 插件回调地址
        "callback_name": "ciyun",
        # 是否阻止其他插件执行
        "prevent_other_plugins": False,
        "event": ["message"],
    },
)


# txt = '弱小的人,才习惯,嘲讽和否定，而内心,强大的人,从不吝啬赞美和鼓励！我们就是后浪，奔涌吧！后浪，奔涌吧！'
# words = jieba.lcut(txt)     #精确分词
# newtxt = ''.join(words)    #空格拼接
# wordcloud = WordCloud(font_path =  "msyh.ttf").generate(newtxt)wordcloud.to_file('中文词云图.jpg')


data = {
    "QQid": "2219349024",
    "message": "消息",
}


def newText(MessageData: GroupMassageData):
    data["message"] = str(MessageData.Message[0])
    data["QQid"] = MessageData.QQ

    file = open(
        "Plugin\\ciyun\\date\\" + MessageData.Group + ".json", "a+", encoding="utf-8"
    )
    if (
        os.path.getsize("Plugin\\ciyun\\date\\" + MessageData.Group + ".json") == 0
    ):  # 文件为空，写入数组
        file.write(json.dumps([data], ensure_ascii=False, indent=4))
    else:
        file.close()
        with open(
            "Plugin\\ciyun\\date\\" + MessageData.Group + ".json",
            "r+",
            encoding="utf-8",
        ) as file:
            file.seek(-3, os.SEEK_END)
            file.write(",\n" + json.dumps(data, ensure_ascii=False, indent=4) + "\n]")


@plugin.register
async def ciyun(websocket: object, MessageData: GroupMassageData):
    newText(MessageData)
    print(MessageData.Group)
