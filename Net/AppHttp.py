from fastapi import FastAPI, Request
from Utils.Logs import Log
import json
import psutil
import getpass
import platform
from Core.PluginLoader import PluginLoaderControl
from Core.GroupControl import GroupControl
from Models.Api.BaseApi import RequestApi, ApiAdapter
from typing import cast
from pynvml import (
    nvmlInit,
    nvmlDeviceGetName,
    nvmlDeviceGetHandleByIndex,
    NVMLError,
    nvmlShutdown,
    nvmlDeviceGetMemoryInfo,
    nvmlDeviceGetUtilizationRates,
)


appHttp = FastAPI()


@appHttp.get("/bot_info")
async def botInfo():
    """
    获取bot账号信息
    """
    api = "get_login_info"
    param = {0: 0}
    args = RequestApi(api, param)
    result = await ApiAdapter.sendActionApi(args, 5)
    # 将结果转换为字典类型
    result = cast(dict, result)
    return result["data"]


@appHttp.get("/plugin_error_list")
async def pluginErrorList():
    """
    获取插件报错记录
    """
    return Log.pluginErrorList


@appHttp.get("/group_list")
async def getGroupList():
    """
    获取群列表
    """
    with open("Cache/GroupList.json", "r", encoding="utf-8") as file:
        groupData = json.load(file)
    return groupData


@appHttp.post("/group_list")
async def updateGroupList(request: Request):
    """
    修改群启用状态
    """

    postData = await request.json()
    groupId = postData.get("group_id")
    newStatus = postData.get("is_enable")
    GroupControl.setGroupStatus(groupId, newStatus)
    return {"message": "OK"}


@appHttp.get("/get_cpu_usage")
async def getCpuUsage():
    """
    获取总CPU使用率
    """
    usage = psutil.cpu_percent(interval=1)
    return {"cpu_usage": usage}


@appHttp.get("/get_free_memory")
async def getFreeMemory():
    """
    获取剩余内存（单位：GB）
    """
    virtualMemory = psutil.virtual_memory()
    freeMemory = round(virtualMemory.free / (1024.0**3), 2)
    return {"free_memory_gb": freeMemory}


@appHttp.get("/get_memory_usage")
async def getMemoryUsage():
    """
    获取内存使用率
    """
    virtualMemory = psutil.virtual_memory()
    memoryUsage = round((virtualMemory.used / virtualMemory.total) * 100, 2)
    return {"memory_usage": memoryUsage}


@appHttp.get("/get_system")
async def getSystemInfo():
    """
    获取当前系统硬件信息
    """
    try:
        nvmlInit()
        nvidiaGpuName = nvmlDeviceGetName(nvmlDeviceGetHandleByIndex(0))
    except NVMLError as _:
        nvidiaGpuName = "No NVIDIA GPUs found"
    finally:
        try:
            nvmlShutdown()
        except Exception:
            pass
    username = getpass.getuser()
    u_name = platform.uname()
    processor_name = platform.processor()
    memory = int(round(psutil.virtual_memory().total, 2) / (1024.0**3))
    time = psutil.boot_time()

    o_usage = None
    for disk_partition in psutil.disk_partitions():
        o_usage = psutil.disk_usage(disk_partition.device)

    if o_usage is None:
        o_usage = psutil.disk_usage("/")
    return {
        "username": username,
        "system_name": u_name.system + u_name.version,
        "gpu_name": nvidiaGpuName,
        "system_memory": memory,
        "cpu_model": processor_name,
        "start_time": time,
        "disk": int(o_usage.total / (1024.0**3)),
    }


@appHttp.get("/get_nvidia_gpu_memory_usage")
async def get_nvidia_gpu_memory_usage() -> dict[str, float | int]:
    """
    获取所有NVIDIA GPU的显存使用情况
    """
    try:
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(0)
        memory_info = nvmlDeviceGetMemoryInfo(handle)

        totalMemory = float(memory_info.total)
        usedMemory = float(memory_info.used)
        used_memory_percentage = (
            round((usedMemory / totalMemory) * 100, 2) if totalMemory > 0 else 0
        )
    except NVMLError as _:
        used_memory_percentage = 0
    finally:
        try:
            nvmlShutdown()
        except Exception:
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
        utilization = float(nvmlDeviceGetUtilizationRates(handle).gpu)
    except NVMLError as _:
        utilization = 0
        try:
            nvmlShutdown()
        except Exception:
            pass
    return {"utilization": utilization}


@appHttp.get("/plugin_list")
async def getPluginList():
    """
    插件列表
    """
    return PluginLoaderControl.getPlugins()


@appHttp.post("/plugin_list")
async def updatePluginSetting(request: Request):
    """
    管理插件
    """
    post_data = await request.json()
    pluginName = post_data.get("plugin_name")
    settingData = post_data.get("setting_data")
    PluginLoaderControl.updatePluginSetting(pluginName, settingData)
    return {"message": "OK"}
