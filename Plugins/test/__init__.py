from Plugin import Plugin


class TestPlugin(Plugin):

    def init(self) -> bool:
        if super().init():
            return True
        return False

    async def run(self) -> bool:
        chi=self.configData["chi"]
         if chi in MessageData.Message[0]:
            return True
        return False

    async def dispose(self) -> bool:
        print("TestPlugin is being disposed")
        return True
