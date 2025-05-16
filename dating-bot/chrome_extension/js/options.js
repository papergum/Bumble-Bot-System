/**
 * Options Page Script for Bumble Bot
 * Handles settings configuration and UI interactions
 */

// DOM Elements
const elements = {
  // Sections
  loginSection: document.getElementById('login-section'),
  settingsSection: document.getElementById('settings-section'),
  statsSection: document.getElementById('stats-section'),
  
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
  
  // Tabs
  tabButtons: document.querySelectorAll('.tab-button'),
  tabContents: document.querySelectorAll('.tab-content'),
  
  // Forms
  swipingForm: document.getElementById('swiping-form'),
  messagingForm: document.getElementById('messaging-form'),
  filtersForm: document.getElementById('filters-form'),
  accountForm: document.getElementById('account-form'),
  
  // Swiping settings
  swipeMode: document.getElementById('swipe-mode'),
  swipeRate: document.getElementById('swipe-rate'),
  swipeRateValue: document.getElementById('swipe-rate-value'),
  likeRatio: document.getElementById('like-ratio'),
  likeRatioValue: document.getElementById('like-ratio-value'),
  scheduleDays: document.querySelectorAll('input[name="schedule-day"]'),
  startTime: document.getElementById('start-time'),
  endTime: document.getElementById('end-time'),
  preferVerified: document.getElementById('prefer-verified'),
  preferWithBio: document.getElementById('prefer-with-bio'),
  preferWithInterests: document.getElementById('prefer-with-interests'),
  
  // Messaging settings
  autoReply: document.getElementById('auto-reply'),
  replyDelay: document.getElementById('reply-delay'),
  replyDelayValue: document.getElementById('reply-delay-value'),
  openingMessages: document.querySelector('#messaging-tab .message-templates'),
  followUpMessages: document.querySelector('#messaging-tab .message-templates:nth-of-type(2)'),
  
  // Filter settings
  filterMode: document.getElementById('filter-mode'),
  filterOneWord: document.getElementById('filter-one-word'),
  filterNoQuestions: document.getElementById('filter-no-questions'),
  filterResponseTime: document.getElementById('filter-response-time'),
  slowResponseHours: document.getElementById('slow-response-hours'),
  filterKeywords: document.getElementById('filter-keywords'),
  filterKeywordsList: document.getElementById('filter-keywords-list'),
  actionFlag: document.getElementById('action-flag'),
  actionDeprioritize: document.getElementById('action-deprioritize'),
  actionUnmatch: document.getElementById('action-unmatch'),
  
  // Account settings
  apiUrlSettings: document.getElementById('api-url-settings'),
  notificationMode: document.getElementById('notification-mode'),
  exportDataButton: document.getElementById('export-data'),
  clearDataButton: document.getElementById('clear-data'),
  logoutButton: document.getElementById('logout-button'),
  
  // Stats
  totalSwipes: document.getElementById('total-swipes'),
  totalMatches: document.getElementById('total-matches'),
  totalConversations: document.getElementById('total-conversations'),
  responseRate: document.getElementById('response-rate'),
  activityChart: document.getElementById('activity-chart'),
  
  // Other
  viewDocsLink: document.getElementById('view-docs')
};

// State
let isAuthenticated = false;
let currentSettings = {
  swiping: {},
  messaging: {},
  filters: {},
  account: {}
};

// Initialize the options page
async function initialize() {
  // Load saved API URL if available
  const savedData = await chrome.storage.local.get(['apiBaseUrl']);
  if (savedData.apiBaseUrl) {
    elements.apiUrlInput.value = savedData.apiBaseUrl;
    elements.apiUrlSettings.value = savedData.apiBaseUrl;
  }
  
  // Check authentication status
  await checkAuthStatus();
  
  // Set up event listeners
  setupEventListeners();
  
  // Update UI based on current state
  updateUI();
  
  // Load settings if authenticated
  if (isAuthenticated) {
    await loadSettings();
    await loadStats();
  }
}

// Check if the user is authenticated
async function checkAuthStatus() {
  try {
    // Get status from background script
    const status = await sendMessageToBackground({ type: 'GET_STATUS' });
    isAuthenticated = status.isAuthenticated;
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
  
  // Tab switching
  elements.tabButtons.forEach(button => {
    button.addEventListener('click', () => switchTab(button.dataset.tab));
  });
  
  // Form submissions
  elements.swipingForm.addEventListener('submit', handleSwipingFormSubmit);
  elements.messagingForm.addEventListener('submit', handleMessagingFormSubmit);
  elements.filtersForm.addEventListener('submit', handleFiltersFormSubmit);
  elements.accountForm.addEventListener('submit', handleAccountFormSubmit);
  
  // Range input value displays
  elements.swipeRate.addEventListener('input', () => {
    elements.swipeRateValue.textContent = elements.swipeRate.value;
  });
  
  elements.likeRatio.addEventListener('input', () => {
    elements.likeRatioValue.textContent = elements.likeRatio.value;
  });
  
  elements.replyDelay.addEventListener('input', () => {
    elements.replyDelayValue.textContent = elements.replyDelay.value;
  });
  
  // Add/remove message templates
  document.querySelectorAll('.add-template').forEach(button => {
    button.addEventListener('click', addMessageTemplate);
  });
  
  // Delegate event for dynamically added remove buttons
  document.addEventListener('click', event => {
    if (event.target.classList.contains('remove-template')) {
      removeMessageTemplate(event.target);
    }
  });
  
  // Account actions
  elements.exportDataButton.addEventListener('click', exportData);
  elements.clearDataButton.addEventListener('click', clearData);
  elements.logoutButton.addEventListener('click', handleLogout);
  
  // Documentation link
  elements.viewDocsLink.addEventListener('click', openDocumentation);
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
      await loadSettings();
      await loadStats();
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

// Switch between tabs
function switchTab(tabId) {
  // Update active tab button
  elements.tabButtons.forEach(button => {
    if (button.dataset.tab === tabId) {
      button.classList.add('active');
    } else {
      button.classList.remove('active');
    }
  });
  
  // Show active tab content
  elements.tabContents.forEach(content => {
    if (content.id === `${tabId}-tab`) {
      content.classList.add('active');
    } else {
      content.classList.remove('active');
    }
  });
}

// Handle swiping form submission
async function handleSwipingFormSubmit(event) {
  event.preventDefault();
  
  const settings = {
    mode: elements.swipeMode.value,
    rate: parseInt(elements.swipeRate.value, 10),
    likeRatio: parseInt(elements.likeRatio.value, 10),
    schedule: {
      days: Array.from(elements.scheduleDays)
        .filter(checkbox => checkbox.checked)
        .map(checkbox => checkbox.value),
      startTime: elements.startTime.value,
      endTime: elements.endTime.value
    },
    preferences: {
      preferVerified: elements.preferVerified.checked,
      preferWithBio: elements.preferWithBio.checked,
      preferWithInterests: elements.preferWithInterests.checked
    }
  };
  
  try {
    const response = await sendMessageToBackground({
      type: 'CONTROL_COMMAND',
      data: {
        action: 'UPDATE_SETTINGS',
        settings: {
          swiping: settings
        }
      }
    });
    
    if (response.success) {
      showSaveSuccess('swiping');
    } else {
      showSaveError('swiping', response.error);
    }
  } catch (error) {
    showSaveError('swiping', error.message);
  }
}

// Handle messaging form submission
async function handleMessagingFormSubmit(event) {
  event.preventDefault();
  
  // Get all opening message templates
  const openingTemplates = Array.from(
    elements.openingMessages.querySelectorAll('.message-template textarea')
  ).map(textarea => textarea.value.trim()).filter(Boolean);
  
  // Get all follow-up message templates
  const followUpTemplates = Array.from(
    elements.followUpMessages.querySelectorAll('.message-template textarea')
  ).map(textarea => textarea.value.trim()).filter(Boolean);
  
  const settings = {
    autoReply: elements.autoReply.value,
    replyDelay: parseInt(elements.replyDelay.value, 10),
    templates: {
      opening: openingTemplates,
      followUp: followUpTemplates
    }
  };
  
  try {
    const response = await sendMessageToBackground({
      type: 'CONTROL_COMMAND',
      data: {
        action: 'UPDATE_SETTINGS',
        settings: {
          messaging: settings
        }
      }
    });
    
    if (response.success) {
      showSaveSuccess('messaging');
    } else {
      showSaveError('messaging', response.error);
    }
  } catch (error) {
    showSaveError('messaging', error.message);
  }
}

// Handle filters form submission
async function handleFiltersFormSubmit(event) {
  event.preventDefault();
  
  const keywords = elements.filterKeywordsList.value
    .split(',')
    .map(keyword => keyword.trim())
    .filter(Boolean);
  
  const settings = {
    mode: elements.filterMode.value,
    criteria: {
      oneWordResponses: elements.filterOneWord.checked,
      noQuestions: elements.filterNoQuestions.checked,
      slowResponseTime: elements.filterResponseTime.checked,
      slowResponseThreshold: parseInt(elements.slowResponseHours.value, 10),
      keywords: elements.filterKeywords.checked ? keywords : []
    },
    actions: {
      flag: elements.actionFlag.checked,
      deprioritize: elements.actionDeprioritize.checked,
      unmatch: elements.actionUnmatch.checked
    }
  };
  
  try {
    const response = await sendMessageToBackground({
      type: 'CONTROL_COMMAND',
      data: {
        action: 'UPDATE_FILTER',
        settings: settings
      }
    });
    
    if (response.success) {
      showSaveSuccess('filters');
    } else {
      showSaveError('filters', response.error);
    }
  } catch (error) {
    showSaveError('filters', error.message);
  }
}

// Handle account form submission
async function handleAccountFormSubmit(event) {
  event.preventDefault();
  
  const apiUrl = elements.apiUrlSettings.value.trim();
  
  if (!apiUrl) {
    showSaveError('account', 'API URL is required');
    return;
  }
  
  const settings = {
    apiUrl: apiUrl,
    notifications: elements.notificationMode.value
  };
  
  try {
    // Update API URL
    await sendMessageToBackground({
      type: 'CONTROL_COMMAND',
      data: {
        action: 'SET_API_URL',
        url: apiUrl
      }
    });
    
    // Update other account settings
    const response = await sendMessageToBackground({
      type: 'CONTROL_COMMAND',
      data: {
        action: 'UPDATE_SETTINGS',
        settings: {
          account: settings
        }
      }
    });
    
    if (response.success) {
      showSaveSuccess('account');
    } else {
      showSaveError('account', response.error);
    }
  } catch (error) {
    showSaveError('account', error.message);
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
    console.error('Logout error:', error);
    alert('Failed to logout: ' + error.message);
  }
}

// Load settings from the API
async function loadSettings() {
  try {
    // Get swiping settings
    const swipingResponse = await sendMessageToBackground({
      type: 'API_REQUEST',
      data: {
        endpoint: '/api/swipe/settings',
        method: 'GET'
      }
    });
    
    if (swipingResponse.success && swipingResponse.data) {
      currentSettings.swiping = swipingResponse.data;
      populateSwipingSettings(swipingResponse.data);
    }
    
    // Get filter settings
    const filterResponse = await sendMessageToBackground({
      type: 'API_REQUEST',
      data: {
        endpoint: '/api/messages/filter/settings',
        method: 'GET'
      }
    });
    
    if (filterResponse.success && filterResponse.data) {
      currentSettings.filters = filterResponse.data;
      populateFilterSettings(filterResponse.data);
    }
    
    // Get account settings from storage
    const storageData = await chrome.storage.local.get(['apiBaseUrl', 'notificationMode']);
    currentSettings.account = {
      apiUrl: storageData.apiBaseUrl || '',
      notifications: storageData.notificationMode || 'important'
    };
    
    populateAccountSettings(currentSettings.account);
    
  } catch (error) {
    console.error('Error loading settings:', error);
  }
}

// Load statistics from the API
async function loadStats() {
  try {
    // Get swiping stats
    const swipeStatsResponse = await sendMessageToBackground({
      type: 'API_REQUEST',
      data: {
        endpoint: '/api/swipe/stats',
        method: 'GET'
      }
    });
    
    if (swipeStatsResponse.success && swipeStatsResponse.data) {
      updateSwipeStats(swipeStatsResponse.data);
    }
    
    // Get filter stats
    const filterStatsResponse = await sendMessageToBackground({
      type: 'API_REQUEST',
      data: {
        endpoint: '/api/messages/filter/stats',
        method: 'GET'
      }
    });
    
    if (filterStatsResponse.success && filterStatsResponse.data) {
      updateFilterStats(filterStatsResponse.data);
    }
    
  } catch (error) {
    console.error('Error loading stats:', error);
  }
}

// Populate swiping settings form
function populateSwipingSettings(settings) {
  if (!settings) return;
  
  // Set form values
  if (settings.mode) {
    elements.swipeMode.value = settings.mode;
  }
  
  if (settings.rate) {
    elements.swipeRate.value = settings.rate;
    elements.swipeRateValue.textContent = settings.rate;
  }
  
  if (settings.likeRatio !== undefined) {
    elements.likeRatio.value = settings.likeRatio;
    elements.likeRatioValue.textContent = settings.likeRatio;
  }
  
  // Schedule
  if (settings.schedule) {
    if (settings.schedule.days && Array.isArray(settings.schedule.days)) {
      elements.scheduleDays.forEach(checkbox => {
        checkbox.checked = settings.schedule.days.includes(checkbox.value);
      });
    }
    
    if (settings.schedule.startTime) {
      elements.startTime.value = settings.schedule.startTime;
    }
    
    if (settings.schedule.endTime) {
      elements.endTime.value = settings.schedule.endTime;
    }
  }
  
  // Preferences
  if (settings.preferences) {
    if (settings.preferences.preferVerified !== undefined) {
      elements.preferVerified.checked = settings.preferences.preferVerified;
    }
    
    if (settings.preferences.preferWithBio !== undefined) {
      elements.preferWithBio.checked = settings.preferences.preferWithBio;
    }
    
    if (settings.preferences.preferWithInterests !== undefined) {
      elements.preferWithInterests.checked = settings.preferences.preferWithInterests;
    }
  }
}

// Populate messaging settings form
function populateMessagingSettings(settings) {
  if (!settings) return;
  
  // Set form values
  if (settings.autoReply) {
    elements.autoReply.value = settings.autoReply;
  }
  
  if (settings.replyDelay) {
    elements.replyDelay.value = settings.replyDelay;
    elements.replyDelayValue.textContent = settings.replyDelay;
  }
  
  // Templates
  if (settings.templates) {
    // Clear existing templates
    clearMessageTemplates(elements.openingMessages);
    clearMessageTemplates(elements.followUpMessages);
    
    // Add opening templates
    if (settings.templates.opening && Array.isArray(settings.templates.opening)) {
      settings.templates.opening.forEach(template => {
        addMessageTemplate(null, elements.openingMessages, template);
      });
    }
    
    // Add follow-up templates
    if (settings.templates.followUp && Array.isArray(settings.templates.followUp)) {
      settings.templates.followUp.forEach(template => {
        addMessageTemplate(null, elements.followUpMessages, template);
      });
    }
  }
}

// Populate filter settings form
function populateFilterSettings(settings) {
  if (!settings) return;
  
  // Set form values
  if (settings.mode) {
    elements.filterMode.value = settings.mode;
  }
  
  // Criteria
  if (settings.criteria) {
    if (settings.criteria.oneWordResponses !== undefined) {
      elements.filterOneWord.checked = settings.criteria.oneWordResponses;
    }
    
    if (settings.criteria.noQuestions !== undefined) {
      elements.filterNoQuestions.checked = settings.criteria.noQuestions;
    }
    
    if (settings.criteria.slowResponseTime !== undefined) {
      elements.filterResponseTime.checked = settings.criteria.slowResponseTime;
    }
    
    if (settings.criteria.slowResponseThreshold) {
      elements.slowResponseHours.value = settings.criteria.slowResponseThreshold;
    }
    
    if (settings.criteria.keywords && Array.isArray(settings.criteria.keywords)) {
      elements.filterKeywords.checked = settings.criteria.keywords.length > 0;
      elements.filterKeywordsList.value = settings.criteria.keywords.join(', ');
    }
  }
  
  // Actions
  if (settings.actions) {
    if (settings.actions.flag !== undefined) {
      elements.actionFlag.checked = settings.actions.flag;
    }
    
    if (settings.actions.deprioritize !== undefined) {
      elements.actionDeprioritize.checked = settings.actions.deprioritize;
    }
    
    if (settings.actions.unmatch !== undefined) {
      elements.actionUnmatch.checked = settings.actions.unmatch;
    }
  }
}

// Populate account settings form
function populateAccountSettings(settings) {
  if (!settings) return;
  
  if (settings.apiUrl) {
    elements.apiUrlSettings.value = settings.apiUrl;
  }
  
  if (settings.notifications) {
    elements.notificationMode.value = settings.notifications;
  }
}

// Update swipe statistics
function updateSwipeStats(stats) {
  if (!stats) return;
  
  if (stats.totalSwipes !== undefined) {
    elements.totalSwipes.textContent = stats.totalSwipes.toLocaleString();
  }
  
  if (stats.totalMatches !== undefined) {
    elements.totalMatches.textContent = stats.totalMatches.toLocaleString();
  }
  
  if (stats.matchRate !== undefined) {
    const matchRate = (stats.matchRate * 100).toFixed(1);
    elements.responseRate.textContent = `${matchRate}%`;
  }
}

// Update filter statistics
function updateFilterStats(stats) {
  if (!stats) return;
  
  if (stats.totalConversations !== undefined) {
    elements.totalConversations.textContent = stats.totalConversations.toLocaleString();
  }
}

// Add a new message template
function addMessageTemplate(event, container = null, value = '') {
  // If called from event handler
  if (event) {
    event.preventDefault();
    container = event.target.closest('.message-templates');
  }
  
  if (!container) return;
  
  // Find the add button
  const addButton = container.querySelector('.add-template');
  
  // Create new template element
  const templateDiv = document.createElement('div');
  templateDiv.className = 'message-template';
  templateDiv.innerHTML = `
    <textarea placeholder="Enter a message template...">${value}</textarea>
    <button type="button" class="btn btn-icon remove-template">×</button>
  `;
  
  // Insert before the add button
  container.insertBefore(templateDiv, addButton);
}

// Remove a message template
function removeMessageTemplate(button) {
  const template = button.closest('.message-template');
  if (template) {
    template.remove();
  }
}

// Clear all message templates
function clearMessageTemplates(container) {
  if (!container) return;
  
  // Keep the add button
  const addButton = container.querySelector('.add-template');
  
  // Remove all template elements
  container.querySelectorAll('.message-template').forEach(el => el.remove());
  
  // Add a single empty template
  addMessageTemplate(null, container);
}

// Export data
function exportData() {
  // This would typically download all user data as JSON
  alert('Data export functionality would be implemented here');
}

// Clear local data
function clearData() {
  if (confirm('Are you sure you want to clear all local data? This will not affect your account on the server.')) {
    chrome.storage.local.clear(() => {
      alert('Local data cleared successfully');
    });
  }
}

// Open documentation
function openDocumentation(event) {
  event.preventDefault();
  // This would typically open the documentation page
  alert('Documentation would open here');
}

// Update the UI based on current state
function updateUI() {
  if (isAuthenticated) {
    elements.loginSection.classList.add('hidden');
    elements.settingsSection.classList.remove('hidden');
    elements.statsSection.classList.remove('hidden');
    
    // Update connection status
    elements.statusDot.classList.add('connected');
    elements.statusText.textContent = 'Connected';
  } else {
    elements.loginSection.classList.remove('hidden');
    elements.settingsSection.classList.add('hidden');
    elements.statsSection.classList.add('hidden');
    
    // Update connection status
    elements.statusDot.classList.remove('connected');
    elements.statusText.textContent = 'Disconnected';
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

// Show save success message
function showSaveSuccess(formType) {
  const form = document.getElementById(`${formType}-form`);
  if (!form) return;
  
  // Create or update success message
  let successMessage = form.querySelector('.success-message');
  if (!successMessage) {
    successMessage = document.createElement('div');
    successMessage.className = 'success-message';
    form.appendChild(successMessage);
  }
  
  successMessage.textContent = 'Settings saved successfully';
  
  // Remove after a delay
  setTimeout(() => {
    successMessage.remove();
  }, 3000);
}

// Show save error message
function showSaveError(formType, message) {
  const form = document.getElementById(`${formType}-form`);
  if (!form) return;
  
  // Create or update error message
  let errorMessage = form.querySelector('.error-message');
  if (!errorMessage) {
    errorMessage = document.createElement('div');
    errorMessage.className = 'error-message';
    form.appendChild(errorMessage);
  }
  
  errorMessage.textContent = message || 'Failed to save settings';
  
  // Remove after a delay
  setTimeout(() => {
    errorMessage.remove();
  }, 5000);
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

// Initialize when the options page is loaded
document.addEventListener('DOMContentLoaded', initialize);