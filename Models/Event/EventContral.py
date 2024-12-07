from Models.Event.GroupMessageEvent import GroupMessageEvent
from Models.Event.PrivateMessageEvent import PrivateMessageEvent
from Models.Event.NoticeEvent import NoticeEvent
from Models.Event.RequestEvent import RequestEvent
from Models.Event.MetaEvent import MetaEvent
from DataType.GroupMassageData import GroupMassageData
from DataType.PrivateMessageData import PrivateMessageData


from typing import Union
import json
from Utils.Logs import Log


class EventAdapter:
    # 事件控制
    OnNext = []

    @staticmethod
    def EventContral(
        data: str,
    ) -> Union[None, GroupMassageData, PrivateMessageData]:

        try:
            # 用于处理api返回的json数据
            data = json.loads(data)
            if "echo" in data:
                # 将api返回的消息打印到控制台
                Log.api_response(data)
                for item in EventAdapter.OnNext:
                    if item.echo == data["echo"]:
                        item.set_result(data)
            else:
                # 输出收到的消息到控制台
                Log.adapter(data)
                # 用于处理上报信息
                Post_Type = data.get("post_type", None)
                if Post_Type == "message":
                    # 消息类型,private或group
                    Message_Type = data.get("message_type", None)
                    if Message_Type == "group":
                        from GroupControl import GroupControl

                        data = GroupMessageEvent(data)
                        # 检查是否开启对应群的消息接收
                        if not GroupControl.is_enable(data.Group):
                            # Log.warning("当前群未开启")
                            return None
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
                    Log.warning(f"无法解析的消息:{data}")

        except Exception as e:
            Log.warning(f"无法解析的消息:{e}")
