"""
Script to run the Bumble Bot API server.
"""

import os
import sys
import json
import logging
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load API configuration
config_path = Path(__file__) / "config" / "api_config.json"
try:
    with open(config_path, "r") as f:
        config = json.load(f)
        api_config = config.get("api", {})
except (FileNotFoundError, json.JSONDecodeError) as e:
    logger.error(f"Failed to load API configuration: {e}")
    api_config = {
        "host": "0.0.0.0",
        "port": 8000,
        "reload": True,
        "workers": 1
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Bumble Bot API server...")
    
    uvicorn.run(
        "src.api.server:app",
        host=api_config.get("host", "0.0.0.0"),
        port=api_config.get("port", 8000),
        reload=api_config.get("reload", True),
        workers=api_config.get("workers", 1)
    )