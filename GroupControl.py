from Models.Api.RobotInfo import RobotInfo
import websockets
import json
import asyncio


class GroupControl:
    """
    群控制类
    """

    # 群列表,群号为键,群是否开启为值
    group_list = {}
    websoket: websockets.WebSocketClientProtocol = None

    @staticmethod
    def init(websoket: websockets.WebSocketClientProtocol):
        """
        初始化群控制类,即通过接口获取群数据,并更新群列表
        :param websoket: websoket连接
        """
        GroupControl.websoket = websoket

        loop = asyncio.get_event_loop()
        loop.create_task(GroupControl.get_group_data())

    @staticmethod
    async def get_group_data():
        """
        获取群数据
        :return: 群数据
        """
        # 通过接口获取群数据
        row_group_data = await RobotInfo.get_group_list(GroupControl.websoket)
        GroupControl.update_group_data(row_group_data)

    @staticmethod
    def is_enable(group_id: str) -> bool:
        """
        判断群是否启用
        :param group_id: 群号
        :return: 是否启用
        """
        return GroupControl.group_list.get(group_id, False)

    @staticmethod
    def update_group_data(row_group_data: dict):
        """
        更新文件中的群数据
        :param row_group_data: 群数据
        """
        try:
            with open("Cacha/group_list.json", "r+", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = []

        group_data_list = data
        group_list = row_group_data["data"]
        # 默认不启用
        is_enable = False
        # 通过推导式将api格式化获取到的数据
        group_list = [
            {
                "group_id": group["group_id"],
                "group_name": group["group_name"],
                "is_enable": is_enable,
            }
            for group in group_list
        ]

        # 将api获取的数据和文件读取的数据合并，更新群列表中的is_enable字段
        for i in range(len(group_list)):
            for item in group_data_list:
                if group_list[i]["group_id"] == item["group_id"]:

                    GroupControl.group_list[str(group_list[i]["group_id"])] = item[
                        "is_enable"
                    ]

                    group_list[i]["is_enable"] = item["is_enable"]

        # 更新文件中的群数据
        with open("Cacha/group_list.json", "w", encoding="utf-8") as f:
            json.dump(group_list, f, ensure_ascii=False, indent=4)
