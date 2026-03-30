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

# 创建虚拟环境
if [ ! -f ".venv/bin/activate" ]; then
    echo "创建 Python 虚拟环境..."

    # 方案1: 优先使用 python3 -m venv
    if python3 -m venv .venv 2>/dev/null; then
        echo "虚拟环境创建成功（使用 python3 -m venv）"
    # 方案2: 如果 venv 失败，尝试 virtualenv
    elif command -v virtualenv >/dev/null 2>&1; then
        echo "尝试使用 virtualenv..."
        virtualenv .venv
    # 方案3: 使用 --without-pip 创建最小环境，然后手动安装 pip
    else
        echo "尝试创建最小化虚拟环境..."
        if python3 -m venv --without-pip .venv 2>/dev/null; then
            echo "安装 pip..."
            # 下载并安装 pip
            if command -v curl >/dev/null 2>&1; then
                curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
            elif command -v wget >/dev/null 2>&1; then
                wget -q https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py
            else
                echo "错误: 需要 curl 或 wget 来下载 pip"
                exit 1
            fi
            .venv/bin/python3 /tmp/get-pip.py
            rm -f /tmp/get-pip.py
        else
            echo ""
            echo "错误: 无法创建 Python 虚拟环境"
            echo ""
            echo "尝试的解决方案："
            echo ""
            echo "1. 安装 python3-venv 包（需要 sudo）:"
            if command -v apt-get >/dev/null 2>&1; then
                echo "   sudo apt-get install python3-venv"
                echo "   # 或对于 Ubuntu/Debian 系统:"
                echo "   sudo apt-get install python3.12-venv"
            elif command -v dnf >/dev/null 2>&1; then
                echo "   sudo dnf install python3-venv"
            elif command -v yum >/dev/null 2>&1; then
                echo "   sudo yum install python3-venv"
            elif command -v pacman >/dev/null 2>&1; then
                echo "   sudo pacman -S python-venv"
            fi
            echo ""
            echo "2. 安装 virtualenv（可能需要 pip）:"
            echo "   pip install --user virtualenv"
            echo ""
            echo "3. 使用 pipx（推荐，无需配置）:"
            echo "   pipx install ai-config-manager"
            echo ""
            echo "4. 如果有 conda/mamba:"
            echo "   conda create -n ai-config-manager python=3.12"
            echo "   conda activate ai-config-manager"
            echo "   pip install ai-config-manager"
            echo ""
            echo "安装完成后重新运行此脚本"
            exit 1
        fi
    fi
fi

source .venv/bin/activate

# 安装包（处理 PEP 668 externally-managed-environment）
echo "安装依赖..."
if ! pip install -q . 2>&1; then
    # 如果是 PEP 668 错误，尝试添加 --break-system-packages
    if pip install --break-system-packages -q . 2>/dev/null; then
        echo "依赖安装成功（使用 --break-system-packages）"
    else
        echo ""
        echo "错误: 无法安装依赖"
        echo ""
        echo "尝试手动安装："
        echo "  source .venv/bin/activate"
        echo "  pip install ."
        echo ""
        echo "或使用 pipx 安装："
        echo "  pipx install ai-config-manager"
        exit 1
    fi
fi

echo ""
echo "安装完成！运行 'ai-config' 启动"
ai-config
