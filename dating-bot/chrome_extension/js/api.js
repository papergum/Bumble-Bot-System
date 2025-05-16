/**
 * API Utility Module for Bumble Bot
 * Handles all communication with the backend API
 */

class BumbleBotAPI {
  constructor() {
    // Base URL for API - this should be configurable in the options
    this.baseUrl = '';
    this.token = null;
    this.initializeFromStorage();
  }

  /**
   * Initialize API configuration from Chrome storage
   */
  async initializeFromStorage() {
    const data = await chrome.storage.local.get(['apiBaseUrl', 'authToken']);
    if (data.apiBaseUrl) {
      this.baseUrl = data.apiBaseUrl;
    }
    if (data.authToken) {
      this.token = data.authToken;
    }
  }

  /**
   * Set the API base URL
   * @param {string} url - The base URL for the API
   */
  async setBaseUrl(url) {
    this.baseUrl = url;
    await chrome.storage.local.set({ apiBaseUrl: url });
  }

  /**
   * Set the authentication token
   * @param {string} token - JWT token
   */
  async setToken(token) {
    this.token = token;
    await chrome.storage.local.set({ authToken: token });
  }

  /**
   * Clear the authentication token
   */
  async clearToken() {
    this.token = null;
    await chrome.storage.local.remove('authToken');
  }

  /**
   * Check if the user is authenticated
   * @returns {boolean} - Authentication status
   */
  isAuthenticated() {
    return !!this.token;
  }

  /**
   * Make an API request
   * @param {string} endpoint - API endpoint
   * @param {string} method - HTTP method
   * @param {Object} data - Request payload
   * @returns {Promise<Object>} - API response
   */
  async request(endpoint, method = 'GET', data = null) {
    if (!this.baseUrl) {
      throw new Error('API base URL not configured');
    }

    const url = `${this.baseUrl}${endpoint}`;
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    // Add authentication token if available
    if (this.token) {
      options.headers['Authorization'] = `Bearer ${this.token}`;
    }

    // Add request body for non-GET requests
    if (data && method !== 'GET') {
      options.body = JSON.stringify(data);
    }

    try {
      const response = await fetch(url, options);
      
      // Handle HTTP errors
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `API Error: ${response.status}`);
      }
      
      // Parse JSON response
      const responseData = await response.json();
      return responseData;
    } catch (error) {
      console.error('API Request Error:', error);
      throw error;
    }
  }

  // Authentication Endpoints

  /**
   * Login with credentials
   * @param {string} username - Username
   * @param {string} password - Password
   * @returns {Promise<Object>} - Login response with token
   */
  async login(username, password) {
    const response = await this.request('/api/auth/login', 'POST', { username, password });
    if (response.token) {
      await this.setToken(response.token);
    }
    return response;
  }

  /**
   * Check authentication status
   * @returns {Promise<Object>} - Authentication status
   */
  async checkAuthStatus() {
    return await this.request('/api/auth/status');
  }

  // Swiping Control Endpoints

  /**
   * Start automated swiping
   * @returns {Promise<Object>} - Start response
   */
  async startSwiping() {
    return await this.request('/api/swipe/start', 'POST');
  }

  /**
   * Stop automated swiping
   * @returns {Promise<Object>} - Stop response
   */
  async stopSwiping() {
    return await this.request('/api/swipe/stop', 'POST');
  }

  /**
   * Get current swiping status
   * @returns {Promise<Object>} - Swiping status
   */
  async getSwipingStatus() {
    return await this.request('/api/swipe/status');
  }

  /**
   * Update swiping settings
   * @param {Object} settings - Swiping settings
   * @returns {Promise<Object>} - Update response
   */
  async updateSwipingSettings(settings) {
    return await this.request('/api/swipe/settings', 'PUT', settings);
  }

  // Match Management Endpoints

  /**
   * Get list of matches
   * @returns {Promise<Array>} - List of matches
   */
  async getMatches() {
    return await this.request('/api/matches');
  }

  /**
   * Get specific match details
   * @param {string} matchId - Match ID
   * @returns {Promise<Object>} - Match details
   */
  async getMatchDetails(matchId) {
    return await this.request(`/api/matches/${matchId}`);
  }

  /**
   * Unmatch with a person
   * @param {string} matchId - Match ID
   * @returns {Promise<Object>} - Unmatch response
   */
  async unmatch(matchId) {
    return await this.request(`/api/matches/${matchId}`, 'DELETE');
  }

  // Message Filtering Endpoints

  /**
   * Get messages for a match
   * @param {string} matchId - Match ID
   * @returns {Promise<Array>} - List of messages
   */
  async getMessages(matchId) {
    return await this.request(`/api/messages/${matchId}`);
  }

  /**
   * Update filter settings
   * @param {Object} settings - Filter settings
   * @returns {Promise<Object>} - Update response
   */
  async updateFilterSettings(settings) {
    return await this.request('/api/messages/filter/settings', 'PUT', settings);
  }

  /**
   * Get statistics on filtered messages
   * @returns {Promise<Object>} - Filter statistics
   */
  async getFilterStats() {
    return await this.request('/api/messages/filter/stats');
  }
}

// Create and export a singleton instance
const api = new BumbleBotAPI();