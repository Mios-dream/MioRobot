from Models.MessageChain.Message import Message


class MessageChain:
    """
    消息链
    """

    messages: list[Message]

    def __init__(self) -> None:
        self.messages = []

    def add(self, message: Message):
        """
        添加消息
        Parameters:
            message(Message): 要添加的消息
        """
        if not isinstance(message, Message):
            raise TypeError("message must be a Message")
        self.messages.append(message)
        return self

    def to_dict(self) -> list[dict]:
        return [message.to_dict() for message in self.messages]
