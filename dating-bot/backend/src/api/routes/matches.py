"""
Match routes for the API.
This module provides endpoints for retrieving match information.
"""

import logging
from typing import Dict, List, Optional, Any

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field

from ..utils.response import success_response, error_response, pagination_response
from ...bumble_bot.bot import BumbleBot
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
    prefix="/matches",
    tags=["matches"],
    responses={401: {"description": "Unauthorized"}},
)

# Models
class MatchProfile(BaseModel):
    id: str
    name: str
    age: Optional[int] = None
    bio: Optional[str] = None
    distance: Optional[str] = None
    photos: List[str] = []
    last_active: Optional[str] = None
    is_new: bool = False

class MatchList(BaseModel):
    matches: List[MatchProfile]
    total: int
    page: int
    page_size: int

# Mock data for development (in production, this would come from the bot)
# This is just for API structure demonstration
mock_matches = [
    {
        "id": "match1",
        "name": "Emma",
        "age": 28,
        "bio": "Love hiking and photography",
        "distance": "5 miles away",
        "photos": ["photo1.jpg", "photo2.jpg"],
        "last_active": "2 hours ago",
        "is_new": True
    },
    {
        "id": "match2",
        "name": "Olivia",
        "age": 26,
        "bio": "Foodie and travel enthusiast",
        "distance": "10 miles away",
        "photos": ["photo3.jpg"],
        "last_active": "1 day ago",
        "is_new": False
    }
]

@router.get("", response_model=MatchList)
async def get_matches(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=50, description="Items per page"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all matches.
    
    Args:
        page: Page number
        page_size: Items per page
        current_user: Current user
        
    Returns:
        MatchList: List of matches
    """
    try:
        # In a real implementation, this would use the bot to get matches
        # bot = get_bot()
        # matches_data = bot.navigator.get_matches()
        
        # For now, use mock data
        total = len(mock_matches)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_matches = mock_matches[start_idx:end_idx]
        
        return pagination_response(
            data=page_matches,
            total=total,
            page=page,
            page_size=page_size,
            message="Matches retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Error getting matches: {e}", exc_info=True)
        return error_response(
            message=f"Failed to get matches: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/{match_id}")
async def get_match(
    match_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific match by ID.
    
    Args:
        match_id: Match ID
        current_user: Current user
        
    Returns:
        Dict: Match details
    """
    try:
        # In a real implementation, this would use the bot to get match details
        # bot = get_bot()
        # match_data = bot.navigator.get_match(match_id)
        
        # For now, use mock data
        match = next((m for m in mock_matches if m["id"] == match_id), None)
        
        if not match:
            return error_response(
                message=f"Match with ID {match_id} not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return success_response(
            data=match,
            message="Match details retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Error getting match {match_id}: {e}", exc_info=True)
        return error_response(
            message=f"Failed to get match: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.delete("/{match_id}")
async def unmatch(
    match_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Unmatch a specific match.
    
    Args:
        match_id: Match ID
        current_user: Current user
        
    Returns:
        Dict: Success message
    """
    try:
        # In a real implementation, this would use the bot to unmatch
        # bot = get_bot()
        # bot.navigator.unmatch(match_id)
        
        # For now, just return success
        return success_response(
            message=f"Successfully unmatched with ID {match_id}"
        )
    except Exception as e:
        logger.error(f"Error unmatching {match_id}: {e}", exc_info=True)
        return error_response(
            message=f"Failed to unmatch: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/{match_id}/conversation")
async def get_conversation(
    match_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get conversation with a specific match.
    
    Args:
        match_id: Match ID
        current_user: Current user
        
    Returns:
        Dict: Conversation messages
    """
    try:
        # In a real implementation, this would use the bot to get conversation
        # bot = get_bot()
        # conversation = bot.navigator.get_conversation(match_id)
        
        # For now, use mock data
        mock_conversation = [
            {"sender": "match", "message": "Hey there!", "timestamp": "2023-05-14T10:30:00Z"},
            {"sender": "user", "message": "Hi! How are you?", "timestamp": "2023-05-14T10:35:00Z"},
            {"sender": "match", "message": "I'm good, thanks! What do you do for fun?", "timestamp": "2023-05-14T10:40:00Z"}
        ]
        
        return success_response(
            data={"messages": mock_conversation},
            message="Conversation retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Error getting conversation for match {match_id}: {e}", exc_info=True)
        return error_response(
            message=f"Failed to get conversation: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.post("/{match_id}/message")
async def send_message(
    match_id: str,
    message: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Send a message to a specific match.
    
    Args:
        match_id: Match ID
        message: Message to send
        current_user: Current user
        
    Returns:
        Dict: Success message
    """
    try:
        # In a real implementation, this would use the bot to send a message
        # bot = get_bot()
        # bot.navigator.send_message(match_id, message)
        
        # For now, just return success
        return success_response(
            message=f"Message sent successfully to match {match_id}"
        )
    except Exception as e:
        logger.error(f"Error sending message to match {match_id}: {e}", exc_info=True)
        return error_response(
            message=f"Failed to send message: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )