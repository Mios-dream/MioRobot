import os
import importlib.util
import sys

def load_packages_from_directory(directory:str):
    """
    动态加载指定目录下的所有包
    :param directory: 包所在的目录路径
    """
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isdir(full_path) and os.path.isfile(os.path.join(full_path, '__init__.py')):
            package_name = entry
            module_name = f"{os.path.basename(directory)}.{package_name}"
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(full_path, '__init__.py'))
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            print(f"Loaded package: {module_name}")

# 使用示例
directory_path = 'd:\\yutuber_ai\\robot\\qq\\plugins'  # 替换为你的目录路径
load_packages_from_directory(directory_path)