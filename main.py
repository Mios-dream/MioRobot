from Net.Receives import recv
import asyncio


async def main():
    # 初始化配置
    httpStart = asyncio.create_task(recv.httpStart())
    Start = asyncio.create_task(recv.Start())
    await asyncio.gather(httpStart, Start)


if __name__ == "__main__":
    print("启动机器人")
    asyncio.run(main())
