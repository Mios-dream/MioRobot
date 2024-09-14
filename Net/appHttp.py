from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
from log import Log
import json
import threading
from init_config import Config
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import psutil
import importlib.util
import getpass
import platform
import ast
import astor
from plugin_loader import PluginLoaderControl
from group_control import GroupControl
from Models.Api.BaseApi import RequestApi, ApiAdapter
from pynvml import *
from Net.Receives import recv
import os


# AES加密类
class AESCipher:
    def __init__(self, key):
        self.key = key

    # 填充数据，使其长度为16的倍数
    def _pad(self, text):
        # AES的块大小是16字节
        block_size = AES.block_size
        padding_length = block_size - len(text) % block_size
        # 使用PKCS7填充
        padding = chr(padding_length) * padding_length
        return text + padding

    # 去除填充
    def _unpad(self, text):
        padding_length = ord(text[-1])
        return text[:-padding_length]

    # 加密函数
    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = get_random_bytes(AES.block_size)  # 生成初始化向量
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(raw.encode("utf-8"))
        # 返回加密后的内容（初始化向量 + 加密数据），并进行Base64编码
        return base64.b64encode(iv + encrypted).decode("utf-8")

    # 解密函数
    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[: AES.block_size]  # 提取初始化向量
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(enc[AES.block_size :]).decode("utf-8")
        return self._unpad(decrypted)


appHttp = FastAPI()


@appHttp.get("/bot_info")
async def bot_info():
    """
    获取bot账号信息
    """
    api = "get_login_info"
    param = {0: 0}
    args = RequestApi(api, param)
    iii = await ApiAdapter.sendActionApi(recv.Websocket, args, 5)
    return iii["data"]


@appHttp.get("/plugin_error_list")
async def plugin_error_list():
    """
    获取插件报错记录
    """
    return Log.plugin_error_list


@appHttp.post("/plugin_trigger_list")
async def plugin_trigger_list(request: Request):
    """
    获取插件触发记录（时间戳）
    """
    post_data = await request.json()
    callback_name = post_data.get("callback_name")
    return {callback_name: PluginLoaderControl.trigger_list[callback_name].runtime}


@appHttp.get("/group_list")
async def get_features():
    """
    获取群列表
    """
    with open("Cacha\group_list.json", "r", encoding="utf-8") as file:
        group_data = json.load(file)
    return group_data


@appHttp.post("/group_list")
async def post_features(request: Request):
    """
    修改群启用
    """
    with open("Cacha\group_list.json", "r", encoding="utf-8") as file:
        group_data = json.load(file)
    post_data = await request.json()
    group_id = post_data.get("group_id")
    NEW_is_enable = post_data.get("is_enable")
    for group in group_data:
        if group["group_id"] == group_id:
            group["is_enable"] = NEW_is_enable

    with open("Cacha/group_list.json", "w", encoding="utf-8") as file:
        json.dump(group_data, file, ensure_ascii=False, indent=4)

    await GroupControl.get_group_data()
    return {"message": "OK"}


def run_api():
    from Models.Api.modelModApi import openapi_qwen2

    uvicorn.run(
        "Models.Api.modelModApi.openapi_qwen2:app", host="0.0.0.0", port=6006, workers=1
    )


@appHttp.get("/modelModApi")
async def modelModApi():
    """
    运行模型
    """
    thread = threading.Thread(target=run_api)
    thread.start()
    return {"message": "OK"}


@appHttp.get("/get_cpu_usage")
async def get_cpu_usage():
    """
    获取总CPU使用率
    """
    usage = psutil.cpu_percent(interval=1)
    return {"cpu_usage": usage}


@appHttp.get("/get_free_memory")
async def get_free_memory():
    """
    获取剩余内存（单位：GB）
    """
    virtual_memory = psutil.virtual_memory()
    free_memory_gb = round(virtual_memory.free / (1024.0**3), 2)
    return {"free_memory_gb": free_memory_gb}


@appHttp.get("/get_memory_usage")
async def get_memory_usage():
    """
    获取内存使用率
    """
    virtual_memory = psutil.virtual_memory()
    memory_usage = round((virtual_memory.used / virtual_memory.total) * 100, 2)
    return {"memory_usage": memory_usage}


@appHttp.get("/get_system")
async def get_username():
    """
    获取当前系统硬件信息
    """
    try:
        nvmlInit()
        nvidia_countt = nvmlDeviceGetName(nvmlDeviceGetHandleByIndex(0))
    except NVMLError as _:
        nvidia_countt = "No NVIDIA GPUs found"
    finally:
        try:
            nvmlShutdown()
        except:
            pass
    username = getpass.getuser()
    u_name = platform.uname()
    processor_name = platform.processor()
    memory = int(round(psutil.virtual_memory().total, 2) / (1024.0**3))
    time = psutil.boot_time()
    for disk_partition in psutil.disk_partitions():
        o_usage = psutil.disk_usage(disk_partition.device)
    return {
        "username": username,
        "system_name": u_name.system + u_name.version,
        "gpu_name": nvidia_countt,
        "system_memory": memory,
        "cpu_model": processor_name,
        "start_time": time,
        "eisk": int(o_usage.total / (1024.0**3)),
    }


@appHttp.get("/get_nvidia_gpu_memory_usage")
async def get_nvidia_gpu_memory_usage():
    """
    获取所有NVIDIA GPU的显存使用情况
    """
    try:
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(0)
        memory_info = nvmlDeviceGetMemoryInfo(handle)
        used_memory_percentage = (
            round((memory_info.used / memory_info.total) * 100, 2)
            if memory_info.total > 0
            else 0
        )
    except NVMLError as _:
        used_memory_percentage = "No NVIDIA GPUs found"
    finally:
        try:
            nvmlShutdown()
        except:
            pass
    return {"memory_usage": used_memory_percentage}


@appHttp.get("/get_nvidia_gpu_utilization")
async def get_nvidia_gpu_utilization():
    """
    获取所有NVIDIA GPU的利用率
    """
    try:
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(0)
        utilization = nvmlDeviceGetUtilizationRates(handle).gpu
    except NVMLError as _:
        utilization = "No NVIDIA GPUs found"
        try:
            nvmlShutdown()
        except:
            pass
    return {"utilization": utilization}


def load_Plugin(module_path):
    try:
        # 检查文件是否存在
        if not os.path.exists(module_path):
            raise FileNotFoundError(f"模块文件未找到: {module_path}")

        # 动态加载模块
        spec = importlib.util.spec_from_file_location("module.name", module_path)
        if spec is None:
            raise ImportError(f"无法创建模块spec: {module_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # 获取模块中的数据属性
        auther = getattr(module, "auther_data", "未提供作者信息")
        name = getattr(module, "name_data", "未提供名称")
        display_name = getattr(module, "display_name_data", "未提供显示名称")
        version = getattr(module, "version_data", "未提供版本号")
        description = getattr(module, "description_data", "未提供描述")
        setting = getattr(module, "setting_data", "未提供设置信息")
        developer_setting = getattr(
            module, "developer_setting_data", "未提供开发者设置信息"
        )

        return {
            "setting": setting,
            "author": auther,
            "name": name,
            "display_name": display_name,
            "version": version,
            "description": description,
            "developer_setting": developer_setting,
        }

    except FileNotFoundError as fnf_error:
        print(f"文件错误: {fnf_error}")
    except ImportError as import_error:
        print(f"导入错误: {import_error}")
    except AttributeError as attr_error:
        print(f"属性错误: {attr_error}")
    except Exception as e:
        print(f"发生未知错误: {e}")
    return None  # 如果出错返回None或其他合适的值


@appHttp.get("/Plugin_list")
async def get_Plugin_list():
    """
    插件列表
    """
    plugin_list = os.listdir("Plugin")
    plugin_list_r = {}
    for plugin_name in plugin_list:
        module_path = f"Plugin/{plugin_name}/__init__.py"
        plugin_list_r[plugin_name] = load_Plugin(module_path)

    return plugin_list_r


class UpdateLoadValue(ast.NodeTransformer):
    def __init__(self, new_load_value):
        self.new_load_value = new_load_value
        # 继承方法，实例化时载入参数

    def visit_Assign(self, node):
        # 确定正在访问的是 setting_data 变量
        if (
            isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == "setting_data"
        ):
            # 确定值是字典类型
            if isinstance(node.value, ast.Dict):
                for index, key in enumerate(node.value.keys):
                    # 定位到 'load' 键
                    if isinstance(key, ast.Str) and key.s == "load":
                        # 更新 'load' 键的值
                        node.value.values[index] = ast.NameConstant(
                            value=self.new_load_value
                        )
        return node


def update_setting_data(file_path, new_load_value):
    with open(file_path, "r", encoding="utf-8") as file:
        source = file.read()

    tree = ast.parse(source)

    # 使用自定义的 AST Transformer
    transformer = UpdateLoadValue(new_load_value)
    transformer.visit(tree)

    # 将修改后的 AST 转换回源代码
    updated_source = astor.to_source(tree)

    # 将更新后的代码写回文件
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(updated_source)


@appHttp.post("/Plugin_list")
async def post_Plugin_list(request: Request):
    """
    管理插件
    """
    post_data = await request.json()
    callback_name_path = post_data.get("callback_name")
    load_path = post_data.get("load")

    module_path = f"Plugin/{callback_name_path}/__init__.py"
    update_setting_data(module_path, load_path)
    PluginLoaderControl.reload()
    return {"message": "OK"}
