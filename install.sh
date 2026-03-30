#!/bin/bash
# 一键安装启动 AI Config Manager

set -e

REPO_URL="https://github.com/AI-Doug/ai-config-manager.git"
INSTALL_DIR="${HOME}/.ai-config-manager"

echo "正在安装 AI Config Manager..."

# 检查 python3-venv 是否可用
check_venv() {
    python3 -m venv --help >/dev/null 2>&1
}

if ! check_venv; then
    echo "错误: python3-venv 不可用"
    echo ""
    echo "请先安装 python3-venv 包："
    if command -v apt-get >/dev/null 2>&1; then
        echo "  sudo apt-get install python3-venv"
        echo ""
        echo "或者如果是 Ubuntu/Debian 系统，使用对应版本："
        echo "  sudo apt-get install python3.12-venv"
    elif command -v dnf >/dev/null 2>&1; then
        echo "  sudo dnf install python3-venv"
    elif command -v yum >/dev/null 2>&1; then
        echo "  sudo yum install python3-venv"
    elif command -v pacman >/dev/null 2>&1; then
        echo "  sudo pacman -S python-venv"
    fi
    echo ""
    echo "安装完成后重新运行此脚本"
    exit 1
fi

if [ -d "$INSTALL_DIR" ]; then
    echo "已安装，正在更新..."
    cd "$INSTALL_DIR"
    git pull
else
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install -q .

echo ""
echo "安装完成！运行 'ai-config' 启动"
ai-config
