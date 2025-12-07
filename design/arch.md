# 游戏排行榜服务架构设计

## 1. 技术栈

### 后端框架
- **FastAPI**: 现代、高性能的 Python Web 框架
  - 自动生成 OpenAPI 文档
  - 类型检查和数据验证
  - 异步支持
  - 高性能

### 数据库
- **SQLite**: 轻量级关系型数据库
  - 无需独立服务器进程
  - 适合中小型应用
  - 支持事务
  - 易于部署

### 依赖管理
- **uv**: 快速的 Python 包管理器
  - 极速的依赖解析和安装
  - 兼容 pip 和 pyproject.toml
  - 虚拟环境管理

---

## 2. 项目结构

```
ctrail-server/
├── main.py                 # 应用入口
├── pyproject.toml          # 项目配置和依赖
├── uv.lock                 # 依赖锁文件
├── README.md
├── design/                 # 设计文档
│   ├── api.md
│   └── arch.md
├── app/
│   ├── __init__.py
│   ├── api/                # API 路由
│   │   ├── __init__.py
│   │   └── leaderboard.py  # 排行榜接口
│   ├── models/             # 数据模型
│   │   ├── __init__.py
│   │   └── leaderboard.py  # 排行榜数据模型
│   ├── schemas/            # Pydantic 模式
│   │   ├── __init__.py
│   │   └── leaderboard.py  # 请求/响应模式
│   ├── services/           # 业务逻辑
│   │   ├── __init__.py
│   │   └── leaderboard.py  # 排行榜服务
│   ├── database.py         # 数据库连接和配置
│   └── config.py           # 应用配置
└── tests/                  # 测试文件
    ├── __init__.py
    └── test_leaderboard.py
```

---

## 3. 系统架构

### 3.1 分层架构

```
┌─────────────────────────────────────────┐
│          Client (Godot Game)            │
└──────────────────┬──────────────────────┘
                   │ HTTP/JSON
┌──────────────────▼──────────────────────┐
│         API Layer (FastAPI)             │
│  - 路由处理                              │
│  - 请求验证                              │
│  - 响应序列化                            │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│       Service Layer (业务逻辑)          │
│  - 排行榜逻辑                            │
│  - 分数计算                              │
│  - 排名更新                              │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│       Model Layer (数据访问)            │
│  - ORM 操作                              │
│  - 数据持久化                            │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│         Database (SQLite)               │
│  - leaderboard 表                        │
│  - 索引和约束                            │
└─────────────────────────────────────────┘
```

### 3.2 核心组件

#### API Layer (app/api/)
- 接收 HTTP 请求
- 参数验证和类型检查
- 调用 Service Layer
- 返回标准化响应

#### Service Layer (app/services/)
- 实现业务逻辑
- 处理排行榜计算
- 协调数据访问
- 处理事务

#### Model Layer (app/models/)
- 定义数据库表结构
- ORM 映射
- 数据库操作

#### Schema Layer (app/schemas/)
- 定义 API 请求/响应格式
- Pydantic 数据验证
- 类型安全

---

## 4. 数据库设计

### 4.1 表结构

#### leaderboard 表

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 记录ID |
| player_id | VARCHAR(255) | NOT NULL, INDEX | 玩家ID |
| score | INTEGER | NOT NULL | 分数 |
| timestamp | INTEGER | NOT NULL | 提交时间戳 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

#### 索引设计
- `idx_player_score`: (player_id, score DESC) - 用于快速查询玩家最高分
- `idx_score_timestamp`: (score DESC, timestamp ASC) - 用于排行榜查询

---

## 5. 核心依赖

### 主要依赖包 (pyproject.toml)

```toml
[project]
name = "ctrail-server"
version = "0.1.0"
description = "Game leaderboard server"
requires-python = ">=3.11"

dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "sqlalchemy>=2.0.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "httpx>=0.25.0",
    "black>=23.11.0",
    "ruff>=0.1.6",
]
```

---

## 6. 配置管理

### 配置项 (app/config.py)

```python
# 主要配置项
- DATABASE_URL: SQLite 数据库路径
- API_PREFIX: API 路径前缀 (/api)
- CORS_ORIGINS: 允许的跨域来源
- LOG_LEVEL: 日志级别
- MAX_LEADERBOARD_SIZE: 排行榜最大记录数
```

---

## 7. 部署方案

### 7.1 开发环境

```bash
# 使用 uv 安装依赖
uv pip install -e ".[dev]"

# 启动开发服务器
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7.2 生产环境

```bash
# 安装生产依赖
uv pip install .

# 使用 uvicorn 启动
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 7.3 容器化部署 (可选)

```dockerfile
FROM python:3.11-slim
RUN pip install uv
COPY . /app
WORKDIR /app
RUN uv pip install --system .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 8. 性能优化

### 8.1 数据库优化
- 索引优化: 为高频查询字段建立索引
- 连接池: 使用 SQLAlchemy 连接池
- 批量操作: 大量数据使用批量插入

### 8.2 API 优化
- 异步处理: 使用 FastAPI 的异步特性
- 缓存策略: 对排行榜数据实施缓存
- 分页查询: 避免一次性返回大量数据

### 8.3 数据清理
- 定期清理过期的历史数据
- 保留每个玩家的最高分记录
- 归档旧数据

---

## 9. 安全考虑

### 9.1 API 安全
- 请求频率限制 (Rate Limiting)
- 输入验证和消毒
- CORS 配置

### 9.2 数据安全
- SQL 注入防护 (ORM 层面)
- 数据库文件访问权限控制
- 定期备份数据库

---

## 10. 监控和日志

### 10.1 日志
- 请求日志: 记录所有 API 请求
- 错误日志: 记录异常和错误
- 业务日志: 记录关键业务操作

### 10.2 监控指标
- API 响应时间
- 请求成功率
- 数据库查询性能
- 系统资源使用
