"""
Reviewer agent implementation for content review and feedback.
"""

from typing import Any, Dict, List, Optional
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from .base import BaseAgent

class ReviewerAgent(BaseAgent):
    """Agent responsible for reviewing and providing feedback on content."""
    
    def __init__(self, agent_id: str, model_name: str, config: Optional[Dict[str, Any]] = None):
        """Initialize the reviewer agent.
        
        Args:
            agent_id: Unique identifier for the agent
            model_name: Name of the model to use for review
            config: Optional configuration dictionary
        """
        super().__init__(agent_id, config)
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        
    async def initialize(self) -> None:
        """Initialize the model and tokenizer."""
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and provide review feedback.
        
        Args:
            input_data: Dictionary containing content to review and review parameters
            
        Returns:
            Dictionary containing review feedback and metadata
        """
        content = input_data.get("content", "")
        review_aspects = input_data.get("review_aspects", ["quality", "relevance", "creativity"])
        
        inputs = self.tokenizer(content, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            scores = torch.softmax(outputs.logits, dim=1)
            
        feedback = {}
        for aspect in review_aspects:
            aspect_score = float(scores[0][0])  # Assuming binary classification
            feedback[aspect] = {
                "score": aspect_score,
                "comment": self._generate_feedback(aspect, aspect_score)
            }
            
        return {
            "feedback": feedback,
            "metadata": {
                "model": self.model_name,
                "review_aspects": review_aspects
            }
        }
        
    def _generate_feedback(self, aspect: str, score: float) -> str:
        """Generate human-readable feedback based on score.
        
        Args:
            aspect: Aspect being reviewed
            score: Numerical score for the aspect
            
        Returns:
            Human-readable feedback
        """
        if score >= 0.8:
            return f"Excellent {aspect}!"
        elif score >= 0.6:
            return f"Good {aspect}, with room for improvement."
        elif score >= 0.4:
            return f"Average {aspect}, needs significant improvement."
        else:
            return f"Poor {aspect}, requires major revision."
            
    async def cleanup(self) -> None:
        """Clean up model resources."""
        if self.model is not None:
            del self.model
        if self.tokenizer is not None:
            del self.tokenizer 