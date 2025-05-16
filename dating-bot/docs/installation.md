# Bumble Bot Installation Guide

This guide provides comprehensive instructions for installing and configuring the Bumble Bot system, including both the Python backend and Chrome extension frontend.

## System Requirements

### Backend Requirements
- Python 3.8 or higher
- Chrome browser installed (for Selenium automation)
- 2GB RAM minimum (4GB recommended)
- 1GB free disk space
- Internet connection

### Frontend Requirements
- Google Chrome browser (version 80 or higher)
- Chrome extension development mode enabled

## Backend Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure the API

Edit the configuration files in the `backend/config` directory:

- `api_config.json`: API server configuration
- `default_settings.json`: Bot and filter settings

At minimum, you should update the `secret_key` in `api_config.json` for security:

```json
{
  "security": {
    "secret_key": "YOUR_SECURE_SECRET_KEY",
    "algorithm": "HS256",
    "access_token_expire_minutes": 60
  }
}
```

### 5. Run the API Server

```bash
# From the backend directory
python run_api.py
```

The API server will start and listen on the configured host and port (default: `0.0.0.0:8000`).

### 6. Verify Backend Installation

You can verify that the API is running correctly by accessing the API documentation:

```
http://localhost:8000/docs
```

Or by running the test script:

```bash
python src/api/test_api.py
```

## Chrome Extension Installation

### 1. Load the Extension in Developer Mode

1. Open Google Chrome
2. Navigate to `chrome://extensions/`
3. Enable "Developer mode" using the toggle in the top-right corner
4. Click "Load unpacked" button
5. Select the `chrome_extension` directory from the project

The extension should now appear in your extensions list and in the Chrome toolbar.

### 2. Configure the Extension

1. Click the Bumble Bot icon in the Chrome toolbar
2. Enter the following information in the login form:
   - API URL: The URL where your backend is running (e.g., `http://localhost:8000`)
   - Username: Your API username (default: `admin`)
   - Password: Your API password (default: `admin`)
3. Click "Login" to connect to the backend

### 3. Verify Extension Installation

After logging in, the extension popup should show:
- A green "Connected" status indicator
- Bot controls (Start/Stop buttons)
- Quick stats section

If you see these elements, the extension is correctly installed and connected to the backend.

## Configuration Options

### Backend Configuration

The backend configuration is stored in two main files:

#### 1. `api_config.json`

```json
{
  "api": {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": false,
    "reload": true,
    "workers": 4,
    "cors_origins": ["*"],
    "api_prefix": "/api/v1"
  },
  "security": {
    "secret_key": "REPLACE_WITH_SECURE_SECRET_KEY",
    "algorithm": "HS256",
    "access_token_expire_minutes": 60
  },
  "rate_limiting": {
    "enabled": true,
    "requests_per_minute": 60
  },
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  }
}
```

Key settings to consider:
- `host` and `port`: Where the API server will listen
- `cors_origins`: Allowed origins for CORS (set to specific origins in production)
- `secret_key`: JWT secret key (change this for security)
- `access_token_expire_minutes`: Token expiration time

#### 2. `default_settings.json`

This file contains default settings for the bot and message filter:

```json
{
  "bot": {
    "headless": true,
    "profile_path": "",
    "swipe": {
      "default_count": 50,
      "default_like_ratio": 0.7,
      "default_delay": 2
    }
  },
  "filter": {
    "min_message_length": 5,
    "max_response_time": 86400,
    "min_engagement_score": 0.5,
    "min_question_ratio": 0.2,
    "max_one_word_ratio": 0.5,
    "red_flag_patterns": [
      "(?i)instagram",
      "(?i)snapchat",
      "(?i)follow me",
      "(?i)my profile",
      "(?i)venmo",
      "(?i)cashapp",
      "(?i)paypal",
      "(?i)send money",
      "(?i)not here often",
      "(?i)check my bio"
    ]
  }
}
```

Key settings to consider:
- `headless`: Whether to run Chrome in headless mode
- `profile_path`: Path to Chrome profile (for maintaining login sessions)
- `swipe` settings: Default values for auto-swiping
- `filter` settings: Parameters for the timewaster detection algorithm

### Chrome Extension Configuration

The extension settings can be configured through the options page:

1. Right-click the extension icon in the toolbar
2. Select "Options" from the menu
3. Configure settings in the following tabs:
   - **Swiping**: Configure swiping behavior and schedule
   - **Messaging**: Set up auto-reply and message templates
   - **Filters**: Configure timewaster detection parameters
   - **Account**: Manage API connection and notification settings

## Troubleshooting

### Backend Issues

#### Chrome Driver Problems

If you encounter issues with Chrome driver:

1. Make sure Chrome is installed and up to date
2. Check that `webdriver-manager` is correctly installing the Chrome driver
3. Try manually downloading the Chrome driver that matches your Chrome version and specify its path

#### API Connection Issues

If you can't connect to the API:

1. Check that the API server is running
2. Verify the host and port configuration in `api_config.json`
3. Ensure your firewall allows connections to the specified port
4. Check if another service is using the same port

#### Authentication Issues

If you encounter authentication problems:

1. Verify that you're using the correct username and password
2. Check that the JWT token is being correctly included in the `Authorization` header
3. Ensure the `secret_key` in `api_config.json` hasn't been changed after generating tokens

### Chrome Extension Issues

#### Extension Not Loading

If the extension doesn't load:

1. Check for errors in the Chrome extension page (`chrome://extensions/`)
2. Click "Errors" to view any loading errors
3. Ensure all required files are present in the extension directory

#### Connection Problems

If the extension can't connect to the backend:

1. Verify the API URL is correct (including `http://` or `https://` prefix)
2. Check that the backend server is running
3. Ensure there are no CORS issues (check browser console for errors)
4. Try using `localhost` instead of `127.0.0.1` or vice versa

#### Interface Issues

If the extension UI doesn't display correctly:

1. Check for JavaScript errors in the browser console
2. Try reloading the extension
3. Clear browser cache and reload

## Security Considerations

1. **API Security**:
   - Change the default `secret_key` in `api_config.json`
   - Change the default admin credentials
   - Use HTTPS in production environments
   - Restrict CORS origins to trusted domains

2. **Chrome Extension Security**:
   - Don't share your extension with others if it contains your API credentials
   - Be cautious when installing the extension on shared computers

3. **Bot Detection Avoidance**:
   - Use a dedicated Chrome profile for the bot
   - Configure reasonable delays between actions
   - Don't run the bot continuously for extended periods

## Next Steps

After installation, you can:

1. Connect the Chrome extension to the API
2. Configure the bot settings through the extension options
3. Start automating Bumble interactions

For more information on using the system, refer to the [Usage Guide](usage.md).