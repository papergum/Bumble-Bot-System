"""
Login functionality for Bumble automation.
This module handles different login methods for Bumble.
"""

import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BumbleLogin:
    """
    Handles login functionality for Bumble.
    """
    
    # Bumble web URL
    BUMBLE_URL = "https://bumble.com/app"
    
    # Selectors for login elements
    # Note: These selectors are based on research and may need adjustment
    # after direct inspection of Bumble's web interface
    SELECTORS = {
        'sign_in_button': "//span[contains(text(), 'Sign In')]",
        'facebook_button': "//span[contains(text(), 'Continue with Facebook')]",
        'phone_button': "//span[contains(text(), 'Use Cell Phone Number')]",
        'phone_input': "//input[@type='tel']",
        'continue_button': "//span[contains(text(), 'Continue')]",
        'fb_email': "//input[@id='email']",
        'fb_password': "//input[@id='pass']",
        'fb_login_button': "//button[@name='login']",
        'verification_code_input': "//input[@type='number']"
    }
    
    def __init__(self, driver):
        """
        Initialize the login handler.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        
    def login_with_facebook(self, email, password):
        """
        Login to Bumble using Facebook credentials.
        
        Args:
            email (str): Facebook email
            password (str): Facebook password
        """
        logger.info("Attempting to login with Facebook")
        
        try:
            # Navigate to Bumble
            self.driver.get(self.BUMBLE_URL)
            
            # Wait for and click sign in button
            self._click_element(self.SELECTORS['sign_in_button'])
            
            # Click on Facebook login option
            self._click_element(self.SELECTORS['facebook_button'])
            
            # Switch to Facebook login popup
            self._switch_to_popup()
            
            # Enter Facebook credentials
            self._enter_text(self.SELECTORS['fb_email'], email)
            self._enter_text(self.SELECTORS['fb_password'], password)
            
            # Click login button
            self._click_element(self.SELECTORS['fb_login_button'])
            
            # Switch back to main window
            self.driver.switch_to.window(self.driver.window_handles[0])
            
            # Wait for login to complete
            self._wait_for_login_completion()
            
            logger.info("Facebook login successful")
            
        except Exception as e:
            logger.error(f"Facebook login failed: {str(e)}")
            raise
            
    def login_with_phone(self, phone_number):
        """
        Login to Bumble using phone number.
        
        Args:
            phone_number (str): Phone number to use for login
        """
        logger.info("Attempting to login with phone number")
        
        try:
            # Navigate to Bumble
            self.driver.get(self.BUMBLE_URL)
            
            # Wait for and click sign in button
            self._click_element(self.SELECTORS['sign_in_button'])
            
            # Click on phone login option
            self._click_element(self.SELECTORS['phone_button'])
            
            # Enter phone number
            self._enter_text(self.SELECTORS['phone_input'], phone_number)
            
            # Click continue button
            self._click_element(self.SELECTORS['continue_button'])
            
            # Wait for verification code input to appear
            self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, self.SELECTORS['verification_code_input'])
            ))
            
            logger.info("Phone verification code required to complete login")
            
            # Note: At this point, manual intervention is required to enter the verification code
            # This could be enhanced with an API integration for SMS verification services
            
        except Exception as e:
            logger.error(f"Phone login failed: {str(e)}")
            raise
            
    def _click_element(self, xpath):
        """
        Wait for an element to be clickable and then click it.
        
        Args:
            xpath (str): XPath selector for the element
        """
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        
    def _enter_text(self, xpath, text):
        """
        Enter text into an input field.
        
        Args:
            xpath (str): XPath selector for the input field
            text (str): Text to enter
        """
        element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        element.clear()
        element.send_keys(text)
        
    def _switch_to_popup(self):
        """
        Switch to the popup window (used for Facebook login).
        """
        # Wait for popup window to appear
        time.sleep(2)
        
        # Switch to the new window
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[1])
        else:
            logger.warning("No popup window detected")
            
    def _wait_for_login_completion(self):
        """
        Wait for login process to complete.
        """
        # Wait for redirect to main app page
        # This is a simple implementation and may need refinement
        time.sleep(5)
        
        # Check if we're logged in by looking for common elements
        try:
            # Wait for an element that indicates successful login
            # This selector needs to be updated based on actual Bumble web interface
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'profile-card')]")
            ))
            return True
        except TimeoutException:
            logger.warning("Login may not have completed successfully")
            return False