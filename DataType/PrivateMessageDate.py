from DataType.MessageData import MessageData


class PrivateMessageDate(MessageData):
    """
    私聊消息数据类
    """

    Time: int
    QQ: str
    Robot: str
    Post_Type: str
    Message: list
    Message_Type: str
    Sub_Type: str
    Message_Id: int
    RowMessage: str
    Nickname: str
