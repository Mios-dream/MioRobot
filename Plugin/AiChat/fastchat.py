import aiohttp


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

    # 发送请求
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers=headers,
                json=data,
            ) as res:

                response = await res.json()

    except Exception as e:
        return "澪不知道该如何回答...."

    assistant_message = response["choices"][0]["message"]["content"]
    # 去除多余信息
    if assistant_message[0:3] == "澪会说":
        assistant_message = assistant_message[3:]

    return assistant_message
