from Models.Event.GroupMessageEvent import GroupMessageEvent
from Models.Event.PrivateMessageEvent import PrivateMessageEvent
from Models.Event.NoticeEvent import NoticeEvent
from Models.Event.RequestEvent import RequestEvent
from Models.Event.MetaEvent import MetaEvent
from typing import Union
import json
from Utils.Logs import Log
from Utils.Task import Task


class EventAdapter:
    # 事件控制
    OnNext: list[Task] = []

    @staticmethod
    def EventControl(
        rawData: str,
    ) -> Union[
        None,
        GroupMessageEvent,
        PrivateMessageEvent,
        NoticeEvent,
        RequestEvent,
        MetaEvent,
    ]:
        """
        事件控制
        用于将消息解析为对应的事件对象
        """

        try:
            # 用于处理api返回的json数据
            data = json.loads(rawData)
            if "echo" in data:
                # 将api返回的消息打印到控制台
                Log.apiResponse(data)
                for item in EventAdapter.OnNext:
                    if item.echo == data["echo"]:
                        item.setResult(data)
            else:
                # 输出收到的消息到控制台
                Log.adapter(data)
                # 用于处理上报信息
                postType = data.get("post_type", None)
                if postType == "message":
                    # 消息类型,private或group
                    Message_Type = data.get("message_type", None)
                    if Message_Type == "group":

                        data = GroupMessageEvent(data)  # type: ignore

                        return data
                    elif Message_Type == "private":
                        data = PrivateMessageEvent(data)
                        return data
                elif postType == "notice":
                    # 通知类型,包括群成员增加,减少,禁言等
                    __Notice_Type = data.get("notice_type", None)
                    data = NoticeEvent(data)
                    return data
                elif postType == "request":
                    # 请求类型,包括加群请求,加好友请求等
                    __Request_Type = data.get("request_type", None)
                    data = RequestEvent(data)
                    return data
                elif postType == "meta_event":
                    # 元事件类型,包括群成员减少,群成员增加,群禁言,群解除禁言等
                    __Meta_Event_Type = data.get("meta_event_type", None)
                    data = MetaEvent(data)
                    return data
                else:
                    Log.warning(f"无法解析的消息:{data}")

        except Exception as e:
            Log.warning(f"无法解析的消息:{e}")
