/**
 * Content Script for Bumble Bot
 * Injected into Bumble pages to interact with the website
 */

// State tracking
let initialized = false;
let observingPage = false;

// Initialize the content script
function initialize() {
  if (initialized) return;
  initialized = true;
  
  console.log('Bumble Bot content script initialized');
  
  // Start observing the page for changes
  startPageObserver();
  
  // Listen for messages from the extension
  chrome.runtime.onMessage.addListener(handleExtensionMessages);
  
  // Notify the extension that the content script is active
  notifyExtension('CONTENT_SCRIPT_ACTIVE', { url: window.location.href });
}

// Start observing the page for relevant changes
function startPageObserver() {
  if (observingPage) return;
  observingPage = true;
  
  // Create a mutation observer to watch for DOM changes
  const observer = new MutationObserver((mutations) => {
    // Check if we're on a relevant page
    if (window.location.pathname.includes('/app')) {
      detectBumbleState();
    }
  });
  
  // Start observing the document body for changes
  observer.observe(document.body, { 
    childList: true, 
    subtree: true 
  });
  
  // Initial state detection
  detectBumbleState();
}

// Detect the current state of the Bumble interface
function detectBumbleState() {
  // Check if we're on the swiping interface
  const isSwipingPage = !!document.querySelector('[data-qa-role="encounters-match"]') || 
                        !!document.querySelector('[data-qa-role="encounters-action"]');
  
  // Check if we're on the messaging interface
  const isMessagingPage = !!document.querySelector('[data-qa-role="conversation"]');
  
  // Check if we're on the matches list
  const isMatchesPage = !!document.querySelector('[data-qa-role="conversation-list"]');
  
  // Notify the extension of the current state
  if (isSwipingPage || isMessagingPage || isMatchesPage) {
    notifyExtension('PAGE_STATE_CHANGED', {
      isSwipingPage,
      isMessagingPage,
      isMatchesPage,
      url: window.location.href
    });
  }
}

// Handle messages from the extension
function handleExtensionMessages(message, sender, sendResponse) {
  if (!message || !message.type) return;
  
  switch (message.type) {
    case 'GET_PAGE_STATE':
      // Return the current state of the page
      sendResponse({
        url: window.location.href,
        isSwipingPage: !!document.querySelector('[data-qa-role="encounters-match"]') || 
                       !!document.querySelector('[data-qa-role="encounters-action"]'),
        isMessagingPage: !!document.querySelector('[data-qa-role="conversation"]'),
        isMatchesPage: !!document.querySelector('[data-qa-role="conversation-list"]')
      });
      break;
      
    case 'EXTRACT_PROFILE_DATA':
      // Extract profile data from the current page
      const profileData = extractProfileData();
      sendResponse({ success: true, data: profileData });
      break;
      
    case 'EXTRACT_CONVERSATION_DATA':
      // Extract conversation data from the current page
      const conversationData = extractConversationData();
      sendResponse({ success: true, data: conversationData });
      break;
      
    case 'PERFORM_ACTION':
      // Perform an action on the page (like, dislike, etc.)
      performAction(message.data.action)
        .then(result => sendResponse({ success: true, result }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true; // Keep the message channel open for async response
      
    default:
      console.log('Unknown message type:', message.type);
      sendResponse({ success: false, error: 'Unknown message type' });
  }
}

// Extract profile data from the current page
function extractProfileData() {
  try {
    // This is a simplified version - in a real implementation,
    // we would need to handle different page layouts and extract more data
    const nameElement = document.querySelector('[data-qa-role="profile-name"]');
    const ageElement = document.querySelector('[data-qa-role="profile-age"]');
    const bioElement = document.querySelector('[data-qa-role="profile-bio"]');
    const photoElements = document.querySelectorAll('[data-qa-role="profile-photo"]');
    
    const photos = Array.from(photoElements || []).map(el => {
      const img = el.querySelector('img');
      return img ? img.src : null;
    }).filter(Boolean);
    
    return {
      name: nameElement ? nameElement.textContent.trim() : '',
      age: ageElement ? parseInt(ageElement.textContent.trim(), 10) : null,
      bio: bioElement ? bioElement.textContent.trim() : '',
      photos
    };
  } catch (error) {
    console.error('Error extracting profile data:', error);
    return {};
  }
}

// Extract conversation data from the current page
function extractConversationData() {
  try {
    // This is a simplified version - in a real implementation,
    // we would need to handle different message types and formats
    const messageElements = document.querySelectorAll('[data-qa-role="message"]');
    
    const messages = Array.from(messageElements || []).map(el => {
      const isOutgoing = el.classList.contains('outgoing') || 
                         el.hasAttribute('data-qa-outgoing');
      const textElement = el.querySelector('[data-qa-role="message-text"]');
      const timestampElement = el.querySelector('[data-qa-role="message-timestamp"]');
      
      return {
        text: textElement ? textElement.textContent.trim() : '',
        timestamp: timestampElement ? timestampElement.textContent.trim() : '',
        isOutgoing
      };
    });
    
    return {
      messages,
      matchName: document.querySelector('[data-qa-role="conversation-header-name"]')?.textContent.trim() || ''
    };
  } catch (error) {
    console.error('Error extracting conversation data:', error);
    return { messages: [] };
  }
}

// Perform an action on the page
async function performAction(action) {
  try {
    switch (action) {
      case 'LIKE':
        // Click the like button
        const likeButton = document.querySelector('[data-qa-role="encounters-action-like"]');
        if (likeButton) {
          likeButton.click();
          return { success: true, action: 'LIKE' };
        }
        throw new Error('Like button not found');
        
      case 'DISLIKE':
        // Click the dislike button
        const dislikeButton = document.querySelector('[data-qa-role="encounters-action-dislike"]');
        if (dislikeButton) {
          dislikeButton.click();
          return { success: true, action: 'DISLIKE' };
        }
        throw new Error('Dislike button not found');
        
      case 'SUPER_LIKE':
        // Click the super like button
        const superLikeButton = document.querySelector('[data-qa-role="encounters-action-superlike"]');
        if (superLikeButton) {
          superLikeButton.click();
          return { success: true, action: 'SUPER_LIKE' };
        }
        throw new Error('Super like button not found');
        
      case 'OPEN_PROFILE':
        // Click to open the full profile
        const profileButton = document.querySelector('[data-qa-role="encounters-match"]');
        if (profileButton) {
          profileButton.click();
          return { success: true, action: 'OPEN_PROFILE' };
        }
        throw new Error('Profile button not found');
        
      default:
        throw new Error(`Unknown action: ${action}`);
    }
  } catch (error) {
    console.error(`Error performing action ${action}:`, error);
    throw error;
  }
}

// Send a message to the extension
function notifyExtension(type, data = {}) {
  chrome.runtime.sendMessage({
    type,
    data,
    timestamp: new Date().toISOString()
  }).catch(error => {
    // Ignore errors when the extension is not listening
    console.debug('Error sending message to extension:', error);
  });
}

// Initialize the content script
initialize();