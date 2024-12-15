import random


class Tip:
    """
    随机一言
    """

    @staticmethod
    def text() -> str:
        """
        随机一言
        """
        with open("Plugin\menu\yiyan.txt", "r", encoding="UTF-8") as f:
            data = random.choice(f.readlines())
        return data
