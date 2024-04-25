import re


class CQcode:
    @staticmethod
    def img(url):
        """
        url: 图片链接,base64,本地图片地址
        """
        return f"[CQ:image,file={url}]"
        # if re.match("^http", url):
        #     # 链接，http或者https
        #     return f"[CQ:image,file={url}]"
        # elif re.match("^base64", url):
        #     # base64图片
        #     return f"[CQ:image,base64={url}]"
        # else:
        #     # 本地图片
        #     return "[CQ:image,file=file://" + url + "]"

    @staticmethod
    def at(qq):
        """
        qq: qq号
        """
        return f"[CQ:at,qq={qq}]"

    @staticmethod
    def face(id):
        """
        id: 表情id
        """
        return f"[CQ:face,id={id}]"

    @staticmethod
    def reply(message_id):
        """
        message_id: 回复的消息id
        """
        return f"[CQ:reply,id={message_id}]"

    @staticmethod
    def record(file):
        """
        file: 音频文件地址
        """
        return f"[CQ:record,file={file}]"

    @staticmethod
    def vidoe(file):
        """
        file: 视频文件地址
        """
        return f"[CQ:video,file={file}]"

    @staticmethod
    def weather(city):
        """
        city: 城市名
        """
        return f"[CQ:weather,city={city}]"

    @staticmethod
    def music(type, id):
        """
        type: 163 网易云音乐 qq QQ音乐
        id: 歌曲id
        """
        return f"[CQ:music,type={type},id={id}]"
