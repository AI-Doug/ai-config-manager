#!/bin/bash
# 一键安装启动 AI Config Manager

set -e

REPO_URL="https://github.com/AI-Doug/ai-config-manager.git"
INSTALL_DIR="${HOME}/.ai-config-manager"

echo "正在安装 AI Config Manager..."

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
