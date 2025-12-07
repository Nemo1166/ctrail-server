"""Application configuration."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "Game Leaderboard Server"
    api_prefix: str = "/api"
    
    # Database
    database_url: str = "sqlite:///./leaderboard.db"
    
    # CORS
    cors_origins: list[str] = ["*"]
    
    # Leaderboard
    max_leaderboard_size: int = 1000
    default_page_limit: int = 50
    max_page_limit: int = 100
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
