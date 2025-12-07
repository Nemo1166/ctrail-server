#!/bin/bash

# Game Leaderboard Server - 启动脚本 (Linux/macOS)

echo "====================================================="
echo "    Game Leaderboard Server - Starting..."
echo "====================================================="
echo ""

# 检查 uv 是否安装
if ! command -v uv &> /dev/null; then
    echo "错误: uv 未安装" >&2
    echo "请访问 https://github.com/astral-sh/uv 安装 uv" >&2
    exit 1
fi

echo "✓ uv 已安装"

# 检查依赖
echo "检查依赖..."
if [ ! -d ".venv" ]; then
    echo "首次运行，正在安装依赖..."
    uv sync
    if [ $? -ne 0 ]; then
        echo "依赖安装失败" >&2
        exit 1
    fi
fi

echo "✓ 依赖已就绪"
echo ""

# 启动服务器
echo "====================================================="
echo "启动服务器..."
echo "====================================================="
echo ""
echo "服务地址: http://127.0.0.1:8000"
echo "API 文档: http://127.0.0.1:8000/docs"
echo "健康检查: http://127.0.0.1:8000/health"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
