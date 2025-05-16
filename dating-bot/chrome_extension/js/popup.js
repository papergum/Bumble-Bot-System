/**
 * Popup Script for Bumble Bot
 * Handles the popup UI interactions and displays status information
 */

// DOM Elements
const elements = {
  // Sections
  loginSection: document.getElementById('login-section'),
  controlsSection: document.getElementById('controls-section'),
  activitySection: document.getElementById('activity-section'),
  
  // Login form
  loginForm: document.getElementById('login-form'),
  apiUrlInput: document.getElementById('api-url'),
  usernameInput: document.getElementById('username'),
  passwordInput: document.getElementById('password'),
  loginError: document.getElementById('login-error'),
  
  // Status indicators
  connectionStatus: document.getElementById('connection-status'),
  statusDot: document.querySelector('.status-dot'),
  statusText: document.querySelector('.status-text'),
  botStatus: document.getElementById('bot-status'),
  lastActivity: document.getElementById('last-activity'),
  matchCount: document.getElementById('match-count'),
  messageCount: document.getElementById('message-count'),
  
  // Stats
  swipeRate: document.getElementById('swipe-rate'),
  matchRate: document.getElementById('match-rate'),
  responseRate: document.getElementById('response-rate'),
  
  // Buttons
  startButton: document.getElementById('start-button'),
  stopButton: document.getElementById('stop-button'),
  openOptionsButton: document.getElementById('open-options'),
  logoutButton: document.getElementById('logout-button'),
  
  // Activity
  activityList: document.getElementById('activity-list')
};

// State
let isAuthenticated = false;
let isRunning = false;

// Initialize the popup
async function initialize() {
  // Load saved API URL if available
  const savedData = await chrome.storage.local.get(['apiBaseUrl']);
  if (savedData.apiBaseUrl) {
    elements.apiUrlInput.value = savedData.apiBaseUrl;
  }
  
  // Check authentication status
  await checkAuthStatus();
  
  // Set up event listeners
  setupEventListeners();
  
  // Update UI based on current state
  updateUI();
}

// Check if the user is authenticated
async function checkAuthStatus() {
  try {
    // Get status from background script
    const status = await sendMessageToBackground({ type: 'GET_STATUS' });
    
    isAuthenticated = status.isAuthenticated;
    isRunning = status.isRunning;
    
    if (isAuthenticated) {
      updateStatusDisplay(status);
      loadActivityData();
    }
    
    return isAuthenticated;
  } catch (error) {
    console.error('Error checking auth status:', error);
    isAuthenticated = false;
    return false;
  }
}

// Set up event listeners
function setupEventListeners() {
  // Login form submission
  elements.loginForm.addEventListener('submit', handleLogin);
  
  // Control buttons
  elements.startButton.addEventListener('click', handleStartBot);
  elements.stopButton.addEventListener('click', handleStopBot);
  elements.openOptionsButton.addEventListener('click', openOptionsPage);
  elements.logoutButton.addEventListener('click', handleLogout);
  
  // Listen for messages from background script
  chrome.runtime.onMessage.addListener((message) => {
    if (message.type === 'STATUS_UPDATE') {
      updateStatusDisplay(message.data);
    }
  });
}

// Handle login form submission
async function handleLogin(event) {
  event.preventDefault();
  
  const apiUrl = elements.apiUrlInput.value.trim();
  const username = elements.usernameInput.value.trim();
  const password = elements.passwordInput.value;
  
  if (!apiUrl || !username || !password) {
    showError('Please fill in all fields');
    return;
  }
  
  try {
    // Show loading state
    elements.loginForm.classList.add('loading');
    showError('');
    
    // Set API URL first
    await sendMessageToBackground({
      type: 'CONTROL_COMMAND',
      data: {
        action: 'SET_API_URL',
        url: apiUrl
      }
    });
    
    // Attempt login
    const response = await sendMessageToBackground({
      type: 'CONTROL_COMMAND',
      data: {
        action: 'LOGIN',
        username,
        password
      }
    });
    
    if (response.success) {
      isAuthenticated = true;
      await checkAuthStatus();
      updateUI();
    } else {
      showError(response.error || 'Login failed');
    }
  } catch (error) {
    showError(error.message || 'Connection error');
  } finally {
    elements.loginForm.classList.remove('loading');
  }
}

// Handle start bot button click
async function handleStartBot() {
  try {
    elements.startButton.disabled = true;
    
    const response = await sendMessageToBackground({
      type: 'CONTROL_COMMAND',
      data: {
        action: 'START_SWIPING'
      }
    });
    
    if (response.success) {
      isRunning = true;
      updateUI();
    } else {
      showError(response.error || 'Failed to start bot');
    }
  } catch (error) {
    showError(error.message || 'Connection error');
  } finally {
    elements.startButton.disabled = false;
  }
}

// Handle stop bot button click
async function handleStopBot() {
  try {
    elements.stopButton.disabled = true;
    
    const response = await sendMessageToBackground({
      type: 'CONTROL_COMMAND',
      data: {
        action: 'STOP_SWIPING'
      }
    });
    
    if (response.success) {
      isRunning = false;
      updateUI();
    } else {
      showError(response.error || 'Failed to stop bot');
    }
  } catch (error) {
    showError(error.message || 'Connection error');
  } finally {
    elements.stopButton.disabled = false;
  }
}

// Handle logout button click
async function handleLogout() {
  try {
    await sendMessageToBackground({
      type: 'CONTROL_COMMAND',
      data: {
        action: 'LOGOUT'
      }
    });
    
    isAuthenticated = false;
    updateUI();
  } catch (error) {
    showError(error.message || 'Logout failed');
  }
}

// Open the options page
function openOptionsPage() {
  chrome.runtime.openOptionsPage();
}

// Update the UI based on current state
function updateUI() {
  if (isAuthenticated) {
    elements.loginSection.classList.add('hidden');
    elements.controlsSection.classList.remove('hidden');
    elements.activitySection.classList.remove('hidden');
    elements.logoutButton.classList.remove('hidden');
    
    // Update button states based on bot running status
    elements.startButton.disabled = isRunning;
    elements.stopButton.disabled = !isRunning;
    
    // Update connection status
    elements.statusDot.classList.add('connected');
    elements.statusText.textContent = 'Connected';
    
    // Update bot status
    elements.botStatus.textContent = isRunning ? 'Active' : 'Inactive';
    elements.botStatus.className = 'status-value ' + (isRunning ? 'active' : 'inactive');
  } else {
    elements.loginSection.classList.remove('hidden');
    elements.controlsSection.classList.add('hidden');
    elements.activitySection.classList.add('hidden');
    elements.logoutButton.classList.add('hidden');
    
    // Update connection status
    elements.statusDot.classList.remove('connected');
    elements.statusText.textContent = 'Disconnected';
  }
}

// Update status display with data from background
function updateStatusDisplay(data) {
  if (!data) return;
  
  isRunning = data.isRunning;
  
  // Update status indicators
  elements.botStatus.textContent = isRunning ? 'Active' : 'Inactive';
  elements.botStatus.className = 'status-value ' + (isRunning ? 'active' : 'inactive');
  
  // Update last activity time
  if (data.lastActivity) {
    const lastActivityTime = new Date(data.lastActivity);
    elements.lastActivity.textContent = formatTimeAgo(lastActivityTime);
  } else {
    elements.lastActivity.textContent = 'Never';
  }
  
  // Update counts
  if (data.matchCount !== undefined) {
    elements.matchCount.textContent = data.matchCount;
  }
  
  if (data.messageCount !== undefined) {
    elements.messageCount.textContent = data.messageCount;
  }
  
  // Update button states
  elements.startButton.disabled = isRunning;
  elements.stopButton.disabled = !isRunning;
}

// Load recent activity data
async function loadActivityData() {
  try {
    // Get recent activity from background or API
    const activity = await sendMessageToBackground({
      type: 'API_REQUEST',
      data: {
        endpoint: '/api/activity/recent',
        method: 'GET'
      }
    });
    
    if (activity.success && activity.data && activity.data.length > 0) {
      renderActivityList(activity.data);
    } else {
      elements.activityList.innerHTML = '<div class="empty-state">No recent activity</div>';
    }
  } catch (error) {
    console.error('Error loading activity data:', error);
    elements.activityList.innerHTML = '<div class="error-state">Failed to load activity</div>';
  }
}

// Render activity list
function renderActivityList(activities) {
  if (!activities || activities.length === 0) {
    elements.activityList.innerHTML = '<div class="empty-state">No recent activity</div>';
    return;
  }
  
  const activityHTML = activities.map(activity => {
    let icon = '';
    let actionText = '';
    
    switch (activity.type) {
      case 'MATCH':
        icon = '💚';
        actionText = `Matched with ${activity.name}`;
        break;
      case 'MESSAGE':
        icon = '💬';
        actionText = `Message with ${activity.name}`;
        break;
      case 'SWIPE':
        icon = activity.direction === 'right' ? '👍' : '👎';
        actionText = `Swiped ${activity.direction} on profile`;
        break;
      default:
        icon = '📝';
        actionText = activity.description || 'Unknown activity';
    }
    
    return `
      <div class="activity-item">
        <div class="activity-icon">${icon}</div>
        <div class="activity-details">
          <div class="activity-text">${actionText}</div>
          <div class="activity-time">${formatTimeAgo(new Date(activity.timestamp))}</div>
        </div>
      </div>
    `;
  }).join('');
  
  elements.activityList.innerHTML = activityHTML;
}

// Format time ago
function formatTimeAgo(date) {
  if (!date) return 'Never';
  
  const now = new Date();
  const diffMs = now - date;
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHour = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHour / 24);
  
  if (diffSec < 60) {
    return 'Just now';
  } else if (diffMin < 60) {
    return `${diffMin} minute${diffMin !== 1 ? 's' : ''} ago`;
  } else if (diffHour < 24) {
    return `${diffHour} hour${diffHour !== 1 ? 's' : ''} ago`;
  } else {
    return `${diffDay} day${diffDay !== 1 ? 's' : ''} ago`;
  }
}

// Show error message
function showError(message) {
  if (!message) {
    elements.loginError.classList.add('hidden');
    elements.loginError.textContent = '';
    return;
  }
  
  elements.loginError.classList.remove('hidden');
  elements.loginError.textContent = message;
}

// Send message to background script
function sendMessageToBackground(message) {
  return new Promise((resolve, reject) => {
    chrome.runtime.sendMessage(message, response => {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
      } else {
        resolve(response);
      }
    });
  });
}

// Initialize when the popup is loaded
document.addEventListener('DOMContentLoaded', initialize);