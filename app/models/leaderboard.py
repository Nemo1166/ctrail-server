"""Leaderboard database model."""
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Index
from app.database import Base


class Leaderboard(Base):
    """Leaderboard table model."""
    
    __tablename__ = "leaderboard"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(String(255), nullable=False, index=True)
    score = Column(Integer, nullable=False)
    timestamp = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Composite indexes for performance
    __table_args__ = (
        Index('idx_player_score', 'player_id', 'score'),
        Index('idx_score_timestamp', 'score', 'timestamp'),
    )
    
    def __repr__(self):
        return f"<Leaderboard(player_id={self.player_id}, score={self.score})>"
