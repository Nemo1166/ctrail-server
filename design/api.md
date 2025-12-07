# 游戏排行榜服务接口设计

## 1. 提交分数

### 接口定义

- **接口路径**: `POST /api/leaderboard/submit`
- **接口描述**: 提交玩家游戏分数
- **请求方式**: POST

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| player_id | string | 是 | 玩家唯一标识 |
| score | integer | 是 | 游戏分数 |
| timestamp | integer | 否 | 提交时间戳(秒)，默认为服务器当前时间 |

### 请求示例

```json
{
  "player_id": "player_12345",
  "score": 9800,
  "timestamp": 1701936000
}
```

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | integer | 状态码，0表示成功 |
| message | string | 响应消息 |
| data | object | 响应数据 |
| data.rank | integer | 当前排名 |
| data.best_score | integer | 历史最高分 |

### 响应示例

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

---

## 2. 获取排行榜

### 接口定义

- **接口路径**: `GET /api/leaderboard`
- **接口描述**: 获取游戏排行榜列表
- **请求方式**: GET

### 

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| limit | integer | 否 | 返回记录数，默认50，最大100 |
| offset | integer | 否 | 偏移量，默认0，用于分页 |
| time_range | string | 否 | 时间范围: `daily`(日榜), `weekly`(周榜), `monthly`(月榜), `all`(总榜)，默认`all` |

### 请求示例

```
GET /api/leaderboard?limit=10&offset=0&time_range=weekly
```

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | integer | 状态码，0表示成功 |
| message | string | 响应消息 |
| data | object | 响应数据 |
| data.total | integer | 总记录数 |
| data.list | array | 排行榜列表 |
| data.list[].rank | integer | 排名 |
| data.list[].player_id | string | 玩家ID |
| data.list[].score | integer | 分数 |
| data.list[].timestamp | integer | 提交时间戳 |

### 响应示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 150,
    "list": [
      {
        "rank": 1,
        "player_id": "player_99999",
        "score": 15800,
        "timestamp": 1701936000
      },
      {
        "rank": 2,
        "player_id": "player_88888",
        "score": 14500,
        "timestamp": 1701935000
      }
    ]
  }
}
```

---

## 3. 获取玩家排名

### 接口定义

- **接口路径**: `GET /api/leaderboard/player/{player_id}`
- **接口描述**: 获取指定玩家的排名信息
- **请求方式**: GET

### 路径参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| player_id | string | 是 | 玩家唯一标识 |

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| time_range | string | 否 | 时间范围: `daily`, `weekly`, `monthly`, `all`，默认`all` |

### 请求示例

```
GET /api/leaderboard/player/player_12345?time_range=all
```

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | integer | 状态码，0表示成功 |
| message | string | 响应消息 |
| data | object | 响应数据 |
| data.player_id | string | 玩家ID |
| data.rank | integer | 当前排名，未上榜为0 |
| data.score | integer | 最高分数 |
| data.timestamp | integer | 最高分提交时间戳 |
| data.total_players | integer | 总参与玩家数 |

### 响应示例

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

---

## 4. 错误码说明

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 400 | 请求参数错误 |
| 404 | 玩家不存在 |
| 500 | 服务器内部错误 |
