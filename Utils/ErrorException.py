import sys
import traceback
from typing import Callable


def error_handler(code: Callable):
    """
    错误处理装饰器
    :param code: 被装饰的函数
    :return: 装饰后的函数
    """

    def wrapper(*args, **kwargs):
        try:
            result = code(*args, **kwargs)

            return result
        except Exception as e:

            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb = traceback.extract_tb(exc_traceback)

            # 打印异常的行号和文件名
            print("行号:", tb[-1].lineno)
            print("文件路径:", tb[-1].filename)

            # 打印异常的源代码
            print("错误源码:", traceback.format_exc())

            # 打印异常的特定信息
            print("错误消息:", str(e))

    return wrapper


if __name__ == "__main__":

    @error_handler
    def test(a):
        a = 1 / 0
        print(a)

    test(1)
