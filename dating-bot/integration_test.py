"""
Integration Test Script for Bumble Bot System

This script tests the integration between the Python backend and Chrome extension frontend
to ensure all components work together properly.
"""

import os
import sys
import json
import time
import logging
import requests
import unittest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BumbleBotIntegrationTest(unittest.TestCase):
    """Integration tests for the Bumble Bot system."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the test environment."""
        logger.info("Setting up integration test environment")
        
        # Start the API server in a separate process
        cls.start_api_server()
        
        # Wait for API server to start
        time.sleep(3)
        
        # Set up Chrome with the extension loaded
        cls.setup_chrome_with_extension()
        
    @classmethod
    def tearDownClass(cls):
        """Clean up the test environment."""
        logger.info("Tearing down integration test environment")
        
        # Close the browser
        if hasattr(cls, 'driver') and cls.driver:
            cls.driver.quit()
        
        # Stop the API server
        cls.stop_api_server()
    
    @classmethod
    def start_api_server(cls):
        """Start the API server."""
        logger.info("Starting API server")
        
        # Use subprocess to start the API server
        import subprocess
        
        # Get the path to run_api.py
        api_script_path = Path("backend/run_api.py").absolute()
        
        if not api_script_path.exists():
            logger.error(f"API script not found at {api_script_path}")
            sys.exit(1)
        
        # Start the server in a new process
        cls.api_process = subprocess.Popen(
            [sys.executable, str(api_script_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        logger.info(f"API server started with PID {cls.api_process.pid}")
    
    @classmethod
    def stop_api_server(cls):
        """Stop the API server."""
        if hasattr(cls, 'api_process') and cls.api_process:
            logger.info("Stopping API server")
            cls.api_process.terminate()
            cls.api_process.wait()
            logger.info("API server stopped")
    
    @classmethod
    def setup_chrome_with_extension(cls):
        """Set up Chrome with the extension loaded."""
        logger.info("Setting up Chrome with extension")
        
        # Get the path to the extension
        extension_path = Path("chrome_extension").absolute()
        
        if not extension_path.exists():
            logger.error(f"Extension not found at {extension_path}")
            sys.exit(1)
        
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument(f"--load-extension={extension_path}")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Initialize Chrome WebDriver
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set implicit wait time
        cls.driver.implicitly_wait(10)
        
        # Get the extension ID
        cls.driver.get("chrome://extensions")
        time.sleep(2)
        
        # Enable developer mode
        cls.driver.execute_script("document.querySelector('extensions-manager').shadowRoot.querySelector('#devMode').click()")
        time.sleep(1)
        
        # Get extension ID
        extension_info = cls.driver.execute_script("""
            return document.querySelector('extensions-manager').shadowRoot
                .querySelector('extensions-item-list').shadowRoot
                .querySelector('extensions-item').shadowRoot
                .querySelector('#id').textContent;
        """)
        
        cls.extension_id = extension_info.strip()
        logger.info(f"Extension ID: {cls.extension_id}")
    
    def test_01_api_server_running(self):
        """Test that the API server is running."""
        logger.info("Testing API server is running")
        
        try:
            response = requests.get("http://localhost:8000/")
            self.assertEqual(response.status_code, 200)
            logger.info("API server is running")
        except requests.exceptions.ConnectionError:
            self.fail("API server is not running")
    
    def test_02_extension_popup_loads(self):
        """Test that the extension popup loads."""
        logger.info("Testing extension popup loads")
        
        # Open the extension popup
        self.driver.get(f"chrome-extension://{self.extension_id}/html/popup.html")
        
        # Check that the popup loaded
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            heading = self.driver.find_element(By.TAG_NAME, "h1").text
            self.assertEqual(heading, "Bumble Bot")
            logger.info("Extension popup loaded successfully")
        except (TimeoutException, WebDriverException) as e:
            self.fail(f"Extension popup failed to load: {e}")
    
    def test_03_extension_login(self):
        """Test the extension login functionality."""
        logger.info("Testing extension login")
        
        # Open the extension popup
        self.driver.get(f"chrome-extension://{self.extension_id}/html/popup.html")
        
        # Wait for the login form to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "login-form"))
            )
            
            # Fill in the login form
            self.driver.find_element(By.ID, "api-url").send_keys("http://localhost:8000/api/v1")
            self.driver.find_element(By.ID, "username").send_keys("admin")
            self.driver.find_element(By.ID, "password").send_keys("admin")
            
            # Submit the form
            self.driver.find_element(By.ID, "login-form").submit()
            
            # Wait for login to complete
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "controls-section"))
            )
            
            # Check that we're logged in
            status_text = self.driver.find_element(By.CLASS_NAME, "status-text").text
            self.assertEqual(status_text, "Connected")
            logger.info("Extension login successful")
        except (TimeoutException, WebDriverException) as e:
            self.fail(f"Extension login failed: {e}")
    
    def test_04_bot_controls(self):
        """Test the bot control functionality."""
        logger.info("Testing bot controls")
        
        # Open the extension popup
        self.driver.get(f"chrome-extension://{self.extension_id}/html/popup.html")
        
        # Wait for the controls section to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "controls-section"))
            )
            
            # Check initial bot status
            bot_status = self.driver.find_element(By.ID, "bot-status").text
            self.assertEqual(bot_status, "Inactive")
            
            # Click the start button
            start_button = self.driver.find_element(By.ID, "start-button")
            start_button.click()
            
            # Wait for status to update
            time.sleep(2)
            
            # Check that the bot status changed
            bot_status = self.driver.find_element(By.ID, "bot-status").text
            self.assertEqual(bot_status, "Active")
            
            # Click the stop button
            stop_button = self.driver.find_element(By.ID, "stop-button")
            stop_button.click()
            
            # Wait for status to update
            time.sleep(2)
            
            # Check that the bot status changed back
            bot_status = self.driver.find_element(By.ID, "bot-status").text
            self.assertEqual(bot_status, "Inactive")
            
            logger.info("Bot controls working correctly")
        except (TimeoutException, WebDriverException) as e:
            self.fail(f"Bot control test failed: {e}")
    
    def test_05_options_page(self):
        """Test the options page functionality."""
        logger.info("Testing options page")
        
        # Open the options page
        self.driver.get(f"chrome-extension://{self.extension_id}/html/options.html")
        
        # Wait for the options page to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            
            # Check that the options page loaded
            heading = self.driver.find_element(By.TAG_NAME, "h1").text
            self.assertTrue("Settings" in heading)
            logger.info("Options page loaded successfully")
        except (TimeoutException, WebDriverException) as e:
            self.fail(f"Options page failed to load: {e}")
    
    def test_06_api_endpoints(self):
        """Test the API endpoints directly."""
        logger.info("Testing API endpoints")
        
        # Get a token
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/auth/token",
                data={"username": "admin", "password": "admin"}
            )
            self.assertEqual(response.status_code, 200)
            token = response.json()["data"]["access_token"]
            
            # Test authenticated endpoint
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                "http://localhost:8000/api/v1/auth/me",
                headers=headers
            )
            self.assertEqual(response.status_code, 200)
            
            # Test swipe status endpoint
            response = requests.get(
                "http://localhost:8000/api/v1/swipe/status",
                headers=headers
            )
            self.assertEqual(response.status_code, 200)
            
            logger.info("API endpoints working correctly")
        except requests.exceptions.RequestException as e:
            self.fail(f"API endpoint test failed: {e}")

def run_tests():
    """Run the integration tests."""
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

if __name__ == "__main__":
    run_tests()