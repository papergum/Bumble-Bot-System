# Bumble Bot API Documentation

This document provides detailed information about the Bumble Bot REST API endpoints, request/response formats, and authentication.

## Base URL

All API endpoints are prefixed with `/api/v1`.

## Authentication

The API uses JWT (JSON Web Token) authentication.

### Obtaining a Token

```
POST /api/v1/auth/token
```

**Request Body:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
}
```

### Using the Token

Include the token in the `Authorization` header of all API requests:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Endpoints

### Authentication

#### Get Current User

```
GET /api/v1/auth/me
```

**Response:**
```json
{
  "status": "success",
  "message": "User details retrieved successfully",
  "data": {
    "username": "admin"
  }
}
```

#### Logout

```
POST /api/v1/auth/logout
```

**Response:**
```json
{
  "status": "success",
  "message": "Logout successful"
}
```

### Swiping

#### Start Auto-Swiping

```
POST /api/v1/swipe/start
```

**Request Body:**
```json
{
  "count": 50,
  "like_ratio": 0.7,
  "delay": 2
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Auto-swipe started",
  "data": {
    "config": {
      "count": 50,
      "like_ratio": 0.7,
      "delay": 2
    }
  }
}
```

#### Stop Auto-Swiping

```
POST /api/v1/swipe/stop
```

**Response:**
```json
{
  "status": "success",
  "message": "Auto-swipe stopped"
}
```

#### Get Swipe Status

```
GET /api/v1/swipe/status
```

**Response:**
```json
{
  "status": "success",
  "message": "Swipe status retrieved",
  "data": {
    "is_running": false,
    "total_swipes": 50,
    "likes": 35,
    "passes": 15,
    "remaining": 0,
    "config": {
      "count": 50,
      "like_ratio": 0.7,
      "delay": 2
    }
  }
}
```

#### Configure Bot

```
POST /api/v1/swipe/configure
```

**Request Body:**
```json
{
  "headless": true,
  "profile_path": "/path/to/chrome/profile"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Bot configured successfully",
  "data": {
    "config": {
      "headless": true,
      "profile_path": "/path/to/chrome/profile"
    }
  }
}
```

#### Login with Facebook

```
POST /api/v1/swipe/login/facebook
```

**Request Body:**
```json
{
  "email": "your_email@example.com",
  "password": "your_password"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Logged in with Facebook successfully"
}
```

#### Login with Phone

```
POST /api/v1/swipe/login/phone
```

**Request Body:**
```json
{
  "phone_number": "+1234567890"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Phone login initiated successfully"
}
```

### Matches

#### Get All Matches

```
GET /api/v1/matches?page=1&page_size=10
```

**Response:**
```json
{
  "status": "success",
  "message": "Matches retrieved successfully",
  "data": [
    {
      "id": "match1",
      "name": "Emma",
      "age": 28,
      "bio": "Love hiking and photography",
      "distance": "5 miles away",
      "photos": ["photo1.jpg", "photo2.jpg"],
      "last_active": "2 hours ago",
      "is_new": true
    },
    {
      "id": "match2",
      "name": "Olivia",
      "age": 26,
      "bio": "Foodie and travel enthusiast",
      "distance": "10 miles away",
      "photos": ["photo3.jpg"],
      "last_active": "1 day ago",
      "is_new": false
    }
  ],
  "pagination": {
    "total": 2,
    "page": 1,
    "page_size": 10,
    "total_pages": 1
  }
}
```

#### Get Match Details

```
GET /api/v1/matches/{match_id}
```

**Response:**
```json
{
  "status": "success",
  "message": "Match details retrieved successfully",
  "data": {
    "id": "match1",
    "name": "Emma",
    "age": 28,
    "bio": "Love hiking and photography",
    "distance": "5 miles away",
    "photos": ["photo1.jpg", "photo2.jpg"],
    "last_active": "2 hours ago",
    "is_new": true
  }
}
```

#### Unmatch

```
DELETE /api/v1/matches/{match_id}
```

**Response:**
```json
{
  "status": "success",
  "message": "Successfully unmatched with ID match1"
}
```

#### Get Conversation

```
GET /api/v1/matches/{match_id}/conversation
```

**Response:**
```json
{
  "status": "success",
  "message": "Conversation retrieved successfully",
  "data": {
    "messages": [
      {
        "sender": "match",
        "message": "Hey there!",
        "timestamp": "2023-05-14T10:30:00Z"
      },
      {
        "sender": "user",
        "message": "Hi! How are you?",
        "timestamp": "2023-05-14T10:35:00Z"
      },
      {
        "sender": "match",
        "message": "I'm good, thanks! What do you do for fun?",
        "timestamp": "2023-05-14T10:40:00Z"
      }
    ]
  }
}
```

#### Send Message

```
POST /api/v1/matches/{match_id}/message
```

**Request Body:**
```json
{
  "message": "Hey, how's your day going?"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Message sent successfully to match match1"
}
```

### Messages

#### Get All Messages

```
GET /api/v1/messages/all
```

**Response:**
```json
{
  "status": "success",
  "message": "All messages retrieved successfully",
  "data": {
    "conversations": {
      "match1": {
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
            "content": "I'm good, thanks! What do you do for fun?",
            "timestamp": 1620985200,
            "sender": "match"
          }
        ]
      },
      "match2": {
        "match_id": "match2",
        "match_name": "Olivia",
        "messages": [
          {
            "content": "Hello!",
            "timestamp": 1620984000,
            "sender": "match"
          },
          {
            "content": "Hey, nice to meet you!",
            "timestamp": 1620984300,
            "sender": "user"
          },
          {
            "content": "Likewise! What brings you to Bumble?",
            "timestamp": 1620984600,
            "sender": "match"
          }
        ]
      }
    }
  }
}
```

#### Filter Conversation

```
POST /api/v1/messages/filter
```

**Request Body:**
```json
{
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
      "content": "I'm good, thanks! What do you do for fun?",
      "timestamp": 1620985200,
      "sender": "match"
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Conversation filtered successfully",
  "data": {
    "is_timewaster": false,
    "confidence": 0.2,
    "overall_score": 0.8,
    "content_score": 0.85,
    "pattern_score": 0.9,
    "time_score": 0.7,
    "flags": [],
    "reason": "Sufficient engagement"
  }
}
```

#### Analyze Conversation

```
POST /api/v1/messages/analyze
```

**Request Body:**
```json
{
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
      "content": "I'm good, thanks! What do you do for fun?",
      "timestamp": 1620985200,
      "sender": "match"
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Conversation analyzed successfully",
  "data": {
    "message_count": 3,
    "avg_length": 5.33,
    "overall_engagement": 0.75,
    "sentiment_distribution": {
      "positive": 2,
      "neutral": 1,
      "negative": 0
    },
    "question_ratio": 0.67,
    "flow_score": 0.8,
    "topics": ["fun"]
  }
}
```

#### Update Filter Configuration

```
POST /api/v1/messages/filter/config
```

**Request Body:**
```json
{
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
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Filter configuration updated successfully",
  "data": {
    "config": {
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
    }
  }
}
```

#### Get Filter Configuration

```
GET /api/v1/messages/filter/config
```

**Response:**
```json
{
  "status": "success",
  "message": "Filter configuration retrieved successfully",
  "data": {
    "config": {
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
}
```

#### Filter All Conversations

```
POST /api/v1/messages/filter/all
```

**Response:**
```json
{
  "status": "success",
  "message": "All conversations filtered successfully",
  "data": {
    "results": {
      "Emma": {
        "is_timewaster": false,
        "confidence": 0.2,
        "overall_score": 0.8,
        "content_score": 0.85,
        "pattern_score": 0.9,
        "time_score": 0.7,
        "flags": [],
        "reason": "Sufficient engagement"
      },
      "Olivia": {
        "is_timewaster": false,
        "confidence": 0.15,
        "overall_score": 0.85,
        "content_score": 0.9,
        "pattern_score": 0.85,
        "time_score": 0.75,
        "flags": [],
        "reason": "Sufficient engagement"
      }
    }
  }
}
```

## Error Responses

All endpoints return a standardized error response format:

```json
{
  "status": "error",
  "message": "Error message",
  "errors": [
    {
      "loc": ["field_name"],
      "msg": "Detailed error message"
    }
  ]
}
```

Common HTTP status codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error