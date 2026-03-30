#!/bin/bash
# 一键安装启动 AI Config Manager

set -e

REPO_URL="https://github.com/AI-Doug/ai-config-manager.git"
INSTALL_DIR="${HOME}/.ai-config-manager"

echo "正在安装 AI Config Manager..."

if [ -d "$INSTALL_DIR" ]; then
    if [ -d "$INSTALL_DIR/.git" ]; then
        echo "已安装，正在更新..."
        cd "$INSTALL_DIR"
        git pull
    else
        echo "检测到已安装但不是 git 仓库，重新安装..."
        rm -rf "$INSTALL_DIR"
        git clone "$REPO_URL" "$INSTALL_DIR"
        cd "$INSTALL_DIR"
    fi
else
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# 创建虚拟环境（捕获错误以便给出清晰提示）
create_venv() {
    python3 -m venv .venv 2>&1
}

if [ ! -f ".venv/bin/activate" ]; then
    echo "创建 Python 虚拟环境..."
    if ! create_venv; then
        echo ""
        echo "错误: 无法创建 Python 虚拟环境"
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
fi

source .venv/bin/activate

# 安装包（捕获错误）
echo "安装依赖..."
if ! pip install -q . 2>&1; then
    echo ""
    echo "错误: 无法安装依赖"
    echo ""
    echo "可能是系统 Python 环境问题，尝试："
    echo "  1. 确保已安装 python3-venv 并创建了虚拟环境"
    echo "  2. 或者手动安装：source .venv/bin/activate && pip install ."
    exit 1
fi

echo ""
echo "安装完成！运行 'ai-config' 启动"
ai-config
