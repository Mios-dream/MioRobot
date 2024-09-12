class GroupMessageEvent:

    def __init__(self, data: dict):
        # 事件类型，为message
        self.Post_Type = data.get("post_type", None)

        # 消息类型,private或group
        self.Message_Type = data.get("message_type", None)

        # 事件戳
        self.Time = data.get("time", None)

        # 消息子类型，为normal
        self.Sub_Type = data.get("sub_type", None)

        # QQ号
        self.QQ = str(data.get("user_id", None))
        # 等级
        self.Level = data.get("sender").get("level", None)
        # 发送者头衔
        self.Title = data.get("sender", None).get("title", None)
        # 发送者角色  member,owner,admin
        self.Role = data.get("sender").get("role", None)
        # robot的QQ号
        self.Robot = str(data.get("self_id", None))

        # 昵称
        self.Nickname = data.get("sender").get("nickname", None)
        # 群号
        self.Group = str(data.get("group_id", None))
        # 群昵称
        self.GroupNickname = data.get("sender").get("card", None)

        # 原始格式化消息数据
        self.MessageData = data.get("message", None)

        # 便捷消息读取
        # 群消息,仅包含文字的列表
        self.Message = []

        # 消息图片，仅包含图片的列表
        self.Images = []
        # At对象，仅包含At对象的列表
        self.At = []

        # 对原始格式化消息数据进行解析，传入便捷消息
        if self.MessageData is not None:
            for MessageDataCacha in self.MessageData:
                # 文字消息
                if MessageDataCacha.get("type", None) == "text":
                    self.Message.append(MessageDataCacha.get("data").get("text", None))
                    continue
                # 图片消息
                # 原始图片
                # if self.MessageDataCacha.get("type", None) == "image":
                #     self.Images.append(
                #         self.MessageDataCacha.get("data").get("url", None)
                #     )

                # 替换图床链接后的图片，这只是一个临时方案
                if MessageDataCacha.get("type", None) == "image":
                    self.Images.append(
                        MessageDataCacha.get("data")
                        .get("url", None)
                        .replace(
                            "https://multimedia.nt.qq.com.cn/", "https://gchat.qpic.cn/"
                        )
                    )
                    continue

                # At消息
                if MessageDataCacha.get("type", None) == "at":
                    self.At.append(str(MessageDataCacha.get("data").get("qq", None)))
                    continue

        if not self.Message:
            self.Message.append("")

        # 原始消息，即带CQ码的消息
        self.RowMessage = data.get("raw_message", None)
        # 群消息类型
        self.Group_Message_Type = self.MessageData[0].get("type", None)
        # 消息ID
        self.Message_ID = data.get("message_id", None)

    def __str__(self):
        return f"{self.QQ} {self.Nickname} {self.Group} {self.GroupNickname} {self.Message} {self.Message_Type} {self.Images} {self.Message_ID} {self.Time}"
