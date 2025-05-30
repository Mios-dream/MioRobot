"""
插件依赖自动安装脚本
自动扫描插件目录并使用uv安装依赖
"""

import subprocess
import threading
import random
import time
from pathlib import Path
import colorama
from Utils.Logs import Log


class SpinnerAnimation:
    """转圈动画类"""

    def __init__(self, message="更新中"):
        self.message = message
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        # 随机颜色
        self.colors = [
            colorama.Fore.RED,
            colorama.Fore.GREEN,
            colorama.Fore.YELLOW,
            colorama.Fore.BLUE,
            colorama.Fore.MAGENTA,
            colorama.Fore.CYAN,
            colorama.Fore.WHITE,
        ]
        self.running = False
        self.thread = None

    def _animate(self):
        i = 0
        while self.running:
            print(
                f"\r{random.choice(self.colors)} {self.spinner_chars[i % len(self.spinner_chars)]} {self.message}",
                end="",
                flush=True,
            )
            time.sleep(0.1)
            i += 1

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        print("\r", end="", flush=True)  # 清除当前行


def check_uv():
    """检查uv是否可用"""
    spinner = SpinnerAnimation("检查核心中的uv版本")
    spinner.start()

    try:
        result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )
        spinner.stop()

        if result.returncode == 0:
            Log.info(f"✓ 找到uv: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    except Exception as e:
        spinner.stop()
        Log.error(f"⚠️ 检查uv时出现问题: {e}")

    spinner.stop()
    Log.error("❌ 未找到uv，请先安装uv")
    Log.error(
        '安装方法:powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"'
    )
    return False


def find_requirements_file(plugin_path):
    """在插件目录中查找requirements文件"""
    possible_paths = [
        plugin_path / "requirements.txt",
        plugin_path / "requirements" / "requirements.txt",
    ]

    # 检查标准位置
    for req_path in possible_paths:
        if req_path.exists():
            return req_path

    # 查找requirements目录下的所有txt文件
    req_dir = plugin_path / "requirements"
    if req_dir.exists():
        for txt_file in req_dir.glob("*.txt"):
            return txt_file

    return None


def parse_requirements(req_file):
    """解析requirements文件，返回包列表"""
    packages = []
    try:
        with open(req_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释
                if line and not line.startswith("#"):
                    packages.append(line)
    except Exception as e:
        Log.error(f"⚠️ 无法读取requirements文件: {e}")
    return packages


def install_single_package(package_name, use_no_build_isolation=False):
    """安装单个包"""
    isolation_text = " (使用 --no-build-isolation)" if use_no_build_isolation else ""
    Log.info(f"📦 正在安装: {package_name}{isolation_text}")

    try:
        cmd = ["uv", "pip", "install", package_name]
        if use_no_build_isolation:
            cmd.append("--no-build-isolation")

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            universal_newlines=True,
        )

        # 实时显示输出
        while True:
            if process.stdout is not None:
                output = process.stdout.readline()
            else:
                output = None

            if output == "" and process.poll() is not None:
                break
            if output:
                line = output.strip()
                if line:
                    print(f"   {line}")

        return_code = process.poll()

        if return_code == 0:
            Log.info(f"✓ {package_name} 安装成功{isolation_text}")
            return True
        else:
            Log.error(
                f"❌ {package_name} 安装失败 (返回码: {return_code}){isolation_text}"
            )
            return False

    except Exception as e:
        Log.error(f"❌ 安装 {package_name} 时出错: {e}")
        return False


def install_requirements(req_file):
    """使用uv安装requirements文件中的依赖，失败时逐个安装"""
    Log.info(f"📦 正在安装: {req_file}")

    # 解析requirements文件
    packages = parse_requirements(req_file)

    if not packages:
        Log.error("❌ requirements文件为空或无效")
        return False

    # 显示要安装的包列表
    print("💼 依赖列表:")
    for package in packages:
        print(f"   - {package}")

    # 方法1：尝试直接安装整个requirements文件
    Log.info("🔄 尝试批量安装...")

    try:
        process = subprocess.Popen(
            ["uv", "pip", "install", "-r", str(req_file)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            universal_newlines=True,
        )

        # 实时显示输出
        output_lines = []
        while True:
            if process.stdout is not None:
                output = process.stdout.readline()
            else:
                output = None

            if output == "" and process.poll() is not None:
                break
            if output:
                line = output.strip()
                if line:
                    print(f"   {line}")
                    output_lines.append(line)

        return_code = process.poll()

        if return_code == 0:
            Log.info("✓ 批量安装成功")
            return True
        else:
            Log.error(f"❌ 批量安装失败 (返回码: {return_code})")

    except Exception as e:
        Log.error(f"❌ 批量安装出错: {e}")

    # 方法2：批量安装失败，尝试逐个安装
    Log.info("🔄 批量安装失败，开始逐个安装...")

    success_count = 0
    failed_packages = []

    for i, package in enumerate(packages, 1):
        Log.info(f"📦 [{i}/{len(packages)}] 正在安装: {package}")

        # 尝试正常安装
        if install_single_package(package):
            success_count += 1
        else:
            # 正常安装失败，尝试使用 --no-build-isolation 参数
            Log.info(
                f"🔄 正常安装失败，尝试使用 --no-build-isolation 参数安装 {package}"
            )

            if install_single_package(package, use_no_build_isolation=True):
                success_count += 1
                Log.info(f"✓ {package} 使用 --no-build-isolation 参数安装成功")
            else:
                failed_packages.append(package)
                Log.error(f"❌ {package} 所有安装方式都失败")

        # 在包之间添加短暂延迟，避免并发问题
        if i < len(packages):
            time.sleep(0.5)

    if failed_packages:
        return False
    else:
        Log.info("✓ 所有依赖安装成功")
        return True


def updataPluginsDependencies():
    """
    自动安装插件依赖
    """

    Log.info("🚀 开始插件依赖自动安装...")

    # 配置 - 自动检测插件目录名
    possible_dirs = ["plugins", "Plugins", "plugin", "Plugin"]
    plugin_dir = None

    for dir_name in possible_dirs:
        if Path(dir_name).exists():
            plugin_dir = Path(dir_name)
            break

    if plugin_dir is None:
        plugin_dir = Path("plugins")  # 默认值

    # 检查插件目录是否存在
    if not plugin_dir.exists():
        Log.error(f"❌ 插件目录 '{plugin_dir}' 不存在")
        return

    # 检查uv是否可用
    if not check_uv():
        return

    Log.info(f"📁 扫描插件目录: {plugin_dir}")

    # 统计变量
    total_plugins = 0
    success_count = 0
    failed_plugins = []

    spinner = SpinnerAnimation("正在检查包中的依赖文件...")

    # 扫描所有插件目录
    for plugin_path in plugin_dir.iterdir():
        spinner.start()
        if not plugin_path.is_dir():
            spinner.stop()
            continue

        plugin_name = plugin_path.name

        # 查找requirements文件
        req_file = find_requirements_file(plugin_path)

        if req_file:
            spinner.stop()
            Log.info(f"🔍 检查插件: {plugin_name}")
            total_plugins += 1
            try:
                rel_path = req_file.relative_to(Path.cwd())
                Log.info(f"📋 找到requirements文件: {rel_path}")
            except ValueError:
                Log.info(f"📋 找到requirements文件: {req_file}")

            if install_requirements(req_file):
                success_count += 1
            else:
                failed_plugins.append(plugin_name)
        else:
            spinner.stop()

    print("=" * 40)
    print("自检结果:")
    print("=" * 40)
    print(f"发现插件数量: {total_plugins}")
    print(f"成功安装: {success_count}")
    print(f"安装失败: {len(failed_plugins)}")

    if failed_plugins:
        print("❌ 安装失败的插件:")
        for plugin in failed_plugins:
            print(f"  - {plugin}")
        print("建议检查:")
        print("  - requirements文件格式是否正确")
        print("  - 网络连接是否正常")
        print("  - uv配置是否正确")
        exit(1)
    elif success_count > 0:
        print("所有插件依赖安装成功！")
    else:
        print("没有找到需要安装的插件依赖")

    Log.info("✅ 系统更新完成！")

    time.sleep(2)


def removeUnusedDependencies():
    """
    移除未使用的依赖
    """

    print("🚀 开始移除未使用的依赖...")
    if not check_uv():  # 检查uv是否可用
        return False

    process = subprocess.Popen(
        ["uv", "sync"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        universal_newlines=True,
    )
    # 实时显示输出
    output_lines = []
    while True:
        if process.stdout is not None:
            output = process.stdout.readline()
        else:
            output = None

        if output == "" and process.poll() is not None:
            break
        if output:
            line = output.strip()
            if line:
                print(f"   {line}")
                output_lines.append(line)

    return_code = process.poll()

    if return_code == 0:
        Log.info("✓ 安装成功")
        return True
    else:
        Log.error(f"❌ 清理依赖失败 (返回码: {return_code})")
        return False
