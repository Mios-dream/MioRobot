from Net import Receives
import asyncio
from init_config import Config


async def main():
    # 初始化配置
    config = Config()
    recv = Receives.OneBotReceive(config)
    await recv.Start()


if __name__ == "__main__":
    print("启动机器人")
    asyncio.run(main())
