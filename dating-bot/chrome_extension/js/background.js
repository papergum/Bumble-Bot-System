/**
 * Background Service Worker for Bumble Bot
 * Handles background processes, API communication, and state management
 */

// Import API module (will be available through module resolution)
importScripts('api.js');

// Extension state
const state = {
  isRunning: false,
  lastActivity: null,
  matchCount: 0,
  messageCount: 0,
  notifications: []
};

// Initialize the extension
async function initialize() {
  console.log('Initializing Bumble Bot extension...');
  
  // Check if we have stored authentication
  try {
    if (api.isAuthenticated()) {
      const authStatus = await api.checkAuthStatus();
      if (!authStatus.authenticated) {
        await api.clearToken();
      }
    }
    
    // Check if bot is currently running
    const swipeStatus = await api.getSwipingStatus().catch(() => ({ running: false }));
    state.isRunning = swipeStatus.running || false;
    
    // Set up periodic status check
    chrome.alarms.create('statusCheck', { periodInMinutes: 1 });
  } catch (error) {
    console.error('Initialization error:', error);
  }
}

// Handle periodic status check
async function checkStatus() {
  if (!api.isAuthenticated()) return;
  
  try {
    // Check swiping status
    const swipeStatus = await api.getSwipingStatus().catch(() => ({ running: false }));
    state.isRunning = swipeStatus.running || false;
    
    // Update badge based on status
    updateBadge();
    
    // Broadcast status update to any open extension pages
    broadcastStatusUpdate();
  } catch (error) {
    console.error('Status check error:', error);
  }
}

// Update the extension badge
function updateBadge() {
  if (state.isRunning) {
    chrome.action.setBadgeText({ text: 'ON' });
    chrome.action.setBadgeBackgroundColor({ color: '#4CAF50' });
  } else {
    chrome.action.setBadgeText({ text: 'OFF' });
    chrome.action.setBadgeBackgroundColor({ color: '#F44336' });
  }
}

// Broadcast status update to all extension pages
function broadcastStatusUpdate() {
  chrome.runtime.sendMessage({
    type: 'STATUS_UPDATE',
    data: {
      isRunning: state.isRunning,
      lastActivity: state.lastActivity,
      matchCount: state.matchCount,
      messageCount: state.messageCount
    }
  }).catch(() => {
    // Ignore errors when no receivers are listening
  });
}

// Handle messages from other parts of the extension
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  // Handle API requests
  if (message.type === 'API_REQUEST') {
    handleApiRequest(message.data, sendResponse);
    return true; // Keep the message channel open for async response
  }
  
  // Handle control commands
  if (message.type === 'CONTROL_COMMAND') {
    handleControlCommand(message.data, sendResponse);
    return true; // Keep the message channel open for async response
  }
  
  // Handle status requests
  if (message.type === 'GET_STATUS') {
    sendResponse({
      isRunning: state.isRunning,
      lastActivity: state.lastActivity,
      matchCount: state.matchCount,
      messageCount: state.messageCount,
      isAuthenticated: api.isAuthenticated()
    });
    return true;
  }
});

// Handle API requests from other parts of the extension
async function handleApiRequest(request, sendResponse) {
  try {
    const { endpoint, method, data } = request;
    const response = await api.request(endpoint, method, data);
    sendResponse({ success: true, data: response });
  } catch (error) {
    sendResponse({ success: false, error: error.message });
  }
}

// Handle control commands
async function handleControlCommand(command, sendResponse) {
  try {
    let response;
    
    switch (command.action) {
      case 'START_SWIPING':
        response = await api.startSwiping();
        state.isRunning = true;
        break;
        
      case 'STOP_SWIPING':
        response = await api.stopSwiping();
        state.isRunning = false;
        break;
        
      case 'LOGIN':
        response = await api.login(command.username, command.password);
        break;
        
      case 'LOGOUT':
        await api.clearToken();
        response = { success: true };
        break;
        
      case 'UPDATE_SETTINGS':
        response = await api.updateSwipingSettings(command.settings);
        break;
        
      case 'UPDATE_FILTER':
        response = await api.updateFilterSettings(command.settings);
        break;
        
      default:
        throw new Error(`Unknown command: ${command.action}`);
    }
    
    // Update badge and broadcast status
    updateBadge();
    broadcastStatusUpdate();
    
    sendResponse({ success: true, data: response });
  } catch (error) {
    sendResponse({ success: false, error: error.message });
  }
}

// Handle alarm events (periodic tasks)
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'statusCheck') {
    checkStatus();
  }
});

// Initialize on install
chrome.runtime.onInstalled.addListener(() => {
  initialize();
});

// Initialize when service worker starts
initialize();