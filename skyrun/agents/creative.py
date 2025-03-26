"""
Creative agent implementation for content generation.
"""

from typing import Any, Dict, Optional
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from .base import BaseAgent

class CreativeAgent(BaseAgent):
    """Agent responsible for creative content generation."""
    
    def __init__(self, agent_id: str, model_name: str, config: Optional[Dict[str, Any]] = None):
        """Initialize the creative agent.
        
        Args:
            agent_id: Unique identifier for the agent
            model_name: Name of the model to use for generation
            config: Optional configuration dictionary
        """
        super().__init__(agent_id, config)
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        
    async def initialize(self) -> None:
        """Initialize the model and tokenizer."""
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and generate creative content.
        
        Args:
            input_data: Dictionary containing prompt and generation parameters
            
        Returns:
            Dictionary containing generated content and metadata
        """
        prompt = input_data.get("prompt", "")
        max_length = input_data.get("max_length", 100)
        temperature = input_data.get("temperature", 0.7)
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_length=max_length,
            temperature=temperature,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return {
            "generated_content": generated_text,
            "metadata": {
                "model": self.model_name,
                "max_length": max_length,
                "temperature": temperature
            }
        }
        
    async def cleanup(self) -> None:
        """Clean up model resources."""
        if self.model is not None:
            del self.model
        if self.tokenizer is not None:
            del self.tokenizer 