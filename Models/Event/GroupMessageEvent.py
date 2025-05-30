from Models.Event.BaseEvent import BaseEvent
from Models.Event.EventType import EventType


class GroupMessageEvent(BaseEvent):
    """
    群消息事件
    """

    # 事件戳
    Time: int
    # 事件类型
    Post_Type: EventType
    # 消息类型
    Message_Type: str
    # 消息子类型，为normal
    Sub_Type: str
    # QQ号
    QQ: int
    # 等级
    Level: int
    # 发送者角色
    Role: int
    # 发送者头衔
    Title: str
    # robot的QQ号
    Robot: int
    # 昵称
    Nickname: str
    # 群号
    Group: int
    # 群昵称Card
    GroupNickname: str
    # 群消息
    Message: list
    # 群消息类型
    Group_Message_Type: str  # type: ignore
    # 消息ID
    Message_ID: int
    # 原始消息，即带CQ码的消息
    RowMessage: str
    # 便捷消息读取
    # 消息图片
    Images: list[str]
    # At对象
    At: list[int]

    def __init__(self, data: dict):
        sender = data.get("sender", {})
        # 初始化基础属性
        self.Post_Type = EventType.GroupMessage
        self.Message_Type = data.get("message_type", "")
        self.Time = data.get("time", "")
        self.Sub_Type = data.get("sub_type", "")
        self.QQ = data.get("user_id", 0)
        self.Level = sender.get("level")
        self.Title = sender.get("title")
        self.Role = sender.get("role")
        self.Robot = data.get("self_id", 0)
        self.Nickname = sender.get("nickname")
        self.Group = data.get("group_id", 0)
        self.GroupNickname = sender.get("card")
        self.RowMessage = data.get("raw_message", "")
        self.Message_ID = data.get("message_id", 0)

        # 初始化便捷消息读取列表
        self.Message = []
        self.Images = []
        self.At = []

        # 解析原始消息数据
        self.MessageData = data.get("message", [])
        self.__parse_message_data()

    def __parse_message_data(self):
        """解析消息数据"""
        for item in self.MessageData:
            msg_type = item.get("type")
            msg_data = item.get("data", {})

            if msg_type == "text":
                self.Message.append(msg_data.get("text", ""))
            elif msg_type == "image":
                url = msg_data.get("url", "").replace(
                    "https://multimedia.nt.qq.com.cn/", "https://gchat.qpic.cn/"
                )
                self.Images.append(url)
            elif msg_type == "at":
                self.At.append(msg_data.get("qq", 0))

        # 如果没有文字消息，添加空字符串占位
        if not self.Message:
            self.Message.append("")

    @property
    def Group_Message_Type(self) -> str:
        """获取群消息类型"""
        return self.MessageData[0].get("type", "") if self.MessageData else ""

    def __str__(self):
        return (
            f"QQ: {self.QQ}, Nickname: {self.Nickname}, Group: {self.Group}, "
            f"GroupNickname: {self.GroupNickname}, Message: {self.Message}, "
            f"MessageType: {self.Message_Type}, Images: {self.Images}, "
            f"MessageID: {self.Message_ID}, Time: {self.Time}"
        )
