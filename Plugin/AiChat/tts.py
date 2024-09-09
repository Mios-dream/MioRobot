from Plugin.AiChat.emotion import emotion_recognition

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
        emotion = emotion_recognition(text)

    url = f"http://127.0.0.1:9880/?text={text}&text_language=zh&prompt_language=zh&refer_wav_path={emotions[emotion]['audio']}&prompt_text={emotions[emotion]['text']}"

    return url
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url) as res:
    #         # 获取状态码
    #         status = await res.status
    #         if status == 200:
    #             # 获取音频数据
    #             response = await res.read()
