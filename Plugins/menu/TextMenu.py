from Plugin.menu.Tip import Tip


class TextMenu:
    """
    生成文字菜单
    """

    # 菜单每页显示数量
    display_number = 10
    # 菜单页数
    page_number = 0
    # 菜单显示的文字列表
    menu_list = []
    # 是否显示一言
    add_yiyan = True
    # 标题
    title = ""

    def __init__(
        self,
        menu_list: list[str],
        title: str = "",
        display_number: int = 10,
        add_yiyan: bool = True,
    ):
        self.add_yiyan = add_yiyan
        self.display_number = display_number

        # 清空菜单列表
        self.menu_list.clear()

        # 添加菜单标题
        self.title = title

        self.menu_list = [
            menu_list[i : i + self.display_number]
            for i in range(0, len(menu_list), self.display_number)
        ]
        # 计算页数
        self.page_number = len(self.menu_list)

    def __custom_length(self, s: str) -> int:
        """
        计算字符串长度，其中汉字长度计为4，其余长度计为1。

        参数:
        s (str): 输入的字符串

        返回:
        int: 根据定制规则计算的字符串长度
        """
        count = 0
        for char in s:
            # 判断是否为汉字，这里简单地通过Unicode范围来判断
            if "\u4e00" <= char <= "\u9fff":
                count += 4
            else:
                count += 1
        return count

    def show_menu(self, page_num: int = 1) -> str:
        """
        显示菜单
        """
        display_list = []
        blank = " " * max((14 - len(self.title)), 2)
        title = (
            f"┍{' ' * (self.__custom_length(self.menu_list[page_num - 1][-1])+6)}┐\n"
            if not self.title
            else f"┍{blank}{self.title}{blank}┐\n"
        )

        end = "".join(["└", " " * (self.__custom_length(title) - 2), "┘"])
        # 添加菜单文字
        display_list.append(title)

        if page_num > len(self.menu_list):
            return None
        # 添加菜单内容
        for text in self.menu_list[page_num - 1]:
            # 计算空格
            blank = " " * max(12 - len(text), 2)
            display_list.append(f"{blank}🌸{text}🌸\n")
        # 添加尾部
        display_list.append(end)
        # 显示一言
        if self.add_yiyan:
            display_list.append("\n============\n")
            display_list.append(Tip.text())

        return "".join(display_list)
