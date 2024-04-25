class Log:
    """
    简单的日志类
    包含三个方法: infor, warning, error
    """

    @staticmethod
    def info(msg):
        print("信息:", msg)

    @staticmethod
    def warning(msg):
        print("警告:", msg)

    @staticmethod
    def error(msg):
        print("错误:", msg)

    @staticmethod
    def adapter(msg):
        """
        输出收到的上报消息
        """
        print("上报消息:", msg)
