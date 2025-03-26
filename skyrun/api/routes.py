"""
API routes for handling requests.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List
import hashlib

from .models import (
    ContentRequest,
    ContentResponse,
    ReviewRequest,
    ReviewResponse,
    TransactionRequest,
    TransactionResponse
)
from ..agents import CoordinatorAgent
from ..blockchain import ContentRegistry, Wallet, Transaction

router = APIRouter()

# Dependency injection
async def get_coordinator() -> CoordinatorAgent:
    """Get the coordinator agent instance."""
    # In a real implementation, this would be properly initialized and managed
    coordinator = CoordinatorAgent("main_coordinator")
    await coordinator.initialize()
    return coordinator

async def get_registry() -> ContentRegistry:
    """Get the content registry contract instance."""
    # In a real implementation, this would be properly initialized
    from web3 import Web3
    web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    contract_address = "0x..."  # Would be properly configured
    contract_abi = []  # Would be properly loaded
    return ContentRegistry(web3, contract_address, contract_abi)

async def get_wallet() -> Wallet:
    """Get the wallet instance."""
    # In a real implementation, this would be properly initialized
    from web3 import Web3
    web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    return Wallet(web3)

@router.post("/content/generate", response_model=ContentResponse)
async def generate_content(
    request: ContentRequest,
    coordinator: CoordinatorAgent = Depends(get_coordinator)
) -> ContentResponse:
    """Generate content using the coordinator agent."""
    try:
        result = await coordinator.process({
            "prompt": request.prompt,
            "max_length": request.max_length,
            "temperature": request.temperature,
            "metadata": request.metadata
        })
        
        return ContentResponse(
            content=result["best_result"]["content"],
            metadata=result["best_result"]["metadata"],
            timestamp=result["best_result"]["metadata"]["timestamp"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/content/review", response_model=ReviewResponse)
async def review_content(
    request: ReviewRequest,
    coordinator: CoordinatorAgent = Depends(get_coordinator)
) -> ReviewResponse:
    """Review content using the coordinator agent."""
    try:
        result = await coordinator.reviewer_agent.process({
            "content": request.content,
            "review_aspects": request.aspects
        })
        
        # Calculate overall score
        scores = [review["score"] for review in result["feedback"].values()]
        overall_score = sum(scores) / len(scores)
        
        return ReviewResponse(
            feedback=result["feedback"],
            overall_score=overall_score,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/content/register", response_model=TransactionResponse)
async def register_content(
    request: TransactionRequest,
    registry: ContentRegistry = Depends(get_registry),
    wallet: Wallet = Depends(get_wallet)
) -> TransactionResponse:
    """Register content on the blockchain."""
    try:
        # Calculate content hash
        content_hash = hashlib.sha256(request.content_hash.encode()).hexdigest()
        
        # Register content
        tx_hash = registry.register_content(
            content_hash=content_hash,
            owner=wallet.account.address,
            metadata=request.metadata
        )
        
        # Create transaction object
        tx = Transaction(wallet.web3, tx_hash)
        receipt = tx.wait_for_receipt()
        
        return TransactionResponse(
            tx_hash=tx_hash,
            status=tx.get_status(),
            timestamp=datetime.now(),
            metadata=request.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/content/transfer", response_model=TransactionResponse)
async def transfer_content(
    request: TransactionRequest,
    registry: ContentRegistry = Depends(get_registry),
    wallet: Wallet = Depends(get_wallet)
) -> TransactionResponse:
    """Transfer content ownership on the blockchain."""
    try:
        # Calculate content hash
        content_hash = hashlib.sha256(request.content_hash.encode()).hexdigest()
        
        # Transfer ownership
        tx_hash = registry.transfer_ownership(
            content_hash=content_hash,
            from_address=wallet.account.address,
            to_address=request.metadata.get("to_address")
        )
        
        # Create transaction object
        tx = Transaction(wallet.web3, tx_hash)
        receipt = tx.wait_for_receipt()
        
        return TransactionResponse(
            tx_hash=tx_hash,
            status=tx.get_status(),
            timestamp=datetime.now(),
            metadata=request.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 