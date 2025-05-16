"""
Main bot class for Bumble automation.
This module provides the core functionality for automating interactions with Bumble.
"""

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from .login import BumbleLogin
from .navigator import BumbleNavigator
from .swiper import BumbleSwiper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BumbleBot:
    """
    Main class for Bumble automation.
    Handles initialization of the browser and provides access to different functionalities.
    """
    
    def __init__(self, headless=False, profile_path=None):
        """
        Initialize the BumbleBot.
        
        Args:
            headless (bool): Whether to run the browser in headless mode
            profile_path (str): Path to Chrome profile to use (for maintaining login sessions)
        """
        logger.info("Initializing BumbleBot")
        self.driver = self._setup_driver(headless, profile_path)
        self.login = BumbleLogin(self.driver)
        self.navigator = BumbleNavigator(self.driver)
        self.swiper = BumbleSwiper(self.driver)
        
    def _setup_driver(self, headless, profile_path):
        """
        Set up and configure the Chrome WebDriver.
        
        Args:
            headless (bool): Whether to run in headless mode
            profile_path (str): Path to Chrome profile
            
        Returns:
            WebDriver: Configured Chrome WebDriver instance
        """
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument("--headless")
        
        # Add common options to make automation more stable
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Add user agent to avoid detection
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        
        # Use profile if provided
        if profile_path and os.path.exists(profile_path):
            chrome_options.add_argument(f"--user-data-dir={profile_path}")
        
        # Initialize Chrome WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set implicit wait time
        driver.implicitly_wait(10)
        
        return driver
    
    def start(self):
        """
        Start the bot by navigating to Bumble website.
        """
        logger.info("Starting BumbleBot")
        self.navigator.go_to_bumble()
        
    def login_with_facebook(self, email, password):
        """
        Login to Bumble using Facebook credentials.
        
        Args:
            email (str): Facebook email
            password (str): Facebook password
        """
        self.login.login_with_facebook(email, password)
        
    def login_with_phone(self, phone_number):
        """
        Login to Bumble using phone number.
        
        Args:
            phone_number (str): Phone number to use for login
        """
        self.login.login_with_phone(phone_number)
        
    def auto_swipe(self, count=10, like_ratio=0.7, delay=2):
        """
        Automatically swipe on profiles.
        
        Args:
            count (int): Number of profiles to swipe on
            like_ratio (float): Ratio of right swipes (likes) to total swipes
            delay (int): Delay between swipes in seconds
        """
        logger.info(f"Starting auto-swipe session. Count: {count}, Like ratio: {like_ratio}")
        self.swiper.auto_swipe(count, like_ratio, delay)
        
    def get_messages(self):
        """
        Get all messages from matches.
        
        Returns:
            dict: Dictionary of conversations with messages
        """
        return self.navigator.get_messages()
        
    def send_message(self, match_name, message):
        """
        Send a message to a specific match.
        
        Args:
            match_name (str): Name of the match to message
            message (str): Message to send
        """
        self.navigator.send_message(match_name, message)
        
    def close(self):
        """
        Close the browser and end the session.
        """
        logger.info("Closing BumbleBot")
        if self.driver:
            self.driver.quit()
            
    def __enter__(self):
        """
        Support for context manager protocol.
        """
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ensure driver is closed when exiting context.
        """
        self.close()