"""
Hybrid Engine module.
Evaluates task complexity and routes execution dynamically between the 
on-device local distilled companion and the full 2.8T cloud model.
"""

import logging
from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HybridEngine")

class HybridEngine:
    def __init__(self):
        logger.info("Initializing Hybrid Engine (Local Distill + Cloud Full K3.1 Pro)...")

    def evaluate_complexity(self, prompt: str, context_tokens: int) -> float:
        """
        Evaluate task complexity score based on prompt length, context size, 
        and keyword indicators (e.g., refactor, architecture, million-token).
        """
        score = 0.0
        
        # Factor 1: Context size weight (large contexts lean towards cloud full)
        if context_tokens > 50000:
            score += 0.5
        elif context_tokens > 10000:
            score += 0.3
            
        # Factor 2: Prompt length & depth indicators
        heavy_keywords = ["refactor", "architecture", "million-token", "deep research", "analysis", "audit"]
        if any(keyword in prompt.lower() for keyword in heavy_keywords):
            score += 0.4
            
        # Factor 3: Length of prompt
        if len(prompt.split()) > 300:
            score += 0.3
            
        return min(score, 1.0)

    def route_task(self, prompt: str, context_tokens: int = 1000) -> str:
        """
        Determine whether to execute locally or escalate to the cloud.
        Returns 'local' or 'cloud'.
        """
        complexity_score = self.evaluate_complexity(prompt, context_tokens)
        
        if complexity_score >= config.default_complexity_threshold:
            logger.info(f"Escalating task to Cloud Full K3.1 Pro (Complexity Score: {complexity_score:.2f})")
            return "cloud"
        else:
            logger.info(f"Routing task to Local Distill Companion (Complexity Score: {complexity_score:.2f})")
            return "local"

    def execute(self, prompt: str, context_tokens: int = 1000) -> dict:
        """
        Execute the task using the appropriate backend engine.
        """
        engine_target = self.route_task(prompt, context_tokens)
        
        if engine_target == "local":
            # Call local distilled model endpoint
            response = f"[Local Distill Execution] Processed locally via {config.local_model_name}."
        else:
            # Call full K3.1 Pro cloud endpoint
            response = f"[Cloud Full Execution] Processed via {config.cloud_model_name} (2.8T Parameters)."
            
        return {
            "engine": engine_target,
            "response": response
        }
