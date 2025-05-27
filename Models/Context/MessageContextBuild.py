from functools import singledispatch
from Models.Event.GroupMessageEvent import GroupMessageEvent
from Models.Context.GroupMessageContext import GroupMessageContext


class MessageContextBuild:
    """
    消息上下文构建
    """

    @singledispatch
    @staticmethod
    def build(data) -> None | GroupMessageContext:
        """
        未知消息上下文
        """
        return None

    @build.register
    @staticmethod
    def _(data: GroupMessageEvent) -> GroupMessageContext:
        """
        构建群聊消息上下文
        """
        return GroupMessageContext(data)
