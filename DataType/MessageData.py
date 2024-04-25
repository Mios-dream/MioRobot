from pydantic import BaseModel


class MessageData(BaseModel):
    """
    消息数据基类
    """

    # 机器人QQ号
    Robot: int
    # 事件类型
    Post_Type: str
    # 消息事件戳
    Time: int
