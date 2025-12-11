"""清除指定玩家ID的成绩记录脚本。

该脚本用于在服务器上清除指定玩家的成绩记录。
支持精确匹配和通配符匹配（使用SQL LIKE语法）。

使用方法：
1. 在 PLAYER_IDS 列表中指定要清除的玩家ID
2. 支持通配符：
   - % 匹配任意多个字符
   - _ 匹配单个字符
3. 运行脚本：python clear_scores.py

示例：
    PLAYER_IDS = [
        "player123",      # 精确匹配
        "test_%",         # 匹配所有以 test_ 开头的ID
        "%_bot",          # 匹配所有以 _bot 结尾的ID
        "demo%player%",   # 匹配包含 demo 和 player 的ID
    ]
"""

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from app.models.leaderboard import Leaderboard
from app.config import settings

# ============================================
# 配置区域：在此列表中添加要清除的玩家ID
# ============================================
PLAYER_IDS = [
    # 在下面添加要清除的玩家ID
    # 示例：
    # "player123",      # 精确匹配
    # "test_%",         # 匹配所有以 test_ 开头的玩家
    # "%_bot",          # 匹配所有以 _bot 结尾的玩家
    
]

# 是否显示详细信息（包括将要删除的记录）
VERBOSE = True

# 是否需要确认（设为False则直接删除，不询问）
REQUIRE_CONFIRMATION = True

# ============================================


def has_wildcard(pattern: str) -> bool:
    """检查字符串是否包含通配符。"""
    return '%' in pattern or '_' in pattern


def clear_scores():
    """清除指定玩家ID的成绩记录。"""
    
    if not PLAYER_IDS:
        print("❌ 错误：PLAYER_IDS 列表为空，请先配置要清除的玩家ID")
        return
    
    # 创建数据库连接
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # 构建查询条件
        conditions = []
        for player_id in PLAYER_IDS:
            if has_wildcard(player_id):
                conditions.append(Leaderboard.player_id.like(player_id))
            else:
                conditions.append(Leaderboard.player_id == player_id)
        
        # 查询匹配的记录
        query = db.query(Leaderboard).filter(or_(*conditions))
        matched_records = query.all()
        
        if not matched_records:
            print("✅ 没有找到匹配的记录")
            return
        
        # 显示匹配的记录
        print(f"\n找到 {len(matched_records)} 条匹配的记录：")
        print("=" * 80)
        
        if VERBOSE:
            # 按玩家ID分组统计
            player_stats = {}
            for record in matched_records:
                pid = record.player_id
                if pid not in player_stats:
                    player_stats[pid] = {
                        'count': 0,
                        'best_score': record.score,
                        'records': []
                    }
                player_stats[pid]['count'] += 1
                player_stats[pid]['best_score'] = max(player_stats[pid]['best_score'], record.score)
                player_stats[pid]['records'].append(record)
            
            # 显示每个玩家的统计信息
            for pid, stats in sorted(player_stats.items()):
                print(f"\n玩家ID: {pid}")
                print(f"  记录数: {stats['count']}")
                print(f"  最高分: {stats['best_score']}")
                
                if stats['count'] <= 5:
                    # 如果记录少于等于5条，显示所有记录
                    for record in stats['records']:
                        print(f"    - ID:{record.id}, 分数:{record.score}, "
                              f"时间:{record.timestamp}, 创建:{record.created_at}")
                else:
                    # 否则只显示前3条和后2条
                    print("  前3条记录:")
                    for record in stats['records'][:3]:
                        print(f"    - ID:{record.id}, 分数:{record.score}, "
                              f"时间:{record.timestamp}, 创建:{record.created_at}")
                    print(f"  ... (省略 {stats['count'] - 5} 条) ...")
                    print("  最后2条记录:")
                    for record in stats['records'][-2:]:
                        print(f"    - ID:{record.id}, 分数:{record.score}, "
                              f"时间:{record.timestamp}, 创建:{record.created_at}")
        else:
            # 简化显示
            player_counts = {}
            for record in matched_records:
                player_counts[record.player_id] = player_counts.get(record.player_id, 0) + 1
            
            for pid, count in sorted(player_counts.items()):
                print(f"  - {pid}: {count} 条记录")
        
        print("=" * 80)
        
        # 确认删除
        if REQUIRE_CONFIRMATION:
            confirmation = input(f"\n确认删除这 {len(matched_records)} 条记录吗? (yes/no): ")
            if confirmation.lower() not in ['yes', 'y', '是']:
                print("❌ 操作已取消")
                return
        
        # 执行删除
        deleted_count = query.delete(synchronize_session=False)
        db.commit()
        
        print(f"\n✅ 成功删除 {deleted_count} 条记录")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ 错误：{e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 80)
    print("成绩清除脚本")
    print("=" * 80)
    print(f"\n配置的玩家ID模式（共 {len(PLAYER_IDS)} 个）:")
    for idx, pid in enumerate(PLAYER_IDS, 1):
        pattern_type = "通配符匹配" if has_wildcard(pid) else "精确匹配"
        print(f"  {idx}. {pid} ({pattern_type})")
    print()
    
    clear_scores()
