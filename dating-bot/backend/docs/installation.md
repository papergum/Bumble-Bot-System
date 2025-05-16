# Bumble Bot API Installation Guide

This guide provides instructions for setting up and running the Bumble Bot API.

## Prerequisites

- Python 3.8 or higher
- Chrome browser installed (for Selenium automation)
- pip (Python package manager)

## Installation Steps

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

### 6. Verify Installation

You can verify that the API is running correctly by accessing the API documentation:

```
http://localhost:8000/docs
```

Or by running the test script:

```bash
python src/api/test_api.py
```

## Troubleshooting

### Chrome Driver Issues

If you encounter issues with Chrome driver:

1. Make sure Chrome is installed and up to date
2. Check that `webdriver-manager` is correctly installing the Chrome driver
3. Try manually downloading the Chrome driver that matches your Chrome version and specify its path

### API Connection Issues

If you can't connect to the API:

1. Check that the API server is running
2. Verify the host and port configuration in `api_config.json`
3. Ensure your firewall allows connections to the specified port

### Authentication Issues

If you encounter authentication problems:

1. Verify that you're using the correct username and password
2. Check that the JWT token is being correctly included in the `Authorization` header
3. Ensure the `secret_key` in `api_config.json` hasn't been changed after generating tokens

## Next Steps

After installation, you can:

1. Connect the Chrome extension to the API
2. Configure the bot settings through the API
3. Start automating Bumble interactions

For more information on using the API, refer to the [API Documentation](api_docs.md).