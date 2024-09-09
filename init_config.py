import json


class Config:
    """
    初始化配置信息
    """

    def __init__(self):
        with open("config.json") as json_file:
            json_data = json.load(json_file)

        # self.__dict__ = json_data

        self._set_data(json_data)
        self._set_ManageData(json_data)

    def __str__(self):
        return str(self.__dict__)

    def _set_data(self, json_data):
        # websocket配置信息
        self.Websocket = "{0}/?access_token={1}".format(
            json_data["websocket"], json_data["token"]
        )

    def _set_ManageData(self, json_data):
        # Uvicorn配置信息
        self.UvicornPort = json_data["ManagePort"]
