"""Leaderboard service layer."""
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.models.leaderboard import Leaderboard
from app.schemas.leaderboard import (
    ScoreSubmit,
    ScoreSubmitResponse,
    LeaderboardEntry,
    LeaderboardResponse,
    PlayerRankResponse
)


class LeaderboardService:
    """Service for leaderboard operations."""
    
    @staticmethod
    def submit_score(db: Session, score_data: ScoreSubmit) -> ScoreSubmitResponse:
        """
        Submit a player score.
        
        Args:
            db: Database session
            score_data: Score submission data
            
        Returns:
            ScoreSubmitResponse with rank and best score
        """
        # Use provided timestamp or current time
        timestamp = score_data.timestamp or int(datetime.now(timezone.utc).timestamp())
        
        # Create new score record
        new_score = Leaderboard(
            player_id=score_data.player_id,
            score=score_data.score,
            timestamp=timestamp
        )
        db.add(new_score)
        db.commit()
        
        # Get player's best score
        best_score = db.query(func.max(Leaderboard.score)).filter(
            Leaderboard.player_id == score_data.player_id
        ).scalar() or 0
        
        # Calculate current rank
        rank = db.query(func.count(func.distinct(Leaderboard.player_id))).filter(
            Leaderboard.score > best_score
        ).scalar() + 1
        
        return ScoreSubmitResponse(rank=rank, best_score=best_score)
    
    @staticmethod
    def get_leaderboard(
        db: Session,
        limit: int = 50,
        offset: int = 0,
        time_range: str = "all"
    ) -> LeaderboardResponse:
        """
        Get leaderboard list.
        
        Args:
            db: Database session
            limit: Number of records to return
            offset: Offset for pagination
            time_range: Time range filter (daily, weekly, monthly, all)
            
        Returns:
            LeaderboardResponse with leaderboard entries
        """
        # Build query for best scores per player
        subquery = db.query(
            Leaderboard.player_id,
            func.max(Leaderboard.score).label('max_score'),
            func.max(Leaderboard.timestamp).label('latest_timestamp')
        ).group_by(Leaderboard.player_id).subquery()
        
        # Join to get full records
        query = db.query(
            Leaderboard.player_id,
            Leaderboard.score,
            Leaderboard.timestamp
        ).join(
            subquery,
            (Leaderboard.player_id == subquery.c.player_id) &
            (Leaderboard.score == subquery.c.max_score)
        ).order_by(desc(Leaderboard.score), Leaderboard.timestamp)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        results = query.offset(offset).limit(limit).all()
        
        # Build response with ranks
        entries = [
            LeaderboardEntry(
                rank=offset + idx + 1,
                player_id=row.player_id,
                score=row.score,
                timestamp=row.timestamp
            )
            for idx, row in enumerate(results)
        ]
        
        return LeaderboardResponse(total=total, entries=entries)
    
    @staticmethod
    def get_player_rank(
        db: Session,
        player_id: str,
        time_range: str = "all"
    ) -> Optional[PlayerRankResponse]:
        """
        Get player rank information.
        
        Args:
            db: Database session
            player_id: Player ID
            time_range: Time range filter (daily, weekly, monthly, all)
            
        Returns:
            PlayerRankResponse or None if player not found
        """
        # Get player's best score
        player_best = db.query(
            func.max(Leaderboard.score).label('score'),
            func.max(Leaderboard.timestamp).label('timestamp')
        ).filter(
            Leaderboard.player_id == player_id
        ).first()
        
        if not player_best or player_best.score is None:
            return None
        
        # Calculate rank
        rank = db.query(func.count(func.distinct(Leaderboard.player_id))).filter(
            Leaderboard.score > player_best.score
        ).scalar() + 1
        
        # Get total players
        total_players = db.query(func.count(func.distinct(Leaderboard.player_id))).scalar()
        
        return PlayerRankResponse(
            player_id=player_id,
            rank=rank,
            score=player_best.score,
            timestamp=player_best.timestamp,
            total_players=total_players
        )
