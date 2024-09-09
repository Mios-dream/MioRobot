from Net import Receives
import asyncio
from init_config import Config


async def main():
    # 初始化配置
    config = Config()
    recv = Receives.OneBotReceive(config)
    httpStart = asyncio.create_task(recv.httpStart())
    Start = asyncio.create_task(recv.Start())
    await asyncio.gather(httpStart, Start)


if __name__ == "__main__":
    print("启动机器人")
    asyncio.run(main())
