# dating-bot, aka Bumble Bot System

A comprehensive automation system for Bumble dating app with a Python backend and Chrome extension frontend.

## Overview

The Bumble Bot System automates interactions on the Bumble dating platform, helping users manage their dating experience more efficiently. The system consists of two main components:

1. **Python Backend**: A REST API server that controls the Bumble automation bot
2. **Chrome Extension**: A user-friendly interface for controlling the bot and viewing results

## System Architecture

![System Architecture](https://i.imgur.com/JGvXZXs.png)

The system follows a client-server architecture:

- **Backend**: Python-based REST API using FastAPI, with Selenium for browser automation
- **Frontend**: Chrome extension with HTML/CSS/JavaScript
- **Communication**: JSON-based API calls between frontend and backend
- **Authentication**: JWT (JSON Web Token) for secure API access

## Key Features

- **Automated Swiping**: Configure and run automated swiping sessions
- **Message Management**: View and respond to matches and conversations
- **Timewaster Detection**: Automatically identify low-quality matches based on message patterns
- **Customizable Settings**: Configure bot behavior through an intuitive interface
- **Secure Communication**: Encrypted communication between frontend and backend

## Quick Start

### Backend Setup

1. Install Python 3.8 or higher
2. Clone the repository
3. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
4. Configure the API:
   ```bash
   # Edit config/api_config.json with your settings
   ```
5. Start the API server:
   ```bash
   python run_api.py
   ```

### Chrome Extension Setup

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" and select the `chrome_extension` directory
4. Click the extension icon in your browser toolbar
5. Enter your API connection details and login

For detailed instructions, see the [Installation Guide](docs/installation.md).

## Documentation

- [Installation Guide](docs/installation.md): Detailed setup instructions
- [Usage Guide](docs/usage.md): How to use the system effectively
- [API Documentation](docs/api_docs.md): Complete API reference

## Future Enhancements

### OpenAI API Integration

Future versions will integrate with OpenAI's API to enable:

- **Smart Message Generation**: AI-generated responses based on conversation context
- **Profile Analysis**: Intelligent profile evaluation for better swiping decisions
- **Conversation Quality Assessment**: Advanced analysis of conversation engagement
- **Personalized Interaction**: Tailored messaging based on profile information

## Security Considerations

- The system uses JWT authentication for API security
- All sensitive data is stored locally and not transmitted to third parties
- HTTPS is recommended for production deployments
- Default credentials should be changed before use

## License

This project is for educational purposes only. Users are responsible for ensuring compliance with Bumble's terms of service.

## Disclaimer

This tool is intended for educational purposes only. Use of automation tools may violate Bumble's terms of service. The developers are not responsible for any account restrictions or bans resulting from the use of this software.
