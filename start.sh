export LANG=en_US.UTF-8

echo "正在检查环境..."
uv version

if [ $? -eq 0 ]; then
    echo "uv 已经安装"
else
    echo "正在安装 uv"

    # 使用 curl 下载安装脚本并执行
    curl -LsSf https://astral.sh/uv/install.sh | sh

    if [ $? -ne 0 ]; then
        echo "安装失败"
        exit 1
    fi
fi

uv sync
uv run main.py