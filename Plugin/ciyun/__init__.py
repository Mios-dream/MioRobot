from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
import requests
import jieba
from wordcloud import WordCloud
import json
import os
import base64
from io import BytesIO

setdata = {
    # 加载优先级,数字越大优先级越高
    "priority": 100,
    # 插件是否可用启用
    "load": False,
    # 插件回调地址
    "callback_name": "ciyun",
    # 是否阻止其他插件执行
    "prevent_other_plugins": False,
    "event": ["message"],
}

plugin = Plugin(
    auther="然飞 ranfey",
    name="生成词云",
    display_name="生成词云",
    version="1.0",
    description="生成词云",
    setting=setdata,
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

    filename = "Plugin\\ciyun\\date\\" + MessageData.Group + ".json"
    mode = "r+" if os.path.exists(filename) and os.path.getsize(filename) > 0 else "w"

    try:
        with open(filename, mode, encoding="utf-8") as file:
            if mode == "w":  # 如果是写入模式，意味着文件之前不存在或为空
                json.dump([data], file, ensure_ascii=False, indent=4)
            else:  # 文件已存在且非空，需要添加到现有数据
                file.seek(0, os.SEEK_END)  # 移动到文件末尾
                file.seek(
                    file.tell() - 1, os.SEEK_SET
                )  # 后退一位，覆盖最后的关闭方括号
                file.write(",")  # 添加一个逗号
                json.dump(data, file, ensure_ascii=False, indent=4)
                file.write("]")  # 重新关闭数组
    except Exception as e:
        print(f"An error occurred: {e}")


@plugin.register
async def ciyun(websocket: object, MessageData: GroupMassageData):
    newText(MessageData)
    if "今日词云" in MessageData.Message[0]:
        with open(
            "Plugin\\ciyun\\date\\" + MessageData.Group + ".json", "r", encoding="utf-8"
        ) as file:
            data = json.load(file)
        texts = [item["message"] for item in data]
        txt = " ".join(texts)
        # 使用 jieba 进行精确分词
        words = jieba.lcut(txt)
        # 使用空格拼接分词结果
        newtxt = " ".join(words)
        wordcloud = WordCloud(font_path="C:\\Windows\\Fonts\\msyh.ttf").generate(newtxt)
        img_data = base64.b64encode(wordcloud.to_image()).decode()
        await MessageApi.sendGroupMessage(
            websocket, MessageData, CQcode.img(f"base64://{img_data}")
        )
