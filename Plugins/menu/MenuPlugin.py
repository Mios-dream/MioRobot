from Core.Plugin import Plugin
from Plugins.menu.Menu import Menu
import re
from Models.Context.GroupMessageContext import GroupMessageContext
from functools import singledispatchmethod


class MenuPlugin(Plugin):
    def init(self):
        pass

    @singledispatchmethod
    async def run(self, context: GroupMessageContext):

        if context.Event.Message[0] == "菜单":
            menu_data = Menu(display_number=10)
            result = menu_data.show_menu()
            if result:
                await context.Command.Reply(result)

            else:
                await context.Command.Reply(" 菜单为空")

            if menu_data.page_number > 1:
                await context.Command.Reply(
                    ' 这是第1页菜单,总共{}页,发送"第2页"可以查看其他菜单哦'.format(
                        menu_data.page_number
                    ),
                )

        elif num := re.match(r"第(\d+)页", context.Event.Message[0]):
            menu_data = Menu(display_number=10)
            data = menu_data.show_menu(page_num=int(num.group(1)))
            await context.Command.Reply(
                data if data else "没有更多了",
            )

    def dispose(self) -> None:
        pass
