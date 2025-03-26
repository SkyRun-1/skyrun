"""
API models for request/response handling.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ContentRequest(BaseModel):
    """Request model for content generation."""
    prompt: str = Field(..., description="Prompt for content generation")
    max_length: Optional[int] = Field(200, description="Maximum length of generated content")
    temperature: Optional[float] = Field(0.7, description="Temperature for generation")
    metadata: Optional[Dict] = Field(default_factory=dict, description="Additional metadata")

class ContentResponse(BaseModel):
    """Response model for content generation."""
    content: str = Field(..., description="Generated content")
    metadata: Dict = Field(..., description="Generation metadata")
    timestamp: datetime = Field(default_factory=datetime.now, description="Generation timestamp")

class ReviewRequest(BaseModel):
    """Request model for content review."""
    content: str = Field(..., description="Content to review")
    aspects: List[str] = Field(default_factory=lambda: ["quality", "relevance", "creativity"],
                             description="Aspects to review")

class ReviewResponse(BaseModel):
    """Response model for content review."""
    feedback: Dict[str, Dict[str, float]] = Field(..., description="Review feedback by aspect")
    overall_score: float = Field(..., description="Overall review score")
    timestamp: datetime = Field(default_factory=datetime.now, description="Review timestamp")

class TransactionRequest(BaseModel):
    """Request model for blockchain transaction."""
    content_hash: str = Field(..., description="Hash of the content")
    action: str = Field(..., description="Transaction action (register/transfer)")
    metadata: Optional[Dict] = Field(default_factory=dict, description="Transaction metadata")

class TransactionResponse(BaseModel):
    """Response model for blockchain transaction."""
    tx_hash: str = Field(..., description="Transaction hash")
    status: str = Field(..., description="Transaction status")
    timestamp: datetime = Field(default_factory=datetime.now, description="Transaction timestamp")
    metadata: Optional[Dict] = Field(default_factory=dict, description="Transaction metadata") 