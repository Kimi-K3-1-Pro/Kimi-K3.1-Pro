"""
Configuration module for Kimi K3.1 Pro Swarm Workstation.
Manages API keys, local model endpoints, and swarm operational parameters.
"""

import os
from dataclasses import dataclass

@dataclass
class SwarmConfig:
    # Local Distill Engine settings (runs locally for lightweight tasks)
    local_model_endpoint: str = os.getenv("KIMI_LOCAL_ENDPOINT", "http://localhost:11434/v1")
    local_model_name: str = "kimi-k3.1-distill-8b"
    
    # Cloud Full K3.1 Pro settings (2.8T parameters for heavy reasoning/refactors)
    cloud_api_key: str = os.getenv("KIMI_CLOUD_API_KEY", "your-moonshot-api-key-here")
    cloud_api_base: str = "https://api.moonshot.ai/v1"
    cloud_model_name: str = "kimi-k3.1-pro-2.8t"
    
    # Swarm parameters
    max_active_agents: int = 300
    default_complexity_threshold: float = 0.7  # Tasks above this score escalate to cloud
    
config = SwarmConfig()
