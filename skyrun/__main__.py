"""
Main entry point for the SkyRun application.
"""

import asyncio
import logging
from typing import Optional

from .api import APIServer
from .config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main() -> None:
    """Main entry point."""
    try:
        # Initialize and start API server
        server = APIServer(
            host=config["API_HOST"],
            port=config["API_PORT"],
            debug=config["API_DEBUG"]
        )
        
        logger.info(f"Starting SkyRun API server on {config['API_HOST']}:{config['API_PORT']}")
        server.start()
        
    except Exception as e:
        logger.error(f"Error starting SkyRun: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 