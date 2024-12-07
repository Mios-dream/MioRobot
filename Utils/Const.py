"""
通过类实现伪常量
使用方法：
import const
const.value = 100
"""


class _const:
    class ConstError(TypeError):
        pass

    def __setattr__(self, key, value):
        if key in self.__dict__:
            data = f"不能重复设置常量 ({key})"
            raise self.ConstError(data)
        self.__dict__[key] = value


import sys

sys.modules[__name__] = _const()
