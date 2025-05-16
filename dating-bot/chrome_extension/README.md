# Bumble Bot Chrome Extension

A Chrome extension that serves as the frontend for the Bumble dating bot, allowing users to control the bot's settings, view results, and interact with the backend API.

## Features

- **Authentication**: Securely log in to the Bumble Bot backend
- **Swiping Control**: Start, stop, and configure automated swiping
- **Match Management**: View and manage your matches
- **Message Filtering**: Configure "timewaster" detection settings
- **Conversation Management**: View and analyze conversations
- **Statistics**: Track your dating app performance

## Installation

### Development Mode

1. Clone or download this repository
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable "Developer mode" using the toggle in the top-right corner
4. Click "Load unpacked" and select the `chrome_extension` directory
5. The extension should now appear in your Chrome toolbar

### Production Mode (Coming Soon)

In the future, this extension will be available on the Chrome Web Store for easy installation.

## Configuration

1. Click the extension icon in your Chrome toolbar
2. If not logged in, you'll be prompted to enter:
   - API URL: The URL of your Bumble Bot backend server
   - Username: Your Bumble Bot account username
   - Password: Your Bumble Bot account password
3. After logging in, you can access detailed settings by clicking the "Settings" button

## Usage

### Quick Controls (Popup)

Click the extension icon in your Chrome toolbar to access quick controls:

- **Start/Stop Swiping**: Begin or pause the automated swiping process
- **Status Information**: View current bot status, match count, and message count
- **Quick Stats**: See your swiping and matching performance at a glance

### Detailed Settings (Options Page)

Access the options page by clicking "Settings" in the popup or right-clicking the extension icon and selecting "Options":

#### Swiping Settings

- **Swipe Mode**: Choose between automatic, selective, or manual swiping
- **Swipe Rate**: Control how many profiles to swipe per hour
- **Like Ratio**: Set the percentage of profiles to like vs. dislike
- **Schedule**: Configure when the bot should be active
- **Profile Preferences**: Set criteria for profiles to like

#### Messaging Settings

- **Auto Reply**: Configure if and when the bot should automatically reply
- **Reply Delay**: Set how long to wait before responding
- **Message Templates**: Create and manage templates for opening and follow-up messages

#### Filter Settings

- **Filter Mode**: Choose how to handle potential timewasters
- **Filter Criteria**: Configure what patterns indicate a timewaster
- **Actions**: Set what actions to take when a timewaster is detected

#### Account Settings

- **API Configuration**: Update your backend API URL
- **Notifications**: Configure notification preferences
- **Data Management**: Export or clear your local data

## Integration with Bumble Website

When you visit the Bumble website with the extension installed:

1. The extension will detect when you're on the Bumble app pages
2. It will communicate with the backend to sync your settings and status
3. You can view real-time information about the profiles you see
4. The bot can provide suggestions or take automated actions based on your settings

## Troubleshooting

If you encounter issues:

1. Ensure your backend API is running and accessible
2. Check that your API URL is correctly configured
3. Verify your login credentials
4. Try refreshing the Bumble website
5. Restart Chrome if necessary

## Privacy & Security

- All communication with the backend is secured via HTTPS
- Authentication tokens are stored securely in Chrome's local storage
- No personal data is shared with third parties
- The extension only accesses the Bumble website when necessary

## Development

This extension is built using:

- HTML/CSS for the user interface
- JavaScript for functionality
- Chrome Extension APIs for browser integration

The code is organized as follows:

- `manifest.json`: Extension configuration
- `js/`: JavaScript files
  - `api.js`: Backend API communication
  - `background.js`: Background processes and state management
  - `content.js`: Interaction with the Bumble website
  - `popup.js`: Popup interface functionality
  - `options.js`: Options page functionality
- `html/`: HTML files for the user interface
- `css/`: Stylesheets
- `images/`: Icons and images

## License

This project is proprietary software. All rights reserved.