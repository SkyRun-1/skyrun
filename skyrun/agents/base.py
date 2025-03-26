"""
Base agent implementation for SkyRun.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from ..core.logging import get_logger

logger = get_logger(__name__)

class BaseAgent(ABC):
    """Base class for all agents in SkyRun."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """Initialize the agent.
        
        Args:
            name: Agent name
            config: Agent configuration
        """
        self.name = name
        self.config = config or {}
        self.logger = get_logger(f"agent.{name}")
        self.initialize()
    
    def initialize(self) -> None:
        """Initialize agent resources."""
        self.logger.info(f"Initializing agent: {self.name}")
        self._load_models()
        self._setup_resources()
    
    @abstractmethod
    def _load_models(self) -> None:
        """Load AI models required by the agent."""
        pass
    
    @abstractmethod
    def _setup_resources(self) -> None:
        """Setup additional resources required by the agent."""
        pass
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data.
        
        Args:
            input_data: Input data for processing
        
        Returns:
            Processing results
        """
        pass
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data.
        
        Args:
            input_data: Input data to validate
        
        Returns:
            True if valid, False otherwise
        """
        return True
    
    def cleanup(self) -> None:
        """Cleanup agent resources."""
        self.logger.info(f"Cleaning up agent: {self.name}")
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        self.cleanup() 