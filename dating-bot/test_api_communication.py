"""
Test script for API communication between the Chrome extension and backend.

This script tests the API endpoints and simulates the communication flow
between the frontend and backend components.
"""

import json
import time
import logging
import requests
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API configuration
API_BASE_URL = "http://localhost:8000/api/v1"
USERNAME = "admin"
PASSWORD = "admin"

class APITester:
    """Test the API communication between frontend and backend."""
    
    def __init__(self, base_url):
        """Initialize the API tester."""
        self.base_url = base_url
        self.token = None
        self.headers = {}
    
    def authenticate(self, username, password):
        """Authenticate with the API."""
        logger.info(f"Authenticating as {username}")
        
        try:
            response = requests.post(
                f"{self.base_url}/auth/token",
                data={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                if "data" in data and "access_token" in data["data"]:
                    self.token = data["data"]["access_token"]
                    self.headers = {"Authorization": f"Bearer {self.token}"}
                    logger.info("Authentication successful")
                    return True
                else:
                    logger.error(f"Unexpected response format: {data}")
            else:
                logger.error(f"Authentication failed with status code {response.status_code}")
                logger.error(f"Response: {response.text}")
            
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Authentication request failed: {e}")
            return False
    
    def test_auth_endpoints(self):
        """Test the authentication endpoints."""
        logger.info("Testing authentication endpoints")
        
        results = []
        
        # Test /auth/me endpoint
        try:
            response = requests.get(
                f"{self.base_url}/auth/me",
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                results.append({
                    "endpoint": "/auth/me",
                    "status": "PASS",
                    "status_code": response.status_code,
                    "response": data
                })
                logger.info("Auth/me endpoint test passed")
            else:
                results.append({
                    "endpoint": "/auth/me",
                    "status": "FAIL",
                    "status_code": response.status_code,
                    "response": response.text
                })
                logger.error(f"Auth/me endpoint test failed with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            results.append({
                "endpoint": "/auth/me",
                "status": "ERROR",
                "error": str(e)
            })
            logger.error(f"Auth/me endpoint request failed: {e}")
        
        # Test without token (should fail)
        try:
            response = requests.get(
                f"{self.base_url}/auth/me"
            )
            
            if response.status_code == 401:
                results.append({
                    "endpoint": "/auth/me (no token)",
                    "status": "PASS",
                    "status_code": response.status_code,
                    "response": "Unauthorized (expected)"
                })
                logger.info("Auth/me endpoint without token correctly returned 401")
            else:
                results.append({
                    "endpoint": "/auth/me (no token)",
                    "status": "FAIL",
                    "status_code": response.status_code,
                    "response": response.text
                })
                logger.error(f"Auth/me endpoint without token returned {response.status_code} instead of 401")
        except requests.exceptions.RequestException as e:
            results.append({
                "endpoint": "/auth/me (no token)",
                "status": "ERROR",
                "error": str(e)
            })
            logger.error(f"Auth/me endpoint without token request failed: {e}")
        
        return results
    
    def test_swipe_endpoints(self):
        """Test the swiping control endpoints."""
        logger.info("Testing swipe endpoints")
        
        results = []
        
        # Test /swipe/status endpoint
        try:
            response = requests.get(
                f"{self.base_url}/swipe/status",
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                results.append({
                    "endpoint": "/swipe/status",
                    "status": "PASS",
                    "status_code": response.status_code,
                    "response": data
                })
                logger.info("Swipe/status endpoint test passed")
            else:
                results.append({
                    "endpoint": "/swipe/status",
                    "status": "FAIL",
                    "status_code": response.status_code,
                    "response": response.text
                })
                logger.error(f"Swipe/status endpoint test failed with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            results.append({
                "endpoint": "/swipe/status",
                "status": "ERROR",
                "error": str(e)
            })
            logger.error(f"Swipe/status endpoint request failed: {e}")
        
        # Test /swipe/start endpoint
        try:
            swipe_config = {
                "count": 10,
                "like_ratio": 0.7,
                "delay": 2
            }
            
            response = requests.post(
                f"{self.base_url}/swipe/start",
                headers=self.headers,
                json=swipe_config
            )
            
            if response.status_code == 200:
                data = response.json()
                results.append({
                    "endpoint": "/swipe/start",
                    "status": "PASS",
                    "status_code": response.status_code,
                    "response": data
                })
                logger.info("Swipe/start endpoint test passed")
            else:
                results.append({
                    "endpoint": "/swipe/start",
                    "status": "FAIL",
                    "status_code": response.status_code,
                    "response": response.text
                })
                logger.error(f"Swipe/start endpoint test failed with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            results.append({
                "endpoint": "/swipe/start",
                "status": "ERROR",
                "error": str(e)
            })
            logger.error(f"Swipe/start endpoint request failed: {e}")
        
        # Wait a moment for the bot to start
        time.sleep(2)
        
        # Test /swipe/status again to see if it's running
        try:
            response = requests.get(
                f"{self.base_url}/swipe/status",
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                is_running = data.get("data", {}).get("is_running", False)
                
                results.append({
                    "endpoint": "/swipe/status (after start)",
                    "status": "PASS" if is_running else "FAIL",
                    "status_code": response.status_code,
                    "response": data
                })
                
                if is_running:
                    logger.info("Bot is running as expected after start command")
                else:
                    logger.error("Bot is not running after start command")
            else:
                results.append({
                    "endpoint": "/swipe/status (after start)",
                    "status": "FAIL",
                    "status_code": response.status_code,
                    "response": response.text
                })
                logger.error(f"Swipe/status endpoint test failed with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            results.append({
                "endpoint": "/swipe/status (after start)",
                "status": "ERROR",
                "error": str(e)
            })
            logger.error(f"Swipe/status endpoint request failed: {e}")
        
        # Test /swipe/stop endpoint
        try:
            response = requests.post(
                f"{self.base_url}/swipe/stop",
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                results.append({
                    "endpoint": "/swipe/stop",
                    "status": "PASS",
                    "status_code": response.status_code,
                    "response": data
                })
                logger.info("Swipe/stop endpoint test passed")
            else:
                results.append({
                    "endpoint": "/swipe/stop",
                    "status": "FAIL",
                    "status_code": response.status_code,
                    "response": response.text
                })
                logger.error(f"Swipe/stop endpoint test failed with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            results.append({
                "endpoint": "/swipe/stop",
                "status": "ERROR",
                "error": str(e)
            })
            logger.error(f"Swipe/stop endpoint request failed: {e}")
        
        # Wait a moment for the bot to stop
        time.sleep(2)
        
        # Test /swipe/status again to see if it's stopped
        try:
            response = requests.get(
                f"{self.base_url}/swipe/status",
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                is_running = data.get("data", {}).get("is_running", True)
                
                results.append({
                    "endpoint": "/swipe/status (after stop)",
                    "status": "PASS" if not is_running else "FAIL",
                    "status_code": response.status_code,
                    "response": data
                })
                
                if not is_running:
                    logger.info("Bot is stopped as expected after stop command")
                else:
                    logger.error("Bot is still running after stop command")
            else:
                results.append({
                    "endpoint": "/swipe/status (after stop)",
                    "status": "FAIL",
                    "status_code": response.status_code,
                    "response": response.text
                })
                logger.error(f"Swipe/status endpoint test failed with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            results.append({
                "endpoint": "/swipe/status (after stop)",
                "status": "ERROR",
                "error": str(e)
            })
            logger.error(f"Swipe/status endpoint request failed: {e}")
        
        return results
    
    def simulate_frontend_flow(self):
        """Simulate the typical frontend communication flow."""
        logger.info("Simulating frontend communication flow")
        
        results = []
        
        # Step 1: Authentication
        auth_result = self.authenticate(USERNAME, PASSWORD)
        results.append({
            "step": "Authentication",
            "status": "PASS" if auth_result else "FAIL"
        })
        
        if not auth_result:
            logger.error("Authentication failed, aborting frontend flow simulation")
            return results
        
        # Step 2: Get user info
        try:
            response = requests.get(
                f"{self.base_url}/auth/me",
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                results.append({
                    "step": "Get user info",
                    "status": "PASS",
                    "response": data
                })
                logger.info("Get user info step passed")
            else:
                results.append({
                    "step": "Get user info",
                    "status": "FAIL",
                    "status_code": response.status_code,
                    "response": response.text
                })
                logger.error(f"Get user info step failed with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            results.append({
                "step": "Get user info",
                "status": "ERROR",
                "error": str(e)
            })
            logger.error(f"Get user info request failed: {e}")
        
        # Step 3: Check bot status
        try:
            response = requests.get(
                f"{self.base_url}/swipe/status",
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                results.append({
                    "step": "Check bot status",
                    "status": "PASS",
                    "response": data
                })
                logger.info("Check bot status step passed")
            else:
                results.append({
                    "step": "Check bot status",
                    "status": "FAIL",
                    "status_code": response.status_code,
                    "response": response.text
                })
                logger.error(f"Check bot status step failed with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            results.append({
                "step": "Check bot status",
                "status": "ERROR",
                "error": str(e)
            })
            logger.error(f"Check bot status request failed: {e}")
        
        # Step 4: Start bot
        try:
            swipe_config = {
                "count": 5,
                "like_ratio": 0.6,
                "delay": 3
            }
            
            response = requests.post(
                f"{self.base_url}/swipe/start",
                headers=self.headers,
                json=swipe_config
            )
            
            if response.status_code == 200:
                data = response.json()
                results.append({
                    "step": "Start bot",
                    "status": "PASS",
                    "response": data
                })
                logger.info("Start bot step passed")
            else:
                results.append({
                    "step": "Start bot",
                    "status": "FAIL",
                    "status_code": response.status_code,
                    "response": response.text
                })
                logger.error(f"Start bot step failed with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            results.append({
                "step": "Start bot",
                "status": "ERROR",
                "error": str(e)
            })
            logger.error(f"Start bot request failed: {e}")
        
        # Step 5: Check status again
        time.sleep(2)
        try:
            response = requests.get(
                f"{self.base_url}/swipe/status",
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                is_running = data.get("data", {}).get("is_running", False)
                
                results.append({
                    "step": "Check status after start",
                    "status": "PASS" if is_running else "FAIL",
                    "response": data
                })
                
                if is_running:
                    logger.info("Bot is running as expected after start command")
                else:
                    logger.error("Bot is not running after start command")
            else:
                results.append({
                    "step": "Check status after start",
                    "status": "FAIL",
                    "status_code": response.status_code,
                    "response": response.text
                })
                logger.error(f"Check status after start step failed with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            results.append({
                "step": "Check status after start",
                "status": "ERROR",
                "error": str(e)
            })
            logger.error(f"Check status after start request failed: {e}")
        
        # Step 6: Stop bot
        try:
            response = requests.post(
                f"{self.base_url}/swipe/stop",
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                results.append({
                    "step": "Stop bot",
                    "status": "PASS",
                    "response": data
                })
                logger.info("Stop bot step passed")
            else:
                results.append({
                    "step": "Stop bot",
                    "status": "FAIL",
                    "status_code": response.status_code,
                    "response": response.text
                })
                logger.error(f"Stop bot step failed with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            results.append({
                "step": "Stop bot",
                "status": "ERROR",
                "error": str(e)
            })
            logger.error(f"Stop bot request failed: {e}")
        
        # Step 7: Logout
        try:
            response = requests.post(
                f"{self.base_url}/auth/logout",
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                results.append({
                    "step": "Logout",
                    "status": "PASS",
                    "response": data
                })
                logger.info("Logout step passed")
            else:
                results.append({
                    "step": "Logout",
                    "status": "FAIL",
                    "status_code": response.status_code,
                    "response": response.text
                })
                logger.error(f"Logout step failed with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            results.append({
                "step": "Logout",
                "status": "ERROR",
                "error": str(e)
            })
            logger.error(f"Logout request failed: {e}")
        
        return results

def run_api_tests():
    """Run the API communication tests."""
    logger.info("Starting API communication tests")
    
    tester = APITester(API_BASE_URL)
    
    # Authenticate
    if not tester.authenticate(USERNAME, PASSWORD):
        logger.error("Authentication failed, cannot proceed with tests")
        return
    
    # Run tests
    auth_results = tester.test_auth_endpoints()
    swipe_results = tester.test_swipe_endpoints()
    flow_results = tester.simulate_frontend_flow()
    
    # Print results
    print("\n" + "="*50)
    print("API COMMUNICATION TEST RESULTS")
    print("="*50)
    
    print("\nAuthentication Endpoints:")
    for result in auth_results:
        status_symbol = "✅" if result.get("status") == "PASS" else "❌"
        print(f"{status_symbol} {result.get('endpoint')}: {result.get('status')}")
    
    print("\nSwipe Endpoints:")
    for result in swipe_results:
        status_symbol = "✅" if result.get("status") == "PASS" else "❌"
        print(f"{status_symbol} {result.get('endpoint')}: {result.get('status')}")
    
    print("\nFrontend Flow Simulation:")
    for result in flow_results:
        status_symbol = "✅" if result.get("status") == "PASS" else "❌"
        print(f"{status_symbol} {result.get('step')}: {result.get('status')}")
    
    # Calculate overall success
    all_results = auth_results + swipe_results + flow_results
    pass_count = sum(1 for r in all_results if r.get("status") == "PASS")
    total_count = len(all_results)
    success_rate = (pass_count / total_count) * 100 if total_count > 0 else 0
    
    print("\n" + "="*50)
    print(f"Overall Success Rate: {success_rate:.1f}% ({pass_count}/{total_count} tests passed)")
    print("="*50)
    
    if success_rate == 100:
        print("\n✅ All API communication tests passed! The frontend and backend are communicating correctly.")
    else:
        print("\n⚠️ Some API communication tests failed. Check the logs for details.")

if __name__ == "__main__":
    run_api_tests()