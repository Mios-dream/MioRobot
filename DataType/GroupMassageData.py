from DataType.MessageData import MessageData


class GroupMassageData(MessageData):
    """
    群消息数据类
    """

    # 事件戳
    Time: str
    # 事件类型
    Post_Type: str
    # 消息类型
    Message_Type: str
    # 消息子类型，为normal
    Sub_Type: str

    # QQ号
    QQ: str
    # 等级
    Level: int
    # 发送者角色
    Role: str
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
    Group_Message_Type: str
    # 消息ID
    Message_ID: str
    # 原始消息，即带CQ码的消息
    RowMessage: str

    # 便捷消息读取
    # 消息图片
    Images: list
    # At对象
    At: list
