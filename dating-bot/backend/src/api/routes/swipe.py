"""
Swiping routes for the API.
This module provides endpoints for controlling swiping functionality.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional, List, Any

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, Field

from ..utils.response import success_response, error_response
from ...bumble_bot.bot import BumbleBot
from ..routes.auth import get_current_active_user, User

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/swipe",
    tags=["swiping"],
    responses={401: {"description": "Unauthorized"}},
)

# Load bot settings
settings_path = Path(__file__).parent.parent.parent.parent / "config" / "default_settings.json"
try:
    with open(settings_path, "r") as f:
        settings = json.load(f)
        swipe_settings = settings.get("swiping", {})
except (FileNotFoundError, json.JSONDecodeError) as e:
    logger.error(f"Failed to load bot settings: {e}")
    swipe_settings = {
        "default_count": 50,
        "default_like_ratio": 0.7,
        "default_delay": 2,
        "max_swipes_per_day": 100
    }

# Global bot instance (in a production app, this would be managed differently)
bot_instance = None

# Models
class SwipeConfig(BaseModel):
    count: int = Field(
        default=swipe_settings.get("default_count", 50),
        ge=1,
        le=swipe_settings.get("max_swipes_per_day", 100),
        description="Number of profiles to swipe on"
    )
    like_ratio: float = Field(
        default=swipe_settings.get("default_like_ratio", 0.7),
        ge=0.0,
        le=1.0,
        description="Ratio of right swipes (likes) to total swipes"
    )
    delay: int = Field(
        default=swipe_settings.get("default_delay", 2),
        ge=1,
        le=10,
        description="Delay between swipes in seconds"
    )

class BotConfig(BaseModel):
    headless: bool = Field(
        default=True,
        description="Whether to run the browser in headless mode"
    )
    profile_path: Optional[str] = Field(
        default=None,
        description="Path to Chrome profile to use (for maintaining login sessions)"
    )

class SwipeStatus(BaseModel):
    is_running: bool
    total_swipes: int = 0
    likes: int = 0
    passes: int = 0
    remaining: int = 0
    config: Optional[SwipeConfig] = None

# Swipe status tracking
swipe_status = SwipeStatus(is_running=False)

def get_bot():
    """
    Get or create the bot instance.
    
    Returns:
        BumbleBot: Bot instance
    """
    global bot_instance
    if bot_instance is None:
        logger.info("Creating new bot instance")
        bot_instance = BumbleBot(headless=True)
    return bot_instance

def close_bot():
    """
    Close the bot instance.
    """
    global bot_instance
    if bot_instance:
        logger.info("Closing bot instance")
        bot_instance.close()
        bot_instance = None

def run_auto_swipe(count: int, like_ratio: float, delay: int):
    """
    Run auto-swipe in the background.
    
    Args:
        count: Number of profiles to swipe on
        like_ratio: Ratio of right swipes (likes) to total swipes
        delay: Delay between swipes in seconds
    """
    global swipe_status
    
    try:
        bot = get_bot()
        
        # Update status
        swipe_status.is_running = True
        swipe_status.total_swipes = count
        swipe_status.likes = 0
        swipe_status.passes = 0
        swipe_status.remaining = count
        swipe_status.config = SwipeConfig(count=count, like_ratio=like_ratio, delay=delay)
        
        # Start bot if not already started
        bot.start()
        
        # Run auto-swipe
        bot.auto_swipe(count=count, like_ratio=like_ratio, delay=delay)
        
        # Update status
        swipe_status.is_running = False
        swipe_status.likes = int(count * like_ratio)
        swipe_status.passes = count - swipe_status.likes
        swipe_status.remaining = 0
        
    except Exception as e:
        logger.error(f"Error in auto-swipe: {e}", exc_info=True)
        swipe_status.is_running = False
        
        # Don't close the bot on error to allow for debugging
        # close_bot()

@router.post("/start")
async def start_swiping(
    config: SwipeConfig,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user)
):
    """
    Start auto-swiping.
    
    Args:
        config: Swipe configuration
        background_tasks: Background tasks
        current_user: Current user
        
    Returns:
        Dict: Success message
    """
    global swipe_status
    
    if swipe_status.is_running:
        return error_response(
            message="Swiping is already running",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Start auto-swipe in the background
    background_tasks.add_task(
        run_auto_swipe,
        count=config.count,
        like_ratio=config.like_ratio,
        delay=config.delay
    )
    
    return success_response(
        message="Auto-swipe started",
        data={
            "config": config.dict()
        }
    )

@router.post("/stop")
async def stop_swiping(current_user: User = Depends(get_current_active_user)):
    """
    Stop auto-swiping.
    
    Args:
        current_user: Current user
        
    Returns:
        Dict: Success message
    """
    global swipe_status
    
    if not swipe_status.is_running:
        return error_response(
            message="Swiping is not running",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Close bot to stop swiping
    close_bot()
    
    # Update status
    swipe_status.is_running = False
    
    return success_response(
        message="Auto-swipe stopped"
    )

@router.get("/status")
async def get_swipe_status(current_user: User = Depends(get_current_active_user)):
    """
    Get the current swipe status.
    
    Args:
        current_user: Current user
        
    Returns:
        Dict: Swipe status
    """
    global swipe_status
    
    return success_response(
        data=swipe_status.dict(),
        message="Swipe status retrieved"
    )

@router.post("/configure")
async def configure_bot(
    config: BotConfig,
    current_user: User = Depends(get_current_active_user)
):
    """
    Configure the bot.
    
    Args:
        config: Bot configuration
        current_user: Current user
        
    Returns:
        Dict: Success message
    """
    global bot_instance
    
    # Close existing bot if any
    close_bot()
    
    # Create new bot with specified configuration
    bot_instance = BumbleBot(
        headless=config.headless,
        profile_path=config.profile_path
    )
    
    return success_response(
        message="Bot configured successfully",
        data={
            "config": config.dict()
        }
    )

@router.post("/login/facebook")
async def login_with_facebook(
    email: str,
    password: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Login to Bumble with Facebook.
    
    Args:
        email: Facebook email
        password: Facebook password
        current_user: Current user
        
    Returns:
        Dict: Success message
    """
    try:
        bot = get_bot()
        bot.start()
        bot.login_with_facebook(email, password)
        
        return success_response(
            message="Logged in with Facebook successfully"
        )
    except Exception as e:
        logger.error(f"Error logging in with Facebook: {e}", exc_info=True)
        return error_response(
            message=f"Failed to login with Facebook: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.post("/login/phone")
async def login_with_phone(
    phone_number: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Login to Bumble with phone number.
    
    Args:
        phone_number: Phone number
        current_user: Current user
        
    Returns:
        Dict: Success message
    """
    try:
        bot = get_bot()
        bot.start()
        bot.login_with_phone(phone_number)
        
        return success_response(
            message="Phone login initiated successfully"
        )
    except Exception as e:
        logger.error(f"Error logging in with phone: {e}", exc_info=True)
        return error_response(
            message=f"Failed to login with phone: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )