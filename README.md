# Game Leaderboard Server

基于 FastAPI 的游戏排行榜服务，使用 SQLite 数据库存储，uv 管理依赖。

## 功能特性

- ✅ 提交玩家分数
- ✅ 获取排行榜列表（支持分页）
- ✅ 查询玩家排名
- ✅ RESTful API 设计
- ✅ 自动生成 API 文档
- ✅ 类型安全（Pydantic）
- ✅ 数据库 ORM（SQLAlchemy）

## 技术栈

- **FastAPI**: 现代高性能 Web 框架
- **SQLite**: 轻量级关系型数据库
- **SQLAlchemy**: Python SQL 工具和 ORM
- **Pydantic**: 数据验证和设置管理
- **Uvicorn**: ASGI 服务器
- **uv**: 快速的 Python 包管理器

## 快速开始

### 环境要求

- Python >= 3.11
- uv 包管理器

### 安装

1. 克隆仓库
```bash
git clone <repository-url>
cd ctrail-server
```

2. 安装依赖
```bash
uv sync
```

### 运行

#### 开发模式

```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 生产模式

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 访问

- **API 服务**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## API 接口

### 1. 提交分数

**POST** `/api/leaderboard/submit`

请求示例：
```json
{
  "player_id": "player_12345",
  "score": 9800,
  "timestamp": 1701936000
}
```

响应示例：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "rank": 15,
    "best_score": 9800
  }
}
```

### 2. 获取排行榜

**GET** `/api/leaderboard?limit=10&offset=0&time_range=all`

参数：
- `limit`: 返回记录数（默认 50，最大 100）
- `offset`: 偏移量（默认 0）
- `time_range`: 时间范围（daily/weekly/monthly/all，默认 all）

响应示例：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 150,
    "entries": [
      {
        "rank": 1,
        "player_id": "player_99999",
        "score": 15800,
        "timestamp": 1701936000
      }
    ]
  }
}
```

### 3. 获取玩家排名

**GET** `/api/leaderboard/player/{player_id}?time_range=all`

响应示例：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "player_id": "player_12345",
    "rank": 15,
    "score": 9800,
    "timestamp": 1701936000,
    "total_players": 150
  }
}
```

## 项目结构

```
ctrail-server/
├── main.py                 # 应用入口
├── pyproject.toml          # 项目配置
├── README.md
├── design/                 # 设计文档
│   ├── api.md             # API 设计
│   └── arch.md            # 架构设计
├── app/
│   ├── __init__.py
│   ├── config.py          # 配置管理
│   ├── database.py        # 数据库配置
│   ├── api/               # API 路由
│   │   └── leaderboard.py
│   ├── models/            # 数据模型
│   │   └── leaderboard.py
│   ├── schemas/           # Pydantic 模式
│   │   └── leaderboard.py
│   └── services/          # 业务逻辑
│       └── leaderboard.py
└── tests/                 # 测试文件
    └── test_leaderboard.py
```

## 测试

运行测试：
```bash
uv run pytest tests/ -v
```

## 配置

可以通过环境变量或 `.env` 文件配置：

```env
# 应用配置
APP_NAME="Game Leaderboard Server"
API_PREFIX="/api"

# 数据库
DATABASE_URL="sqlite:///./leaderboard.db"

# CORS
CORS_ORIGINS=["*"]

# 排行榜
MAX_LEADERBOARD_SIZE=1000
DEFAULT_PAGE_LIMIT=50
MAX_PAGE_LIMIT=100

# 日志
LOG_LEVEL="INFO"
```

## 开发

### 安装开发依赖

```bash
uv sync --all-extras
```

### 代码格式化

```bash
uv run black .
```

### 代码检查

```bash
uv run ruff check .
```

## 许可

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
