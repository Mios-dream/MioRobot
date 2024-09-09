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
from pynvml import *


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


@appHttp.get("/group_list")
async def get_features():
    with open("Cacha\group_list.json", "r", encoding="utf-8") as file:
        group_data = json.load(file)
    return group_data


@appHttp.post("/group_list")
async def post_features(request: Request):
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
    return {"message": "OK"}


def run_api():
    from Models.Api.modelModApi import openapi_qwen2

    uvicorn.run(
        "Models.Api.modelModApi.openapi_qwen2:app", host="0.0.0.0", port=6006, workers=1
    )


@appHttp.get("/modelModApi")
async def modelModApi():
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


import importlib.util
import json


def load_modify_save(module_path, new_settings):
    # 动态加载模块
    spec = importlib.util.spec_from_file_location("module.name", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 获取原有设置
    original_settings = module.plugin.setting

    # 更新设置
    original_settings.update(new_settings)

    # 将更新后的设置写回文件（需要处理文件写入逻辑）
    with open(module_path, "r") as file:
        lines = file.readlines()

    with open(module_path, "w") as file:
        inside_setting = False
        for line in lines:
            if "setting={" in line:
                inside_setting = True
                file.write("    setting={\n")
                for key, value in original_settings.items():
                    file.write(f"        '{key}': {json.dumps(value)},\n")
                continue
            if inside_setting:
                if "}," in line:
                    file.write("    },\n")
                    inside_setting = False
                continue
            file.write(line)


# 调用函数
load_modify_save("path/to/plugin/__init__.py", {"load": False})
