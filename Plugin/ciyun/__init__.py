from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
import requests
import jieba
from wordcloud import WordCloud


plugin = Plugin(
    auther="然飞 ranfey",
    name="生成词云",
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

GroupClass = {}


def copyGroup(MessageData: str):
    GroupClass.setdefault(MessageData, newText(MessageData))


def newText(MessageData: str):
    with open(MessageData + ".txt", "a") as file:
        file.write("What I want to add on goes here")


@plugin.register
async def fudu(websocket: object, MessageData: GroupMassageData):
    GroupTT = str(MessageData.Group)
    copyGroup(GroupTT)
