from Net import Receives
from log import Log
import asyncio
from init_config import Config


async def main():
    # 初始化配置
    config = Config()
    recv = Receives.OneBotReceive(config)
    await recv.Start()


if __name__ == "__main__":
    Log.info("正在启动澪...")
    asyncio.run(main())
