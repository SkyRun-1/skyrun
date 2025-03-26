"""
Tests for the agents module.
"""

import pytest
import torch
from unittest.mock import Mock, patch

from skyrun.agents import CreativeAgent, ReviewerAgent, CoordinatorAgent

@pytest.fixture
def mock_model():
    """Create a mock model for testing."""
    model = Mock()
    model.device = torch.device("cpu")
    return model

@pytest.fixture
def mock_tokenizer():
    """Create a mock tokenizer for testing."""
    tokenizer = Mock()
    tokenizer.eos_token_id = 50256
    return tokenizer

@pytest.mark.asyncio
async def test_creative_agent_initialization(mock_model, mock_tokenizer):
    """Test creative agent initialization."""
    with patch("skyrun.agents.creative.AutoModelForCausalLM.from_pretrained", return_value=mock_model), \
         patch("skyrun.agents.creative.AutoTokenizer.from_pretrained", return_value=mock_tokenizer):
        
        agent = CreativeAgent("test_creative", "test_model")
        await agent.initialize()
        
        assert agent.model == mock_model
        assert agent.tokenizer == mock_tokenizer

@pytest.mark.asyncio
async def test_reviewer_agent_initialization(mock_model, mock_tokenizer):
    """Test reviewer agent initialization."""
    with patch("skyrun.agents.reviewer.AutoModelForSequenceClassification.from_pretrained", return_value=mock_model), \
         patch("skyrun.agents.reviewer.AutoTokenizer.from_pretrained", return_value=mock_tokenizer):
        
        agent = ReviewerAgent("test_reviewer", "test_model")
        await agent.initialize()
        
        assert agent.model == mock_model
        assert agent.tokenizer == mock_tokenizer

@pytest.mark.asyncio
async def test_coordinator_agent_initialization():
    """Test coordinator agent initialization."""
    coordinator = CoordinatorAgent("test_coordinator")
    await coordinator.initialize()
    
    assert coordinator.creative_agent is not None
    assert coordinator.reviewer_agent is not None

@pytest.mark.asyncio
async def test_creative_agent_process(mock_model, mock_tokenizer):
    """Test creative agent content generation."""
    mock_model.generate.return_value = torch.tensor([[1, 2, 3]])
    mock_tokenizer.decode.return_value = "Generated content"
    
    with patch("skyrun.agents.creative.AutoModelForCausalLM.from_pretrained", return_value=mock_model), \
         patch("skyrun.agents.creative.AutoTokenizer.from_pretrained", return_value=mock_tokenizer):
        
        agent = CreativeAgent("test_creative", "test_model")
        await agent.initialize()
        
        result = await agent.process({
            "prompt": "Test prompt",
            "max_length": 100,
            "temperature": 0.7
        })
        
        assert result["generated_content"] == "Generated content"
        assert "metadata" in result

@pytest.mark.asyncio
async def test_reviewer_agent_process(mock_model, mock_tokenizer):
    """Test reviewer agent content review."""
    mock_model.return_value.logits = torch.tensor([[0.8, 0.2]])
    
    with patch("skyrun.agents.reviewer.AutoModelForSequenceClassification.from_pretrained", return_value=mock_model), \
         patch("skyrun.agents.reviewer.AutoTokenizer.from_pretrained", return_value=mock_tokenizer):
        
        agent = ReviewerAgent("test_reviewer", "test_model")
        await agent.initialize()
        
        result = await agent.process({
            "content": "Test content",
            "review_aspects": ["quality"]
        })
        
        assert "feedback" in result
        assert "quality" in result["feedback"]

@pytest.mark.asyncio
async def test_coordinator_agent_process():
    """Test coordinator agent workflow."""
    coordinator = CoordinatorAgent("test_coordinator")
    await coordinator.initialize()
    
    result = await coordinator.process({
        "prompt": "Test prompt",
        "max_iterations": 1,
        "min_quality_score": 0.5
    })
    
    assert "best_result" in result
    assert "workflow_summary" in result 