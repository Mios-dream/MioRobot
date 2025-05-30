@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo 正在检查环境...
uv version

if not %errorlevel% neq 0 (
    echo uv已经安装,正在启动...
) else (
    echo 正在安装uv

    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

    if %errorlevel% neq 0 (
        echo 安装失败
        pause
        exit /b 1
    )

    uv sync
)

if not exist .venv (
    echo 创建虚拟环境
    uv sync
)


call .venv\Scripts\activate.bat

echo 正在检查环境更新... 

uv pip install -r pyproject.toml

uv run main.py

pause