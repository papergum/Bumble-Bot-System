"""
Test script for the Bumble Bot API.
This script tests the basic functionality of the API endpoints.
"""

import json
import requests
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load API configuration
config_path = Path(__file__).parent.parent.parent / "config" / "api_config.json"
try:
    with open(config_path, "r") as f:
        config = json.load(f)
        api_config = config.get("api", {})
except (FileNotFoundError, json.JSONDecodeError) as e:
    logger.error(f"Failed to load API configuration: {e}")
    api_config = {
        "host": "0.0.0.0",
        "port": 8000,
        "api_prefix": "/api/v1"
    }

# API base URL
API_BASE_URL = f"http://{api_config.get('host', '0.0.0.0')}:{api_config.get('port', 8000)}{api_config.get('api_prefix', '/api/v1')}"

def test_auth_endpoints():
    """
    Test authentication endpoints.
    """
    logger.info("Testing authentication endpoints...")
    
    # Test login
    login_url = f"{API_BASE_URL}/auth/token"
    login_data = {
        "username": "admin",
        "password": "admin"
    }
    
    try:
        response = requests.post(login_url, data=login_data)
        response.raise_for_status()
        token_data = response.json()
        
        if token_data.get("status") == "success" and "access_token" in token_data.get("data", {}):
            logger.info("Login successful")
            access_token = token_data["data"]["access_token"]
            
            # Test get current user
            me_url = f"{API_BASE_URL}/auth/me"
            headers = {"Authorization": f"Bearer {access_token}"}
            
            response = requests.get(me_url, headers=headers)
            response.raise_for_status()
            user_data = response.json()
            
            if user_data.get("status") == "success" and "username" in user_data.get("data", {}):
                logger.info("Get current user successful")
                return access_token
            else:
                logger.error("Get current user failed")
                return None
        else:
            logger.error("Login failed")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error testing auth endpoints: {e}")
        return None

def test_swipe_endpoints(access_token):
    """
    Test swiping endpoints.
    
    Args:
        access_token: Access token for authentication
    """
    logger.info("Testing swiping endpoints...")
    
    if not access_token:
        logger.error("No access token provided")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Test get swipe status
    status_url = f"{API_BASE_URL}/swipe/status"
    
    try:
        response = requests.get(status_url, headers=headers)
        response.raise_for_status()
        status_data = response.json()
        
        if status_data.get("status") == "success":
            logger.info("Get swipe status successful")
        else:
            logger.error("Get swipe status failed")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error testing swipe status endpoint: {e}")

def test_matches_endpoints(access_token):
    """
    Test matches endpoints.
    
    Args:
        access_token: Access token for authentication
    """
    logger.info("Testing matches endpoints...")
    
    if not access_token:
        logger.error("No access token provided")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Test get matches
    matches_url = f"{API_BASE_URL}/matches"
    
    try:
        response = requests.get(matches_url, headers=headers)
        response.raise_for_status()
        matches_data = response.json()
        
        if matches_data.get("status") == "success":
            logger.info("Get matches successful")
        else:
            logger.error("Get matches failed")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error testing matches endpoint: {e}")

def test_messages_endpoints(access_token):
    """
    Test messages endpoints.
    
    Args:
        access_token: Access token for authentication
    """
    logger.info("Testing messages endpoints...")
    
    if not access_token:
        logger.error("No access token provided")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Test get filter config
    config_url = f"{API_BASE_URL}/messages/filter/config"
    
    try:
        response = requests.get(config_url, headers=headers)
        response.raise_for_status()
        config_data = response.json()
        
        if config_data.get("status") == "success":
            logger.info("Get filter config successful")
        else:
            logger.error("Get filter config failed")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error testing filter config endpoint: {e}")

def run_tests():
    """
    Run all API tests.
    """
    logger.info(f"Testing API at {API_BASE_URL}")
    
    # Test authentication endpoints
    access_token = test_auth_endpoints()
    
    if access_token:
        # Test other endpoints
        test_swipe_endpoints(access_token)
        test_matches_endpoints(access_token)
        test_messages_endpoints(access_token)
        
        logger.info("All tests completed")
    else:
        logger.error("Authentication failed, skipping other tests")

if __name__ == "__main__":
    run_tests()