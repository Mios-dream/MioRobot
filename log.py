import colorama

# 自动重置颜色
colorama.init(autoreset=True)


class Log:
    """
    简单的日志类
    包含三个方法: infor, warning, error
    """

    @staticmethod
    def info(msg) -> None:
        """
        输出普通信息
        """
        print(f"{colorama.Fore.GREEN}\n信息:{msg}")

    @staticmethod
    def warning(msg) -> None:
        """
        输出警告信息
        """
        # print(colorama.Fore.YELLOW + "\n警告:", msg)
        print(f"{colorama.Fore.YELLOW}\n警告:{msg}")

    @staticmethod
    def error(msg) -> None:
        """
        输出错误信息
        """
        # print(colorama.Fore.RED + "\n错误:", msg)
        print(f"{colorama.Fore.RED}\n错误:{msg}")

    @staticmethod
    def adapter(msg) -> None:
        """
        输出收到的上报消息
        """
        print("\n上报消息:", msg)
