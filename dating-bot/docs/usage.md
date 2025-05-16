# Bumble Bot Usage Guide

This guide provides comprehensive instructions for using the Bumble Bot system effectively, including both the backend API and Chrome extension frontend.

## Getting Started

### Accessing the System

1. Ensure the backend API server is running:
   ```bash
   cd backend
   python run_api.py
   ```

2. Open Chrome and click the Bumble Bot extension icon in the toolbar

### Authentication

Before using the system, you need to authenticate:

1. In the extension popup, enter:
   - API URL (e.g., `http://localhost:8000`)
   - Username (default: `admin`)
   - Password (default: `admin`)

2. Click "Login"

3. Upon successful authentication, the status indicator will turn green and show "Connected"

## Chrome Extension Interface

### Main Popup

The main extension popup provides quick access to essential functions:

![Extension Popup](https://i.imgur.com/JGvXZXs.png)

#### Status Panel
- **Status**: Current bot status (Active/Inactive)
- **Last Activity**: Time of the most recent bot action
- **Matches**: Number of current matches
- **Messages**: Number of unread messages

#### Control Buttons
- **Start Swiping**: Begin automated swiping session
- **Stop Swiping**: End the current swiping session
- **Settings**: Open the extension options page

#### Quick Stats
- **Swipe Rate**: Average swipes per hour
- **Match Rate**: Percentage of right swipes that result in matches
- **Response Rate**: Percentage of matches that respond to messages

#### Recent Activity
- List of recent bot actions and events

### Options Page

The options page provides detailed configuration for all aspects of the bot:

#### Swiping Settings
- **Swipe Mode**: Choose between Automatic, Selective, or Manual
- **Swipe Rate**: Control how many profiles to swipe per hour
- **Like Ratio**: Set the percentage of profiles to like vs. pass
- **Swiping Schedule**: Configure when the bot should be active
- **Profile Preferences**: Set criteria for profiles to like

#### Messaging Settings
- **Auto Reply**: Configure automatic message responses
- **Reply Delay**: Set how long to wait before responding
- **Opening Messages**: Create templates for first messages
- **Follow-up Messages**: Create templates for follow-up messages

#### Filter Settings
- **Filter Mode**: Choose between Disabled, Flag Only, or Auto Filter
- **Filter Criteria**: Configure what patterns to detect in timewasters
- **Actions**: Set what actions to take when timewasters are detected

#### Account Settings
- **API URL**: Configure the backend connection
- **Notifications**: Control notification behavior
- **Data Management**: Export or clear local data

## Basic Workflow

### 1. Configure the Bot

Before starting, configure the bot settings:

1. Click "Settings" in the extension popup
2. Navigate to the "Swiping" tab
3. Configure your preferred swiping parameters:
   - Set "Swipe Rate" to a reasonable value (20-30/hour recommended)
   - Adjust "Like Ratio" based on your preferences
   - Configure "Swiping Schedule" to avoid detection

4. Navigate to the "Filters" tab
5. Configure timewaster detection:
   - Set "Filter Mode" to "Flag Only" initially
   - Adjust filter criteria based on your preferences

6. Click "Save Filter Settings"

### 2. Start Bumble in Your Browser

1. Open Chrome and navigate to `https://bumble.com/`
2. Log in to your Bumble account
3. Navigate to the swiping section

### 3. Start Auto-Swiping

1. Click the extension icon to open the popup
2. Click "Start Swiping"
3. The bot will begin swiping according to your settings
4. The status will change to "Active" and you'll see activity in the Recent Activity section

### 4. Monitor Progress

1. Check the extension popup periodically to monitor:
   - Number of matches
   - Swipe statistics
   - Recent activity

2. You can stop the bot at any time by clicking "Stop Swiping"

### 5. Review Matches and Conversations

1. Open Bumble in your browser
2. Navigate to the matches section
3. The extension will analyze conversations in the background
4. Check the "Filter" tab in settings to see which matches have been flagged as potential timewasters

## Advanced Features

### Managing Matches

The system helps you manage matches efficiently:

1. **Viewing Match Statistics**:
   - Open the extension options page
   - Navigate to the Stats section
   - View detailed statistics about your matches and conversations

2. **Filtering Timewasters**:
   - The system automatically analyzes conversations
   - Matches flagged as potential timewasters will be highlighted
   - You can review the analysis to make your own decision

3. **Bulk Actions**:
   - Select multiple matches
   - Apply actions like unmatch or deprioritize

### Customizing Message Templates

Create personalized message templates for different scenarios:

1. Navigate to the "Messaging" tab in options
2. Add new templates for:
   - Opening messages
   - Follow-up messages
   - Responses to common questions

3. Use variables in templates:
   - `{name}`: Match's name
   - `{interest}`: A shared interest if available
   - `{question}`: A question based on their profile

### Scheduling Bot Activity

Configure when the bot should be active:

1. Navigate to the "Swiping" tab in options
2. In the "Swiping Schedule" section:
   - Select active days
   - Set start and end times
   - Configure maximum daily actions

3. The bot will only operate during the specified times

## API Usage

For advanced users or developers, you can interact directly with the API:

### Authentication

```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin"
```

### Starting Auto-Swiping

```bash
curl -X POST "http://localhost:8000/api/v1/swipe/start" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "count": 50,
    "like_ratio": 0.7,
    "delay": 2
  }'
```

### Getting Match Information

```bash
curl -X GET "http://localhost:8000/api/v1/matches?page=1&page_size=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Analyzing Conversations

```bash
curl -X POST "http://localhost:8000/api/v1/messages/filter/all" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

For a complete API reference, see the [API Documentation](api_docs.md).

## Best Practices

### Avoiding Detection

To minimize the risk of being detected as a bot:

1. **Use Realistic Timing**:
   - Set reasonable swipe rates (20-30 per hour)
   - Configure natural delays between actions
   - Don't run the bot 24/7

2. **Vary Your Patterns**:
   - Change swipe ratios periodically
   - Don't use the exact same schedule every day
   - Mix automated and manual usage

3. **Use a Dedicated Profile**:
   - Configure a dedicated Chrome profile for the bot
   - This helps maintain login sessions and cookies

### Optimizing Match Quality

To improve the quality of your matches:

1. **Refine Your Filters**:
   - Adjust the timewaster detection parameters based on results
   - Review flagged conversations to improve accuracy

2. **Customize Like Criteria**:
   - Use the "Profile Preferences" settings to focus on quality matches
   - Prioritize verified profiles and those with complete bios

3. **Analyze Performance**:
   - Review match statistics regularly
   - Adjust settings based on what's working

### Managing Conversations

For effective conversation management:

1. **Prioritize Promising Matches**:
   - Focus on matches that show genuine engagement
   - Use the filter system to identify quality conversations

2. **Use Personalized Messages**:
   - Customize templates based on profile information
   - Avoid generic messages that appear automated

3. **Balance Automation and Personal Touch**:
   - Use automation for initial screening
   - Take over manually for matches you're interested in

## Troubleshooting

### Bot Not Swiping

If the bot isn't swiping properly:

1. Check that you're on the correct Bumble page (swiping section)
2. Verify the bot status is "Active" in the extension
3. Check for any error messages in the Recent Activity section
4. Try refreshing the Bumble page and restarting the bot

### Connection Issues

If the extension loses connection to the backend:

1. Verify the API server is still running
2. Check the API URL in the extension settings
3. Try logging out and back in to refresh the authentication token
4. Check for any network issues or firewall restrictions

### Inaccurate Timewaster Detection

If the timewaster detection isn't accurate:

1. Navigate to the "Filters" tab in options
2. Adjust the filter parameters:
   - Increase/decrease thresholds based on false positives/negatives
   - Add or remove red flag patterns
3. Save the settings and re-analyze conversations

## Future OpenAI API Integration

The system is designed for future integration with OpenAI's API, which will enable:

### Smart Message Generation

AI-generated responses based on:
- Conversation context
- Match's profile information
- Your communication style

To prepare for this integration:
1. Ensure your conversations are being properly analyzed
2. Begin collecting examples of successful conversations
3. Consider what aspects of messaging you'd like to automate

### Profile Analysis

Advanced profile evaluation using AI:
- Analyzing bio text for compatibility
- Evaluating photo content
- Identifying potential red flags

This will enhance the selective swiping mode by making more intelligent decisions.

### Implementation Notes

When OpenAI integration is available:
1. You'll need an OpenAI API key
2. Additional configuration options will be added to the settings
3. The system will include controls for AI-generated content review

## Conclusion

The Bumble Bot system provides powerful automation tools to enhance your dating experience. By following this guide and experimenting with different settings, you can optimize your results and save time while finding quality matches.

For technical details about the API endpoints, refer to the [API Documentation](api_docs.md).