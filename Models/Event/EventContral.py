from Models.Event.GroupMessageEvent import GroupMessageEvent
from Models.Event.PrivateMessageEvent import PrivateMessageEvent
from Models.Event.NoticeEvent import NoticeEvent
from Models.Event.RequestEvent import RequestEvent
from Models.Event.MetaEvent import MetaEvent
from DataType.MessageData import MessageData
from DataType.GroupMassageData import GroupMassageData
from DataType.PrivateMessageData import PrivateMessageData
from typing import Union


def EventContral(data: MessageData) -> Union[GroupMassageData, PrivateMessageData]:

    try:
        Post_Type = data.get("post_type", None)
        if Post_Type == "message":
            # 消息类型,private或group
            Message_Type = data.get("message_type", None)
            if Message_Type == "group":
                data = GroupMessageEvent(data)
                return data
            elif Message_Type == "private":
                data = PrivateMessageEvent(data)
                return data
        elif Post_Type == "notice":
            # 通知类型,包括群成员增加,减少,禁言等
            Notice_Type = data.get("notice_type", None)
            data = NoticeEvent(data)
            return data
        elif Post_Type == "request":
            # 请求类型,包括加群请求,加好友请求等
            Request_Type = data.get("request_type", None)
            data = RequestEvent(data)
            return data
        elif Post_Type == "meta_event":
            # 元事件类型,包括群成员减少,群成员增加,群禁言,群解除禁言等
            Meta_Event_Type = data.get("meta_event_type", None)
            data = MetaEvent(data)
            return data
        else:
            print("无法解析的消息:", data)

    except Exception as e:
        print("无法解析的消息:", e)
