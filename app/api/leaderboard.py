"""Leaderboard API routes."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.leaderboard import (
    ScoreSubmit,
    ScoreSubmitResponse,
    LeaderboardResponse,
    PlayerRankResponse,
    APIResponse
)
from app.services.leaderboard import LeaderboardService
from app.config import settings

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.post("/submit", response_model=APIResponse)
async def submit_score(
    score_data: ScoreSubmit,
    db: Session = Depends(get_db)
):
    """
    Submit player score.
    
    Args:
        score_data: Score submission data
        db: Database session
        
    Returns:
        API response with rank and best score
    """
    try:
        result = LeaderboardService.submit_score(db, score_data)
        return APIResponse(code=0, message="success", data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=APIResponse)
async def get_leaderboard(
    limit: int = Query(
        default=settings.default_page_limit,
        ge=1,
        le=settings.max_page_limit,
        description="Number of records to return"
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Offset for pagination"
    ),
    time_range: str = Query(
        default="all",
        regex="^(daily|weekly|monthly|all)$",
        description="Time range: daily, weekly, monthly, all"
    ),
    db: Session = Depends(get_db)
):
    """
    Get leaderboard list.
    
    Args:
        limit: Number of records to return
        offset: Offset for pagination
        time_range: Time range filter
        db: Database session
        
    Returns:
        API response with leaderboard entries
    """
    try:
        result = LeaderboardService.get_leaderboard(db, limit, offset, time_range)
        return APIResponse(code=0, message="success", data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/player/{player_id}", response_model=APIResponse)
async def get_player_rank(
    player_id: str,
    time_range: str = Query(
        default="all",
        regex="^(daily|weekly|monthly|all)$",
        description="Time range: daily, weekly, monthly, all"
    ),
    db: Session = Depends(get_db)
):
    """
    Get player rank information.
    
    Args:
        player_id: Player unique identifier
        time_range: Time range filter
        db: Database session
        
    Returns:
        API response with player rank information
    """
    try:
        result = LeaderboardService.get_player_rank(db, player_id, time_range)
        if result is None:
            raise HTTPException(status_code=404, detail="Player not found")
        return APIResponse(code=0, message="success", data=result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
