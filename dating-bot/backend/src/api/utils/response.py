"""
Response formatting utilities for the API.
This module provides functions for formatting API responses.
"""

from typing import Any, Dict, List, Optional, Union
from fastapi.responses import JSONResponse
from fastapi import status

def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = status.HTTP_200_OK
) -> JSONResponse:
    """
    Create a success response.
    
    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code
        
    Returns:
        JSONResponse: Formatted success response
    """
    content = {
        "status": "success",
        "message": message
    }
    
    if data is not None:
        content["data"] = data
        
    return JSONResponse(
        content=content,
        status_code=status_code
    )

def error_response(
    message: str = "An error occurred",
    status_code: int = status.HTTP_400_BAD_REQUEST,
    errors: Optional[List[Dict[str, Any]]] = None
) -> JSONResponse:
    """
    Create an error response.
    
    Args:
        message: Error message
        status_code: HTTP status code
        errors: List of specific errors
        
    Returns:
        JSONResponse: Formatted error response
    """
    content = {
        "status": "error",
        "message": message
    }
    
    if errors:
        content["errors"] = errors
        
    return JSONResponse(
        content=content,
        status_code=status_code
    )

def pagination_response(
    data: List[Any],
    total: int,
    page: int,
    page_size: int,
    message: str = "Success"
) -> JSONResponse:
    """
    Create a paginated response.
    
    Args:
        data: Page data
        total: Total number of items
        page: Current page number
        page_size: Number of items per page
        message: Success message
        
    Returns:
        JSONResponse: Formatted paginated response
    """
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    
    content = {
        "status": "success",
        "message": message,
        "data": data,
        "pagination": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }
    }
    
    return JSONResponse(
        content=content,
        status_code=status.HTTP_200_OK
    )