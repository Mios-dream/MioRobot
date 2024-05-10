import aiohttp
import asyncio
import ssl
import requests

url = "https://multimedia.nt.qq.com.cn/download?appid=1407&fileid=CgoyODE0NzIxMzAyEhRaNIrt1RG9xuKmue1exIhVF8QWyBiM6AQg_woog9aHg4WAhgNQgL2jAQ&spec=0&rkey=CAISKKSBekjVG1fM0BNdf6VNLhi59kD8MC3BSdV-QdZ3X_O8q4dW-I7HXfM"


# url = "https://gchat.qpic.cn/download?appid=1407&fileid=CgoyODE0NzIxMzAyEhRaNIrt1RG9xuKmue1exIhVF8QWyBiM6AQg_woog9aHg4WAhgNQgL2jAQ&spec=0&rkey=CAISKKSBekjVG1fM0BNdf6VNLhi59kD8MC3BSdV-QdZ3X_O8q4dW-I7HXfM&spec=0"

# async def test():
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url=url, ssl=False) as resp:
#             img_data = await resp.read()
#             # 处理图片数据
#             with open("test.png", "wb") as f:
#                 f.write(img_data)


def test():
    resp = requests.get(url=url, verify=False)
    img_data = resp.content
    # 处理图片数据
    with open("test.png", "wb") as f:
        f.write(img_data)


if __name__ == "__main__":
    test()
    # asyncio.run(test())
