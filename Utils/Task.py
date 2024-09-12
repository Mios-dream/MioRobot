import asyncio


class Task:
    """
    用于异步任务处理
    """

    def __init__(self, guid) -> None:
        # 为任务设置唯一标识符
        self.echo = guid
        # 获取当前事件循环
        loop = asyncio.get_running_loop()
        # 创建一个Future对象
        self.fut = loop.create_future()

    def set_result(self, JObject):
        try:
            # 设置Future对象的值，标志任务完成
            self.fut.set_result(JObject)
        except Exception:
            pass
