# Bumble Bot API Usage Guide

This guide provides instructions for using the Bumble Bot API to automate Bumble interactions.

## Getting Started

### Authentication

Before using the API, you need to authenticate:

1. Obtain an access token:

```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin"
```

2. Use the token in subsequent requests:

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Basic Workflow

The typical workflow for using the Bumble Bot API is:

1. Configure the bot
2. Log in to Bumble
3. Start auto-swiping
4. Retrieve and analyze matches and conversations
5. Filter out timewasters

## Bot Configuration

Configure the bot before starting:

```bash
curl -X POST "http://localhost:8000/api/v1/swipe/configure" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "headless": true,
    "profile_path": "/path/to/chrome/profile"
  }'
```

## Logging In

### Login with Facebook

```bash
curl -X POST "http://localhost:8000/api/v1/swipe/login/facebook" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your_email@example.com",
    "password": "your_password"
  }'
```

### Login with Phone Number

```bash
curl -X POST "http://localhost:8000/api/v1/swipe/login/phone" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1234567890"
  }'
```

## Auto-Swiping

### Start Auto-Swiping

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

### Check Swiping Status

```bash
curl -X GET "http://localhost:8000/api/v1/swipe/status" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Stop Auto-Swiping

```bash
curl -X POST "http://localhost:8000/api/v1/swipe/stop" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Managing Matches

### Get All Matches

```bash
curl -X GET "http://localhost:8000/api/v1/matches?page=1&page_size=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Match Details

```bash
curl -X GET "http://localhost:8000/api/v1/matches/match1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Conversation with Match

```bash
curl -X GET "http://localhost:8000/api/v1/matches/match1/conversation" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Send Message to Match

```bash
curl -X POST "http://localhost:8000/api/v1/matches/match1/message" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hey, how are you doing?"
  }'
```

### Unmatch

```bash
curl -X DELETE "http://localhost:8000/api/v1/matches/match1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Message Filtering and Analysis

### Get All Messages

```bash
curl -X GET "http://localhost:8000/api/v1/messages/all" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Filter a Conversation

```bash
curl -X POST "http://localhost:8000/api/v1/messages/filter" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "match_id": "match1",
    "match_name": "Emma",
    "messages": [
      {
        "content": "Hey there!",
        "timestamp": 1620984600,
        "sender": "match"
      },
      {
        "content": "Hi! How are you?",
        "timestamp": 1620984900,
        "sender": "user"
      },
      {
        "content": "I am good, thanks! What do you do for fun?",
        "timestamp": 1620985200,
        "sender": "match"
      }
    ]
  }'
```

### Analyze a Conversation

```bash
curl -X POST "http://localhost:8000/api/v1/messages/analyze" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "match_id": "match1",
    "match_name": "Emma",
    "messages": [
      {
        "content": "Hey there!",
        "timestamp": 1620984600,
        "sender": "match"
      },
      {
        "content": "Hi! How are you?",
        "timestamp": 1620984900,
        "sender": "user"
      },
      {
        "content": "I am good, thanks! What do you do for fun?",
        "timestamp": 1620985200,
        "sender": "match"
      }
    ]
  }'
```

### Filter All Conversations

```bash
curl -X POST "http://localhost:8000/api/v1/messages/filter/all" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Filter Configuration

### Get Current Filter Configuration

```bash
curl -X GET "http://localhost:8000/api/v1/messages/filter/config" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Update Filter Configuration

```bash
curl -X POST "http://localhost:8000/api/v1/messages/filter/config" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "min_message_length": 5,
    "max_response_time": 86400,
    "min_engagement_score": 0.5,
    "min_question_ratio": 0.2,
    "max_one_word_ratio": 0.5,
    "red_flag_patterns": [
      "(?i)instagram",
      "(?i)snapchat",
      "(?i)follow me"
    ]
  }'
```

## Best Practices

1. **Session Management**: Keep your authentication token secure and refresh it regularly.

2. **Rate Limiting**: Avoid making too many requests in a short period to prevent detection.

3. **Browser Profile**: Use a dedicated Chrome profile for the bot to maintain login sessions.

4. **Headless Mode**: Use headless mode (`"headless": true`) for production, but set it to `false` for debugging.

5. **Filter Tuning**: Adjust the filter configuration based on your experience to better identify timewasters.

6. **Regular Monitoring**: Check the bot's status regularly to ensure it's functioning correctly.

7. **Error Handling**: Implement proper error handling in your client application to handle API errors gracefully.

## Troubleshooting

### API Connection Issues

If you can't connect to the API:
- Verify the API server is running
- Check your network connection
- Ensure the correct host and port are being used

### Authentication Errors

If you receive 401 Unauthorized errors:
- Your token may have expired; request a new one
- Ensure you're including the token correctly in the Authorization header

### Bot Operation Issues

If the bot isn't working as expected:
- Check the API logs for errors
- Verify your Chrome installation and webdriver
- Try running the bot with `"headless": false` to see what's happening

## Further Resources

For more detailed information, refer to:
- [API Documentation](api_docs.md)
- [Installation Guide](installation.md)