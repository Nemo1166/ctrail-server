# Godot 集成示例

## GDScript HTTP 请求示例

### 1. 创建 LeaderboardAPI 类

```gdscript
# leaderboard_api.gd
extends Node

const BASE_URL = "http://127.0.0.1:8000/api"

# 提交分数
func submit_score(player_id: String, score: int) -> void:
    var http_request = HTTPRequest.new()
    add_child(http_request)
    http_request.request_completed.connect(_on_submit_score_completed)
    
    var url = BASE_URL + "/leaderboard/submit"
    var headers = ["Content-Type: application/json"]
    var body = JSON.stringify({
        "player_id": player_id,
        "score": score
    })
    
    var error = http_request.request(url, headers, HTTPClient.METHOD_POST, body)
    if error != OK:
        push_error("提交分数失败: " + str(error))

func _on_submit_score_completed(result, response_code, headers, body):
    var json = JSON.new()
    var error = json.parse(body.get_string_from_utf8())
    
    if error == OK:
        var response = json.data
        if response.code == 0:
            print("分数提交成功!")
            print("当前排名: ", response.data.rank)
            print("最高分: ", response.data.best_score)
        else:
            push_error("提交失败: " + response.message)
    else:
        push_error("解析响应失败")

# 获取排行榜
func get_leaderboard(limit: int = 10, offset: int = 0) -> void:
    var http_request = HTTPRequest.new()
    add_child(http_request)
    http_request.request_completed.connect(_on_get_leaderboard_completed)
    
    var url = BASE_URL + "/leaderboard?limit=" + str(limit) + "&offset=" + str(offset)
    
    var error = http_request.request(url)
    if error != OK:
        push_error("获取排行榜失败: " + str(error))

func _on_get_leaderboard_completed(result, response_code, headers, body):
    var json = JSON.new()
    var error = json.parse(body.get_string_from_utf8())
    
    if error == OK:
        var response = json.data
        if response.code == 0:
            print("排行榜获取成功!")
            print("总记录数: ", response.data.total)
            for entry in response.data.entries:
                print("排名 %d: %s - %d 分" % [entry.rank, entry.player_id, entry.score])
        else:
            push_error("获取失败: " + response.message)
    else:
        push_error("解析响应失败")

# 获取玩家排名
func get_player_rank(player_id: String) -> void:
    var http_request = HTTPRequest.new()
    add_child(http_request)
    http_request.request_completed.connect(_on_get_player_rank_completed)
    
    var url = BASE_URL + "/leaderboard/player/" + player_id
    
    var error = http_request.request(url)
    if error != OK:
        push_error("获取玩家排名失败: " + str(error))

func _on_get_player_rank_completed(result, response_code, headers, body):
    var json = JSON.new()
    var error = json.parse(body.get_string_from_utf8())
    
    if error == OK:
        var response = json.data
        if response.code == 0:
            var data = response.data
            print("玩家排名信息:")
            print("玩家ID: ", data.player_id)
            print("排名: ", data.rank)
            print("分数: ", data.score)
            print("总玩家数: ", data.total_players)
        else:
            push_error("获取失败: " + response.message)
    else:
        push_error("解析响应失败")
```

### 2. 使用示例

```gdscript
# game_manager.gd
extends Node

var leaderboard_api: Node

func _ready():
    # 创建 API 实例
    leaderboard_api = preload("res://leaderboard_api.gd").new()
    add_child(leaderboard_api)

func on_game_over(player_id: String, final_score: int):
    # 游戏结束时提交分数
    leaderboard_api.submit_score(player_id, final_score)

func show_leaderboard():
    # 显示排行榜
    leaderboard_api.get_leaderboard(10, 0)

func show_player_stats(player_id: String):
    # 显示玩家统计
    leaderboard_api.get_player_rank(player_id)
```

### 3. 带信号的高级版本

```gdscript
# leaderboard_api_advanced.gd
extends Node

signal score_submitted(rank: int, best_score: int)
signal leaderboard_loaded(entries: Array)
signal player_rank_loaded(rank_data: Dictionary)
signal api_error(error_message: String)

const BASE_URL = "http://127.0.0.1:8000/api"

func submit_score(player_id: String, score: int) -> void:
    var http_request = HTTPRequest.new()
    add_child(http_request)
    http_request.request_completed.connect(func(result, code, headers, body):
        _handle_submit_score(result, code, headers, body, http_request)
    )
    
    var url = BASE_URL + "/leaderboard/submit"
    var headers = ["Content-Type: application/json"]
    var body = JSON.stringify({
        "player_id": player_id,
        "score": score
    })
    
    http_request.request(url, headers, HTTPClient.METHOD_POST, body)

func _handle_submit_score(result, response_code, headers, body, http_request):
    http_request.queue_free()
    
    var json = JSON.new()
    if json.parse(body.get_string_from_utf8()) == OK:
        var response = json.data
        if response.code == 0:
            score_submitted.emit(response.data.rank, response.data.best_score)
        else:
            api_error.emit("提交失败: " + response.message)
    else:
        api_error.emit("解析响应失败")

func get_leaderboard(limit: int = 10) -> void:
    var http_request = HTTPRequest.new()
    add_child(http_request)
    http_request.request_completed.connect(func(result, code, headers, body):
        _handle_get_leaderboard(result, code, headers, body, http_request)
    )
    
    var url = BASE_URL + "/leaderboard?limit=" + str(limit)
    http_request.request(url)

func _handle_get_leaderboard(result, response_code, headers, body, http_request):
    http_request.queue_free()
    
    var json = JSON.new()
    if json.parse(body.get_string_from_utf8()) == OK:
        var response = json.data
        if response.code == 0:
            leaderboard_loaded.emit(response.data.entries)
        else:
            api_error.emit("获取失败: " + response.message)
    else:
        api_error.emit("解析响应失败")
```

### 4. UI 集成示例

```gdscript
# leaderboard_ui.gd
extends Control

@onready var leaderboard_list = $VBoxContainer/LeaderboardList
@onready var player_rank_label = $VBoxContainer/PlayerRankLabel
@onready var leaderboard_api = $LeaderboardAPI

func _ready():
    # 连接信号
    leaderboard_api.leaderboard_loaded.connect(_on_leaderboard_loaded)
    leaderboard_api.player_rank_loaded.connect(_on_player_rank_loaded)
    leaderboard_api.api_error.connect(_on_api_error)
    
    # 加载排行榜
    refresh_leaderboard()

func refresh_leaderboard():
    leaderboard_api.get_leaderboard(10)

func _on_leaderboard_loaded(entries: Array):
    # 清空列表
    for child in leaderboard_list.get_children():
        child.queue_free()
    
    # 添加排行榜条目
    for entry in entries:
        var label = Label.new()
        label.text = "排名 %d: %s - %d 分" % [entry.rank, entry.player_id, entry.score]
        leaderboard_list.add_child(label)

func _on_player_rank_loaded(rank_data: Dictionary):
    player_rank_label.text = "你的排名: %d / %d (分数: %d)" % [
        rank_data.rank,
        rank_data.total_players,
        rank_data.score
    ]

func _on_api_error(error_message: String):
    push_error(error_message)
    # 显示错误提示
```

## 注意事项

1. **CORS 配置**: 确保服务器的 CORS 设置允许 Godot 游戏的来源
2. **错误处理**: 始终处理网络错误和 API 错误
3. **异步操作**: HTTP 请求是异步的，使用信号处理结果
4. **清理资源**: 请求完成后记得 `queue_free()` HTTPRequest 节点
5. **测试**: 在导出游戏前测试所有网络功能

## 调试技巧

```gdscript
# 启用详细日志
func _on_request_completed(result, response_code, headers, body):
    print("Result: ", result)
    print("Response Code: ", response_code)
    print("Headers: ", headers)
    print("Body: ", body.get_string_from_utf8())
```

## 生产环境配置

```gdscript
# config.gd
extends Node

const DEV_URL = "http://127.0.0.1:8000/api"
const PROD_URL = "https://your-production-server.com/api"

var BASE_URL = DEV_URL if OS.is_debug_build() else PROD_URL
```
