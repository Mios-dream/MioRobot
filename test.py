import asyncio
from Plugins.test import TestPlugin


if __name__ == "__main__":
    plugin = TestPlugin()

    plugin.init()
    asyncio.run(plugin.run())
