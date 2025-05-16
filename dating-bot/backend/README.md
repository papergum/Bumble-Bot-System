# Bumble Bot API

A REST API for frontend-backend communication in the Bumble automation bot system.

## Overview

This API provides endpoints for controlling the Bumble bot, managing matches, and filtering conversations to detect potential timewasters. It serves as the communication layer between the Chrome extension frontend and the Python backend that performs the actual Bumble automation.

## Features

- **Authentication**: Secure JWT-based authentication system
- **Swiping Control**: Start, stop, and configure automated swiping
- **Match Management**: Retrieve and interact with matches
- **Message Filtering**: Detect potential timewasters based on message content and patterns
- **Conversation Analysis**: Analyze conversations for engagement and sentiment

## Project Structure

```
backend/
├── src/
│   ├── bumble_bot/          # Core bot functionality
│   │   ├── __init__.py
│   │   ├── bot.py           # Main bot class
│   │   ├── login.py         # Login functionality
│   │   ├── navigator.py     # Page navigation
│   │   └── swiper.py        # Swiping functionality
│   ├── message_filter/      # Message filtering logic
│   │   ├── __init__.py
│   │   ├── analyzer.py      # Message content analysis
│   │   └── filter.py        # Timewaster detection
│   └── api/                 # API implementation
│       ├── __init__.py
│       ├── server.py        # Main API server
│       ├── routes/          # API routes
│       │   ├── __init__.py
│       │   ├── auth.py      # Authentication endpoints
│       │   ├── swipe.py     # Swiping control endpoints
│       │   ├── matches.py   # Match management endpoints
│       │   └── messages.py  # Message and filter endpoints
│       └── utils/           # Utility functions
│           ├── __init__.py
│           └── response.py  # Response formatting
├── config/                  # Configuration files
│   ├── api_config.json      # API configuration
│   └── default_settings.json # Default bot settings
├── docs/                    # Documentation
│   ├── installation.md      # Installation guide
│   ├── usage.md             # Usage instructions
│   └── api_docs.md          # API documentation
├── run_api.py               # Script to run the API server
└── requirements.txt         # Python dependencies
```

## Getting Started

### Installation

See the [Installation Guide](docs/installation.md) for detailed setup instructions.

Quick start:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API server
python run_api.py
```

### Usage

See the [Usage Guide](docs/usage.md) for detailed usage instructions.

Basic authentication:

```bash
# Get an access token
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin"
```

## API Documentation

See the [API Documentation](docs/api_docs.md) for detailed endpoint information.

Main endpoints:

- `/api/v1/auth/*` - Authentication endpoints
- `/api/v1/swipe/*` - Swiping control endpoints
- `/api/v1/matches/*` - Match management endpoints
- `/api/v1/messages/*` - Message filtering endpoints

## Technologies Used

- **FastAPI**: Modern, high-performance web framework for building APIs
- **Selenium**: Web browser automation for Bumble interaction
- **JWT**: JSON Web Tokens for secure authentication
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for running the API

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.