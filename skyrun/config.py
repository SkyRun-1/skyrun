"""
Configuration module for the SkyRun platform.
"""

import os
from typing import Dict, Any
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_DEBUG: bool = False
    
    # Blockchain Settings
    WEB3_PROVIDER: str = "http://localhost:8545"
    CONTRACT_ADDRESS: str = "0x..."  # Would be properly configured
    CONTRACT_ABI: list = []  # Would be properly loaded
    
    # Model Settings
    CREATIVE_MODEL: str = "gpt2"
    REVIEWER_MODEL: str = "bert-base-uncased"
    
    # Agent Settings
    MAX_ITERATIONS: int = 3
    MIN_QUALITY_SCORE: float = 0.7
    
    # Storage Settings
    STORAGE_PATH: str = "data"
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = True

def load_config() -> Dict[str, Any]:
    """Load configuration from environment and defaults.
    
    Returns:
        Configuration dictionary
    """
    settings = Settings()
    return settings.dict()

# Global configuration
config = load_config() 