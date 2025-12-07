# Game Leaderboard Server - 启动脚本

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "    Game Leaderboard Server - Starting..." -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# 检查 uv 是否安装
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "错误: uv 未安装" -ForegroundColor Red
    Write-Host "请访问 https://github.com/astral-sh/uv 安装 uv" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ uv 已安装" -ForegroundColor Green

# 检查依赖
Write-Host "检查依赖..." -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    Write-Host "首次运行，正在安装依赖..." -ForegroundColor Yellow
    uv sync
    if ($LASTEXITCODE -ne 0) {
        Write-Host "依赖安装失败" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✓ 依赖已就绪" -ForegroundColor Green
Write-Host ""

# 启动服务器
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "启动服务器..." -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "服务地址: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "API 文档: http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host "健康检查: http://127.0.0.1:8000/health" -ForegroundColor Green
Write-Host ""
Write-Host "按 Ctrl+C 停止服务器" -ForegroundColor Yellow
Write-Host ""

uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
