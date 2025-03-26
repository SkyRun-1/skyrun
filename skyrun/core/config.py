"""
Core configuration management for SkyRun.
"""
import os
from pathlib import Path
from typing import Dict, Any

import yaml
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Base settings class."""
    # Project paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
    ASSETS_DIR: Path = PROJECT_ROOT / "assets"
    CONFIG_DIR: Path = PROJECT_ROOT / "configs"
    
    # API settings
    API_VERSION: str = "v1"
    API_PREFIX: str = f"/api/{API_VERSION}"
    DEBUG: bool = False
    
    # AI Model settings
    MODEL_NAME: str = "open-sora-v1"
    MODEL_DEVICE: str = "cuda"
    
    # Blockchain settings
    CHAIN_ID: int = 1
    CONTRACT_ADDRESS: str = ""
    
    # Security
    SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"

class ConfigManager:
    """Configuration manager for loading and managing config files."""
    
    def __init__(self, env: str = "dev"):
        self.env = env
        self.settings = Settings()
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from YAML file."""
        config_file = self.settings.CONFIG_DIR / f"{self.env}.yaml"
        if not config_file.exists():
            config_file = self.settings.CONFIG_DIR / "default.yaml"
        
        with open(config_file) as f:
            self.config = yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)

# Global config instance
config = ConfigManager(env=os.getenv("ENV", "dev"))
settings = Settings() 