"""
API server implementation.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional

from .routes import router

class APIServer:
    """API server for the SkyRun platform."""
    
    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 8000,
        debug: bool = False,
        title: str = "SkyRun API",
        description: str = "API for the SkyRun decentralized AI creative platform",
        version: str = "0.1.0"
    ):
        """Initialize the API server.
        
        Args:
            host: Host to bind to
            port: Port to listen on
            debug: Whether to run in debug mode
            title: API title
            description: API description
            version: API version
        """
        self.host = host
        self.port = port
        self.debug = debug
        
        self.app = FastAPI(
            title=title,
            description=description,
            version=version
        )
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Include routers
        self.app.include_router(router, prefix="/api/v1")
        
    def start(self) -> None:
        """Start the API server."""
        uvicorn.run(
            self.app,
            host=self.host,
            port=self.port,
            debug=self.debug
        )
        
    def get_app(self) -> FastAPI:
        """Get the FastAPI application instance.
        
        Returns:
            FastAPI application instance
        """
        return self.app 