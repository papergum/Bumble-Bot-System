"""
Message routes for the API.
This module provides endpoints for message filtering and conversation management.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from pydantic import BaseModel, Field

from ..utils.response import success_response, error_response
from ...bumble_bot.bot import BumbleBot
from ...message_filter.filter import TimewasterFilter
from ...message_filter.analyzer import MessageAnalyzer
from ..routes.auth import get_current_active_user, User
from ..routes.swipe import get_bot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/messages",
    tags=["messages"],
    responses={401: {"description": "Unauthorized"}},
)

# Load filter settings
settings_path = Path(__file__).parent.parent.parent.parent / "config" / "default_settings.json"
try:
    with open(settings_path, "r") as f:
        settings = json.load(f)
        filter_settings = settings.get("message_filter", {})
        analyzer_settings = settings.get("message_analyzer", {})
except (FileNotFoundError, json.JSONDecodeError) as e:
    logger.error(f"Failed to load filter settings: {e}")
    filter_settings = {}
    analyzer_settings = {}

# Create filter and analyzer instances
timewaster_filter = TimewasterFilter(config=filter_settings)
message_analyzer = MessageAnalyzer(config=analyzer_settings)

# Models
class FilterConfig(BaseModel):
    min_message_length: int = Field(
        default=filter_settings.get("min_message_length", 5),
        ge=1,
        le=50,
        description="Minimum message length to consider"
    )
    max_response_time: int = Field(
        default=filter_settings.get("max_response_time", 86400),
        ge=60,
        le=604800,  # 1 week in seconds
        description="Maximum acceptable response time in seconds"
    )
    min_engagement_score: float = Field(
        default=filter_settings.get("min_engagement_score", 0.5),
        ge=0.0,
        le=1.0,
        description="Minimum engagement score to consider"
    )
    min_question_ratio: float = Field(
        default=filter_settings.get("min_question_ratio", 0.2),
        ge=0.0,
        le=1.0,
        description="Minimum ratio of questions to messages"
    )
    max_one_word_ratio: float = Field(
        default=filter_settings.get("max_one_word_ratio", 0.5),
        ge=0.0,
        le=1.0,
        description="Maximum ratio of one-word responses"
    )
    red_flag_patterns: List[str] = Field(
        default=filter_settings.get("red_flag_patterns", [
            "(?i)instagram",
            "(?i)snapchat",
            "(?i)follow me"
        ]),
        description="Regex patterns for red flags"
    )

class Message(BaseModel):
    content: str
    timestamp: Optional[int] = None
    sender: str = "user"  # "user" or "match"

class Conversation(BaseModel):
    match_id: str
    match_name: str
    messages: List[Message]

class FilterResult(BaseModel):
    is_timewaster: bool
    confidence: float
    overall_score: float
    content_score: float
    pattern_score: float
    time_score: float
    flags: List[str]
    reason: str

class AnalysisResult(BaseModel):
    message_count: int
    avg_length: float
    overall_engagement: float
    sentiment_distribution: Dict[str, int]
    question_ratio: float
    flow_score: float
    topics: List[str]

@router.get("/all")
async def get_all_messages(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all messages from all matches.
    
    Args:
        current_user: Current user
        
    Returns:
        Dict: All messages
    """
    try:
        # In a real implementation, this would use the bot to get all messages
        # bot = get_bot()
        # messages = bot.get_messages()
        
        # For now, use mock data
        mock_conversations = {
            "match1": {
                "match_id": "match1",
                "match_name": "Emma",
                "messages": [
                    {"content": "Hey there!", "timestamp": 1620984600, "sender": "match"},
                    {"content": "Hi! How are you?", "timestamp": 1620984900, "sender": "user"},
                    {"content": "I'm good, thanks! What do you do for fun?", "timestamp": 1620985200, "sender": "match"}
                ]
            },
            "match2": {
                "match_id": "match2",
                "match_name": "Olivia",
                "messages": [
                    {"content": "Hello!", "timestamp": 1620984000, "sender": "match"},
                    {"content": "Hey, nice to meet you!", "timestamp": 1620984300, "sender": "user"},
                    {"content": "Likewise! What brings you to Bumble?", "timestamp": 1620984600, "sender": "match"}
                ]
            }
        }
        
        return success_response(
            data={"conversations": mock_conversations},
            message="All messages retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Error getting all messages: {e}", exc_info=True)
        return error_response(
            message=f"Failed to get messages: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.post("/filter")
async def filter_conversation(
    conversation: Conversation,
    current_user: User = Depends(get_current_active_user)
):
    """
    Filter a conversation to detect potential timewasters.
    
    Args:
        conversation: Conversation to filter
        current_user: Current user
        
    Returns:
        Dict: Filter results
    """
    try:
        # Extract messages and timestamps
        messages = [msg.content for msg in conversation.messages]
        timestamps = [msg.timestamp for msg in conversation.messages if msg.timestamp is not None]
        
        # Analyze conversation
        result = timewaster_filter.analyze_conversation(messages, timestamps)
        
        return success_response(
            data=result,
            message="Conversation filtered successfully"
        )
    except Exception as e:
        logger.error(f"Error filtering conversation: {e}", exc_info=True)
        return error_response(
            message=f"Failed to filter conversation: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.post("/analyze")
async def analyze_conversation(
    conversation: Conversation,
    current_user: User = Depends(get_current_active_user)
):
    """
    Analyze a conversation to extract insights.
    
    Args:
        conversation: Conversation to analyze
        current_user: Current user
        
    Returns:
        Dict: Analysis results
    """
    try:
        # Extract messages
        messages = [msg.content for msg in conversation.messages]
        
        # Analyze conversation
        result = message_analyzer.analyze_conversation(messages)
        
        return success_response(
            data=result,
            message="Conversation analyzed successfully"
        )
    except Exception as e:
        logger.error(f"Error analyzing conversation: {e}", exc_info=True)
        return error_response(
            message=f"Failed to analyze conversation: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.post("/filter/config")
async def update_filter_config(
    config: FilterConfig,
    current_user: User = Depends(get_current_active_user)
):
    """
    Update the timewaster filter configuration.
    
    Args:
        config: New filter configuration
        current_user: Current user
        
    Returns:
        Dict: Success message
    """
    try:
        global timewaster_filter
        
        # Update filter configuration
        new_config = {
            "min_message_length": config.min_message_length,
            "max_response_time": config.max_response_time,
            "min_engagement_score": config.min_engagement_score,
            "min_question_ratio": config.min_question_ratio,
            "max_one_word_ratio": config.max_one_word_ratio,
            "red_flag_patterns": config.red_flag_patterns
        }
        
        # Create new filter with updated config
        timewaster_filter = TimewasterFilter(config=new_config)
        
        # In a real implementation, we would also update the config file
        # with open(settings_path, "r") as f:
        #     settings = json.load(f)
        # settings["message_filter"] = new_config
        # with open(settings_path, "w") as f:
        #     json.dump(settings, f, indent=2)
        
        return success_response(
            data={"config": new_config},
            message="Filter configuration updated successfully"
        )
    except Exception as e:
        logger.error(f"Error updating filter config: {e}", exc_info=True)
        return error_response(
            message=f"Failed to update filter configuration: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/filter/config")
async def get_filter_config(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get the current timewaster filter configuration.
    
    Args:
        current_user: Current user
        
    Returns:
        Dict: Current filter configuration
    """
    try:
        # Get current filter configuration
        config = {
            "min_message_length": timewaster_filter.thresholds.get("min_message_length", 5),
            "max_response_time": timewaster_filter.thresholds.get("max_response_time", 86400),
            "min_engagement_score": timewaster_filter.thresholds.get("min_engagement_score", 0.5),
            "min_question_ratio": timewaster_filter.thresholds.get("min_question_ratio", 0.2),
            "max_one_word_ratio": timewaster_filter.thresholds.get("max_one_word_ratio", 0.5),
            "red_flag_patterns": timewaster_filter.red_flag_patterns
        }
        
        return success_response(
            data={"config": config},
            message="Filter configuration retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Error getting filter config: {e}", exc_info=True)
        return error_response(
            message=f"Failed to get filter configuration: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.post("/filter/all")
async def filter_all_conversations(
    current_user: User = Depends(get_current_active_user)
):
    """
    Filter all conversations to detect potential timewasters.
    
    Args:
        current_user: Current user
        
    Returns:
        Dict: Filter results for all conversations
    """
    try:
        # In a real implementation, this would use the bot to get all messages
        # bot = get_bot()
        # conversations = bot.get_messages()
        
        # For now, use mock data
        mock_conversations = {
            "Emma": [
                "Hey there!",
                "I'm good, thanks! What do you do for fun?"
            ],
            "Olivia": [
                "Hello!",
                "Likewise! What brings you to Bumble?"
            ]
        }
        
        # Filter all conversations
        results = timewaster_filter.filter_conversations(mock_conversations)
        
        return success_response(
            data={"results": results},
            message="All conversations filtered successfully"
        )
    except Exception as e:
        logger.error(f"Error filtering all conversations: {e}", exc_info=True)
        return error_response(
            message=f"Failed to filter conversations: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )