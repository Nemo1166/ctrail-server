"""Pydantic schemas for leaderboard."""
from typing import Optional
from pydantic import BaseModel, Field


# Request schemas
class ScoreSubmit(BaseModel):
    """Schema for submitting a score."""
    
    player_id: str = Field(..., min_length=1, max_length=255, description="Player unique identifier")
    score: int = Field(..., ge=0, description="Game score")
    timestamp: Optional[int] = Field(None, ge=0, description="Submission timestamp (seconds)")


# Response schemas
class ScoreSubmitResponse(BaseModel):
    """Response after submitting a score."""
    
    rank: int = Field(..., description="Current rank")
    best_score: int = Field(..., description="Historical best score")


class LeaderboardEntry(BaseModel):
    """Single leaderboard entry."""
    
    rank: int = Field(..., description="Rank")
    player_id: str = Field(..., description="Player ID")
    score: int = Field(..., description="Score")
    timestamp: int = Field(..., description="Submission timestamp")
    
    class Config:
        from_attributes = True


class LeaderboardResponse(BaseModel):
    """Response for leaderboard list."""
    
    total: int = Field(..., description="Total number of records")
    entries: list[LeaderboardEntry] = Field(..., description="Leaderboard entries")


class PlayerRankResponse(BaseModel):
    """Response for player rank query."""
    
    player_id: str = Field(..., description="Player ID")
    rank: int = Field(..., description="Current rank, 0 if not ranked")
    score: int = Field(..., description="Highest score")
    timestamp: int = Field(..., description="Highest score submission timestamp")
    total_players: int = Field(..., description="Total participating players")


# Standard API response wrapper
class APIResponse(BaseModel):
    """Standard API response wrapper."""
    
    code: int = Field(0, description="Status code, 0 for success")
    message: str = Field("success", description="Response message")
    data: Optional[ScoreSubmitResponse | LeaderboardResponse | PlayerRankResponse] = None
