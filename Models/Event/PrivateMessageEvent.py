from DataType.PrivateMessageDate import PrivateMessageDate


class PrivateMessageEvent:

    def __init__(self, data: PrivateMessageDate):
        self.QQ = data.get("user_id")
        self.MessageData = data.get("message", None)
        self.Time = data.get("time")
        self.Robot = data.get("self_id")
        self.Sub_Type = data.get("sub_type")
        self.Message_ID = data.get("message_id")
        self.RowMessage = data.get("raw_message")
        self.NickName = data.get("sender").get("nickname")
        self.Message_Type = data.get("message")[0].get("type")

        # 便捷消息读取
        # 群消息,仅包含文字的列表
        self.Message = []

        # 消息图片，仅包含图片的列表
        self.Images = []

        # 对原始格式化消息数据进行解析，传入便捷消息
        if self.MessageData is not None:
            for self.MessageDataCacha in self.MessageData:
                # 文字消息
                if self.MessageDataCacha.get("type", None) == "text":
                    self.Message.append(
                        self.MessageDataCacha.get("data").get("text", None)
                    )
                # 图片消息
                if self.MessageDataCacha.get("type", None) == "image":
                    self.Images.append(
                        self.MessageDataCacha.get("data").get("url", None)
                    )
            # 删除原始格式化消息数据缓存
            del self.MessageDataCacha

        if self.Message is None:
            self.Message.append("")
