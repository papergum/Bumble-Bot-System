"""
Swiping functionality for Bumble automation.
This module handles swiping on profiles in Bumble.
"""

import time
import random
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BumbleSwiper:
    """
    Handles swiping functionality for Bumble.
    """
    
    # Selectors for swiping elements
    # Note: These selectors are based on research and may need adjustment
    # after direct inspection of Bumble's web interface
    SELECTORS = {
        'profile_card': "//div[contains(@class, 'profile-card')]",
        'like_button': "//span[contains(@data-qa-icon-name, 'floating-action-yes')]",
        'dislike_button': "//span[contains(@data-qa-icon-name, 'floating-action-no')]",
        'superswipe_button': "//span[contains(@data-qa-icon-name, 'floating-action-superswipe')]",
        'match_popup': "//div[contains(@class, 'match-popup')]",
        'close_match_popup': "//button[contains(@aria-label, 'Close')]",
        'profile_name': "//h1[contains(@class, 'profile-name')]",
        'profile_bio': "//div[contains(@class, 'profile-bio')]",
        'profile_info': "//div[contains(@class, 'profile-info')]",
        'out_of_likes': "//div[contains(text(), 'out of likes')]"
    }
    
    # Keyboard shortcuts for swiping
    KEYBOARD_SHORTCUTS = {
        'like': Keys.ARROW_RIGHT,
        'dislike': Keys.ARROW_LEFT,
        'superswipe': Keys.ARROW_UP,
        'open_profile': Keys.SPACE
    }
    
    def __init__(self, driver):
        """
        Initialize the swiper.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.action = ActionChains(driver)
        
    def swipe_right(self):
        """
        Swipe right (like) on the current profile.
        
        Returns:
            bool: True if swipe was successful, False otherwise
        """
        logger.info("Swiping right (like)")
        
        try:
            # Try using the like button
            try:
                like_button = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, self.SELECTORS['like_button'])
                ))
                like_button.click()
            except (TimeoutException, NoSuchElementException, ElementNotInteractableException):
                # Fall back to keyboard shortcut
                logger.info("Using keyboard shortcut for right swipe")
                self.action.send_keys(self.KEYBOARD_SHORTCUTS['like']).perform()
                
            # Check for match popup
            self._handle_match_popup()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to swipe right: {str(e)}")
            return False
            
    def swipe_left(self):
        """
        Swipe left (dislike) on the current profile.
        
        Returns:
            bool: True if swipe was successful, False otherwise
        """
        logger.info("Swiping left (dislike)")
        
        try:
            # Try using the dislike button
            try:
                dislike_button = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, self.SELECTORS['dislike_button'])
                ))
                dislike_button.click()
            except (TimeoutException, NoSuchElementException, ElementNotInteractableException):
                # Fall back to keyboard shortcut
                logger.info("Using keyboard shortcut for left swipe")
                self.action.send_keys(self.KEYBOARD_SHORTCUTS['dislike']).perform()
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to swipe left: {str(e)}")
            return False
            
    def super_swipe(self):
        """
        Super swipe on the current profile.
        
        Returns:
            bool: True if super swipe was successful, False otherwise
        """
        logger.info("Super swiping")
        
        try:
            # Try using the superswipe button
            try:
                superswipe_button = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, self.SELECTORS['superswipe_button'])
                ))
                superswipe_button.click()
            except (TimeoutException, NoSuchElementException, ElementNotInteractableException):
                # Fall back to keyboard shortcut
                logger.info("Using keyboard shortcut for super swipe")
                self.action.send_keys(self.KEYBOARD_SHORTCUTS['superswipe']).perform()
                
            # Check for match popup
            self._handle_match_popup()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to super swipe: {str(e)}")
            return False
            
    def get_profile_info(self):
        """
        Get information about the current profile.
        
        Returns:
            dict: Dictionary containing profile information
        """
        logger.info("Getting profile information")
        
        profile_info = {
            'name': '',
            'bio': '',
            'details': []
        }
        
        try:
            # Get profile name
            try:
                name_element = self.driver.find_element(By.XPATH, self.SELECTORS['profile_name'])
                profile_info['name'] = name_element.text
            except NoSuchElementException:
                logger.warning("Could not find profile name")
                
            # Get profile bio
            try:
                bio_element = self.driver.find_element(By.XPATH, self.SELECTORS['profile_bio'])
                profile_info['bio'] = bio_element.text
            except NoSuchElementException:
                logger.warning("Could not find profile bio")
                
            # Get profile details
            try:
                info_elements = self.driver.find_elements(By.XPATH, self.SELECTORS['profile_info'])
                profile_info['details'] = [element.text for element in info_elements]
            except NoSuchElementException:
                logger.warning("Could not find profile details")
                
            return profile_info
            
        except Exception as e:
            logger.error(f"Failed to get profile information: {str(e)}")
            return profile_info
            
    def auto_swipe(self, count=10, like_ratio=0.7, delay=2):
        """
        Automatically swipe on profiles.
        
        Args:
            count (int): Number of profiles to swipe on
            like_ratio (float): Ratio of right swipes (likes) to total swipes
            delay (int): Delay between swipes in seconds
            
        Returns:
            int: Number of profiles swiped on
        """
        logger.info(f"Starting auto-swipe. Count: {count}, Like ratio: {like_ratio}")
        
        swipes_completed = 0
        
        for i in range(count):
            try:
                # Check if we've run out of likes
                if self._check_out_of_likes():
                    logger.warning("Out of likes. Stopping auto-swipe.")
                    break
                    
                # Wait for profile card to load
                try:
                    self.wait.until(EC.presence_of_element_located(
                        (By.XPATH, self.SELECTORS['profile_card'])
                    ))
                except TimeoutException:
                    logger.warning("No profile card found. Stopping auto-swipe.")
                    break
                    
                # Get profile information
                profile_info = self.get_profile_info()
                logger.info(f"Profile: {profile_info['name']}")
                
                # Decide whether to swipe right or left
                if random.random() < like_ratio:
                    success = self.swipe_right()
                else:
                    success = self.swipe_left()
                    
                if success:
                    swipes_completed += 1
                    
                # Add delay between swipes
                time.sleep(delay + random.uniform(0, 1))
                
            except Exception as e:
                logger.error(f"Error during auto-swipe: {str(e)}")
                
        logger.info(f"Auto-swipe completed. Swiped on {swipes_completed} profiles.")
        return swipes_completed
        
    def _handle_match_popup(self):
        """
        Handle match popup if it appears.
        """
        try:
            # Check if match popup appears
            match_popup = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, self.SELECTORS['match_popup'])
            ))
            
            logger.info("Match popup detected")
            
            # Close match popup
            close_button = self.driver.find_element(By.XPATH, self.SELECTORS['close_match_popup'])
            close_button.click()
            
            logger.info("Closed match popup")
            
        except TimeoutException:
            # No match popup appeared
            pass
            
    def _check_out_of_likes(self):
        """
        Check if we've run out of likes.
        
        Returns:
            bool: True if out of likes, False otherwise
        """
        try:
            self.driver.find_element(By.XPATH, self.SELECTORS['out_of_likes'])
            return True
        except NoSuchElementException:
            return False