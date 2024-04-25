from Net import Receives
import asyncio

import init_config


async def main():
    config = init_config.Config()
    recv = Receives.OneBotReceive(config)
    await recv.Start()


if __name__ == "__main__":
    print("启动机器人")
    asyncio.run(main())
