"""
Main API server implementation for Bumble bot.
This module provides the FastAPI server setup and configuration.
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Any

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

# Load configuration
def load_config() -> Dict[str, Any]:
    """
    Load API configuration from file.
    
    Returns:
        Dict[str, Any]: API configuration
    """
    config_path = Path(__file__).parent.parent.parent / "config" / "api_config.json"
    
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load API configuration: {e}")
        # Return default configuration
        return {
            "api": {
                "host": "0.0.0.0",
                "port": 8000,
                "debug": False,
                "reload": True,
                "workers": 4,
                "cors_origins": ["*"],
                "api_prefix": "/api/v1"
            },
            "security": {
                "secret_key": "REPLACE_WITH_SECURE_SECRET_KEY",
                "algorithm": "HS256",
                "access_token_expire_minutes": 60
            },
            "rate_limiting": {
                "enabled": True,
                "requests_per_minute": 60
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }

# Load bot settings
def load_bot_settings() -> Dict[str, Any]:
    """
    Load bot settings from file.
    
    Returns:
        Dict[str, Any]: Bot settings
    """
    settings_path = Path(__file__).parent.parent.parent / "config" / "default_settings.json"
    
    try:
        with open(settings_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load bot settings: {e}")
        return {}

# Configure logging
config = load_config()
logging_config = config.get("logging", {})
logging.basicConfig(
    level=getattr(logging, logging_config.get("level", "INFO")),
    format=logging_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Bumble Bot API",
    description="REST API for Bumble bot frontend-backend communication",
    version="1.0.0"
)

# Configure CORS
api_config = config.get("api", {})
app.add_middleware(
    CORSMiddleware,
    allow_origins=api_config.get("cors_origins", ["*"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{api_config.get('api_prefix', '')}/auth/token")

# Import and include routers
from .routes import auth, swipe, matches, messages

# Include routers with API prefix
api_prefix = api_config.get("api_prefix", "/api/v1")
app.include_router(auth.router, prefix=api_prefix)
app.include_router(swipe.router, prefix=api_prefix)
app.include_router(matches.router, prefix=api_prefix)
app.include_router(messages.router, prefix=api_prefix)

@app.get("/")
async def root():
    """
    Root endpoint that redirects to API documentation.
    """
    return {"message": "Welcome to Bumble Bot API", "docs_url": "/docs"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled exceptions.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

def start_server():
    """
    Start the API server.
    """
    uvicorn.run(
        "backend.src.api.server:app",
        host=api_config.get("host", "0.0.0.0"),
        port=api_config.get("port", 8000),
        reload=api_config.get("reload", True),
        workers=api_config.get("workers", 4)
    )

if __name__ == "__main__":
    start_server()