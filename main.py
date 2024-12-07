from Net.Receives import recv
from Utils.Logs import Log
import asyncio


async def main():
    # 初始化配置
    httpStart = asyncio.create_task(recv.httpStart())
    Start = asyncio.create_task(recv.start())
    await asyncio.gather(httpStart, Start)


if __name__ == "__main__":
    Log.info("正在启动澪...")
    asyncio.run(main())
