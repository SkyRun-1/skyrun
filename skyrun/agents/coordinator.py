"""
Coordinator agent implementation for managing multi-agent collaboration.
"""

from typing import Any, Dict, List, Optional
import asyncio
from datetime import datetime

from .base import BaseAgent
from .creative import CreativeAgent
from .reviewer import ReviewerAgent

class CoordinatorAgent(BaseAgent):
    """Agent responsible for coordinating the creative and review process."""
    
    def __init__(self, agent_id: str, config: Optional[Dict[str, Any]] = None):
        """Initialize the coordinator agent.
        
        Args:
            agent_id: Unique identifier for the agent
            config: Optional configuration dictionary
        """
        super().__init__(agent_id, config)
        self.creative_agent = None
        self.reviewer_agent = None
        self.workflow_history: List[Dict[str, Any]] = []
        
    async def initialize(self) -> None:
        """Initialize the creative and reviewer agents."""
        self.creative_agent = CreativeAgent(
            f"{self.agent_id}_creative",
            self.config.get("creative_model", "gpt2"),
            self.config.get("creative_config", {})
        )
        self.reviewer_agent = ReviewerAgent(
            f"{self.agent_id}_reviewer",
            self.config.get("reviewer_model", "bert-base-uncased"),
            self.config.get("reviewer_config", {})
        )
        
        await self.creative_agent.initialize()
        await self.reviewer_agent.initialize()
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and coordinate the creative workflow.
        
        Args:
            input_data: Dictionary containing workflow parameters and initial prompt
            
        Returns:
            Dictionary containing workflow results and metadata
        """
        prompt = input_data.get("prompt", "")
        max_iterations = input_data.get("max_iterations", 3)
        min_quality_score = input_data.get("min_quality_score", 0.7)
        
        current_prompt = prompt
        iteration = 0
        best_result = None
        best_score = 0
        
        while iteration < max_iterations:
            # Generate content
            generation_result = await self.creative_agent.process({
                "prompt": current_prompt,
                "max_length": input_data.get("max_length", 200),
                "temperature": input_data.get("temperature", 0.7)
            })
            
            # Review content
            review_result = await self.reviewer_agent.process({
                "content": generation_result["generated_content"],
                "review_aspects": ["quality", "relevance", "creativity"]
            })
            
            # Calculate overall score
            quality_score = review_result["feedback"]["quality"]["score"]
            
            # Update best result if better
            if quality_score > best_score:
                best_score = quality_score
                best_result = {
                    "content": generation_result["generated_content"],
                    "review": review_result["feedback"],
                    "metadata": {
                        "iteration": iteration,
                        "prompt": current_prompt,
                        "timestamp": datetime.now().isoformat()
                    }
                }
            
            # Check if quality threshold is met
            if quality_score >= min_quality_score:
                break
                
            # Update prompt for next iteration
            current_prompt = self._refine_prompt(
                current_prompt,
                review_result["feedback"]
            )
            
            iteration += 1
            
        # Record workflow history
        self.workflow_history.append({
            "timestamp": datetime.now().isoformat(),
            "iterations": iteration,
            "best_score": best_score,
            "final_prompt": current_prompt
        })
        
        return {
            "best_result": best_result,
            "workflow_summary": {
                "total_iterations": iteration,
                "best_score": best_score,
                "quality_threshold_met": best_score >= min_quality_score
            }
        }
        
    def _refine_prompt(self, current_prompt: str, feedback: Dict[str, Any]) -> str:
        """Refine the prompt based on review feedback.
        
        Args:
            current_prompt: Current prompt to refine
            feedback: Review feedback dictionary
            
        Returns:
            Refined prompt
        """
        # Simple prompt refinement based on feedback
        improvements = []
        for aspect, review in feedback.items():
            if review["score"] < 0.6:
                improvements.append(f"improve {aspect}")
                
        if improvements:
            return f"{current_prompt} (Please {', '.join(improvements)})"
        return current_prompt
        
    async def cleanup(self) -> None:
        """Clean up agent resources."""
        if self.creative_agent:
            await self.creative_agent.cleanup()
        if self.reviewer_agent:
            await self.reviewer_agent.cleanup() 