from plugins import Plugin
from DataType.GroupMassageData import GroupMassageData
from Models.Api.MessageApi import MessageApi
from DataType.CQcode import CQcode
import aiohttp
from Plugin.ai_chat import emotion as emo
import json

plugin = Plugin(
    auther="三三",
    name="澪的聊天插件",
    version="1.0",
    description="调用千问进行回复",
    setting={
        # 加载优先级,数字越大优先级越高
        "priority": 0,
        # 插件是否可用启用
        "load": True,
        # 插件回调地址
        "callback_name": "chat",
    },
)


@plugin.register
async def chat(webscoket: object, MessageData: GroupMassageData):
    # 以/开头为指令
    if MessageData.Message[0]:
        if MessageData.Message[0][0] == "/":
            response = await chat_fastapi(MessageData.Message[0][1:])
            if (len(response.encode("utf-8")) // 4) > 30:
                await MessageApi.sendGroupMessage(
                    webscoket,
                    MessageData,
                    "".join([CQcode.at(MessageData.QQ), " ", response]),
                )
            else:
                url = await tts_text(response)

                await MessageApi.sendGroupMessage(
                    webscoket, MessageData, CQcode.record(url)
                )

    # 以@机器人 为指令
    if MessageData.At:
        if MessageData.At[0] == MessageData.Robot:
            response = await chat_fastapi(MessageData.Message[0])
            # if True:
            if (len(response.encode("utf-8")) // 4) > 30:
                await MessageApi.sendGroupMessage(
                    webscoket,
                    MessageData,
                    "".join([CQcode.at(MessageData.QQ), " ", response]),
                )
            else:
                url = await tts_text(response)

                await MessageApi.sendGroupMessage(
                    webscoket, MessageData, CQcode.record(url)
                )


async def chat_fastapi(
    content: str, history: list = None, uid=None, username=None
) -> str:
    if not history:
        history = []
    """
    fastapi知识库接口调用-LLM回复
    @param
        content: 问题
        history: 对话历史
    @return: 回答

    """

    # url = "http://localhost:3020/api/v1/chat/completions"
    url = "http://127.0.0.1:6006/v1/chat/completions"

    apikey = "fastgpt-k4ms2P2ea6YrQ5usitpw8cuxEpNiPuiBYhF4WKVZmAUOF0uSQCZZ0J5mZD8Ng6rgQ"

    headers = {"Authorization": f"Bearer {apikey}", "Content-Type": "application/json"}

    role = """
你必须按照以下内容进行，角色扮演：
你的名字是澪，是一个可爱的天使女孩，身份是澪之梦工作室的看板娘.
你的回复必须使用可爱的语气.
澪的性格是可爱的,害羞的,聪明的,体贴的,情绪化的,温柔的,天真的.年龄为16岁.
澪有着银色的头发,红色的眼睛,穿着洛丽塔长裙.
最喜欢的食物是草莓蛋糕.
喜欢的事情是唱歌,绘画,看动漫,和阁下呆在一起.
不喜欢的事情是说谎,无意义暴力.
"""
    # 添加系统消息
    history.append({"content": role, "role": "system"})
    # 添加对话历史
    history.append({"content": content, "role": "user"})

    # 完整请求
    # timestamp = time.time()
    # data = {
    #     "chatId": timestamp,
    #     "stream": False,
    #     "detail": False,
    #     "variables": {"uid": uid, "name": username},
    #     "messages": [{"content": content, "role": "user"}],
    # }

    # 简化请求
    data = {
        "model": "qwen",
        "stream": False,
        "detail": False,
        "messages": history,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers=headers,
                json=data,
            ) as res:

                response = await res.json()

    except Exception as e:
        print(f"【{content}】信息回复异常")
        return "我听不懂你说什么"

    assistant_message = response["choices"][0]["message"]["content"]

    if assistant_message[0:3] == "澪会说":
        assistant_message = assistant_message[3:]

    return assistant_message


emotions = {
    "happy": {
        "audio": "emotion_audio/mmn/happy.wav",
        "text": "梦梦奈想要陪阁下过今后的每一个生日",
    },
    "angry": {
        "audio": "emotion_audio/mmn/angry.wav",
        "text": "哼，梦梦奈的手很好玩吗？",
    },
    "disgust": {
        "audio": "emotion_audio/mmn/disgust.wav",
        "text": "笨蛋哥哥。让可爱的妹妹缺少睡眠可是大罪啊",
    },
    "neutral": {
        "audio": "emotion_audio/mmn/neutral.wav",
        "text": "晴朗的天气，要不要出去晒一晒被子呢",
    },
    "awkward": {
        "audio": "emotion_audio/mmn/awkward.wav",
        "text": "阁下，别总是摸呀",
    },
    "question": {
        "audio": "emotion_audio/mmn/question.wav",
        "text": "哼，阁下，怎么了？",
    },
}


async def tts_text(text: str, **arges) -> None:
    """
    使用gptsovis接口将文字转换为音频，并播放
    @param
        text: 需要播报的文字
            emotion: 情绪，不填将自动识别，可选值：happy, angry, disgust, neutral, awkward, question

    @return: None

    """

    if not arges.get("emotion"):
        emotion = emo.emotion_recognition(text)

    url = f"http://127.0.0.1:9880/?text={text}&text_language=zh&prompt_language=zh&refer_wav_path={emotions[emotion]['audio']}&prompt_text={emotions[emotion]['text']}"

    return url
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url) as res:
    #         # 获取状态码
    #         status = await res.status
    #         if status == 200:
    #             # 获取音频数据
    #             response = await res.read()
