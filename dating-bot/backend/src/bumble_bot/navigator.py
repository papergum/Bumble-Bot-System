"""
Page navigation functionality for Bumble automation.
This module handles navigation through different sections of Bumble.
"""

import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BumbleNavigator:
    """
    Handles navigation through Bumble's web interface.
    """
    
    # Bumble web URL
    BUMBLE_URL = "https://bumble.com/app"
    
    # Selectors for navigation elements
    # Note: These selectors are based on research and may need adjustment
    # after direct inspection of Bumble's web interface
    SELECTORS = {
        'match_tab': "//span[contains(text(), 'Matches')]",
        'message_tab': "//span[contains(text(), 'Messages')]",
        'profile_tab': "//span[contains(text(), 'Profile')]",
        'settings_button': "//span[contains(text(), 'Settings')]",
        'match_card': "//div[contains(@class, 'match-card')]",
        'conversation_list': "//div[contains(@class, 'conversation-list')]",
        'conversation_item': "//div[contains(@class, 'conversation-item')]",
        'message_input': "//textarea[contains(@placeholder, 'Message')]",
        'send_button': "//button[contains(@aria-label, 'Send')]",
        'message_container': "//div[contains(@class, 'message-container')]",
        'message_text': "//div[contains(@class, 'message-text')]"
    }
    
    def __init__(self, driver):
        """
        Initialize the navigator.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        
    def go_to_bumble(self):
        """
        Navigate to Bumble website.
        """
        logger.info("Navigating to Bumble")
        self.driver.get(self.BUMBLE_URL)
        
    def go_to_matches(self):
        """
        Navigate to the matches tab.
        """
        logger.info("Navigating to matches tab")
        self._click_element(self.SELECTORS['match_tab'])
        
    def go_to_messages(self):
        """
        Navigate to the messages tab.
        """
        logger.info("Navigating to messages tab")
        self._click_element(self.SELECTORS['message_tab'])
        
    def go_to_profile(self):
        """
        Navigate to the profile tab.
        """
        logger.info("Navigating to profile tab")
        self._click_element(self.SELECTORS['profile_tab'])
        
    def go_to_settings(self):
        """
        Navigate to settings.
        """
        logger.info("Navigating to settings")
        self._click_element(self.SELECTORS['settings_button'])
        
    def get_matches(self):
        """
        Get all available matches.
        
        Returns:
            list: List of match elements
        """
        logger.info("Getting matches")
        self.go_to_matches()
        
        try:
            # Wait for match cards to load
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, self.SELECTORS['match_card'])
            ))
            
            # Get all match cards
            match_cards = self.driver.find_elements(By.XPATH, self.SELECTORS['match_card'])
            logger.info(f"Found {len(match_cards)} matches")
            
            return match_cards
            
        except TimeoutException:
            logger.warning("No matches found or matches failed to load")
            return []
            
    def get_conversations(self):
        """
        Get all available conversations.
        
        Returns:
            list: List of conversation elements
        """
        logger.info("Getting conversations")
        self.go_to_messages()
        
        try:
            # Wait for conversation list to load
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, self.SELECTORS['conversation_list'])
            ))
            
            # Get all conversation items
            conversation_items = self.driver.find_elements(By.XPATH, self.SELECTORS['conversation_item'])
            logger.info(f"Found {len(conversation_items)} conversations")
            
            return conversation_items
            
        except TimeoutException:
            logger.warning("No conversations found or conversations failed to load")
            return []
            
    def open_conversation(self, match_name):
        """
        Open a conversation with a specific match.
        
        Args:
            match_name (str): Name of the match
            
        Returns:
            bool: True if conversation was opened successfully, False otherwise
        """
        logger.info(f"Opening conversation with {match_name}")
        self.go_to_messages()
        
        try:
            # Find conversation by match name
            conversation_xpath = f"//div[contains(@class, 'conversation-item') and contains(., '{match_name}')]"
            conversation = self.wait.until(EC.element_to_be_clickable((By.XPATH, conversation_xpath)))
            conversation.click()
            
            # Wait for conversation to load
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, self.SELECTORS['message_input'])
            ))
            
            logger.info(f"Conversation with {match_name} opened successfully")
            return True
            
        except (TimeoutException, NoSuchElementException):
            logger.warning(f"Failed to open conversation with {match_name}")
            return False
            
    def send_message(self, match_name, message):
        """
        Send a message to a specific match.
        
        Args:
            match_name (str): Name of the match
            message (str): Message to send
            
        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        logger.info(f"Sending message to {match_name}: {message}")
        
        # Open conversation with match
        if not self.open_conversation(match_name):
            return False
            
        try:
            # Enter message
            message_input = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, self.SELECTORS['message_input'])
            ))
            message_input.clear()
            message_input.send_keys(message)
            
            # Click send button
            send_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, self.SELECTORS['send_button'])
            ))
            send_button.click()
            
            logger.info(f"Message sent to {match_name}")
            return True
            
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            logger.error(f"Failed to send message to {match_name}: {str(e)}")
            return False
            
    def get_messages(self, match_name=None):
        """
        Get messages from a specific match or all matches.
        
        Args:
            match_name (str, optional): Name of the match. If None, get messages from all matches.
            
        Returns:
            dict: Dictionary of conversations with messages
        """
        if match_name:
            logger.info(f"Getting messages from {match_name}")
            return self._get_messages_from_match(match_name)
        else:
            logger.info("Getting messages from all matches")
            return self._get_all_messages()
            
    def _get_messages_from_match(self, match_name):
        """
        Get messages from a specific match.
        
        Args:
            match_name (str): Name of the match
            
        Returns:
            dict: Dictionary with match name as key and list of messages as value
        """
        # Open conversation with match
        if not self.open_conversation(match_name):
            return {match_name: []}
            
        try:
            # Wait for messages to load
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, self.SELECTORS['message_container'])
            ))
            
            # Get all message elements
            message_elements = self.driver.find_elements(By.XPATH, self.SELECTORS['message_text'])
            
            # Extract message text
            messages = [element.text for element in message_elements]
            
            logger.info(f"Found {len(messages)} messages from {match_name}")
            
            return {match_name: messages}
            
        except TimeoutException:
            logger.warning(f"No messages found from {match_name} or messages failed to load")
            return {match_name: []}
            
    def _get_all_messages(self):
        """
        Get messages from all matches.
        
        Returns:
            dict: Dictionary with match names as keys and lists of messages as values
        """
        all_messages = {}
        
        # Get all conversations
        conversations = self.get_conversations()
        
        for conversation in conversations:
            try:
                # Extract match name
                match_name = conversation.text.split('\n')[0]
                
                # Get messages from this match
                match_messages = self._get_messages_from_match(match_name)
                
                # Add to all messages
                all_messages.update(match_messages)
                
            except Exception as e:
                logger.error(f"Error getting messages from conversation: {str(e)}")
                
        return all_messages
        
    def _click_element(self, xpath):
        """
        Wait for an element to be clickable and then click it.
        
        Args:
            xpath (str): XPath selector for the element
        """
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()