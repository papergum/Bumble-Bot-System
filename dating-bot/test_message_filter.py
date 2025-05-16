"""
Test script for the message filtering functionality of the Bumble Bot.

This script tests the timewaster detection logic to ensure it correctly
identifies low-quality conversations based on various criteria.
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the backend directory to the path so we can import the message filter
backend_path = Path("backend").absolute()
sys.path.append(str(backend_path))

# Import the message filter
try:
    from src.message_filter.filter import TimewasterFilter
except ImportError as e:
    logger.error(f"Failed to import TimewasterFilter: {e}")
    sys.exit(1)

def load_config():
    """Load the message filter configuration."""
    config_path = Path("backend/config/default_settings.json").absolute()
    
    try:
        with open(config_path, "r") as f:
            settings = json.load(f)
            return settings.get("message_filter", {})
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Failed to load configuration: {e}")
        return {}

def generate_test_conversations():
    """Generate test conversations with different characteristics."""
    # Current time for timestamps
    now = datetime.now()
    
    # Test conversations
    conversations = {
        # High-quality conversation with good engagement
        "good_conversation": {
            "messages": [
                "Hey there! I really liked your profile. What do you enjoy doing on weekends?",
                "Hi! Thanks for the message. I usually go hiking or try new restaurants. How about you?",
                "That sounds fun! I'm into photography and exploring new places. Have you been to any good restaurants lately?",
                "Yes! I tried this new Italian place downtown last week. The pasta was amazing. Do you like Italian food?",
                "I love Italian food! What's the name of the place? I'd like to check it out sometime.",
                "It's called Bella Vita on Main Street. Maybe we could go there together sometime?",
                "That sounds like a great idea! I'd enjoy that. When are you usually free?"
            ],
            "timestamps": [
                int((now - timedelta(days=2, hours=3)).timestamp()),
                int((now - timedelta(days=2, hours=2, minutes=45)).timestamp()),
                int((now - timedelta(days=2, hours=2, minutes=30)).timestamp()),
                int((now - timedelta(days=2, hours=2)).timestamp()),
                int((now - timedelta(days=1, hours=5)).timestamp()),
                int((now - timedelta(days=1, hours=4)).timestamp()),
                int((now - timedelta(hours=2)).timestamp())
            ]
        },
        
        # Low-quality conversation with short responses
        "short_responses": {
            "messages": [
                "Hey how are you doing today?",
                "good",
                "What do you like to do for fun?",
                "stuff",
                "Any hobbies or interests?",
                "yeah",
                "What kind of hobbies?",
                "idk",
                "Do you want to meet up sometime?",
                "maybe"
            ],
            "timestamps": [
                int((now - timedelta(days=1, hours=5)).timestamp()),
                int((now - timedelta(days=1, hours=4)).timestamp()),
                int((now - timedelta(days=1, hours=3)).timestamp()),
                int((now - timedelta(days=1, hours=2)).timestamp()),
                int((now - timedelta(days=1, hours=1)).timestamp()),
                int((now - timedelta(days=1)).timestamp()),
                int((now - timedelta(hours=23)).timestamp()),
                int((now - timedelta(hours=22)).timestamp()),
                int((now - timedelta(hours=21)).timestamp()),
                int((now - timedelta(hours=20)).timestamp())
            ]
        },
        
        # Conversation with red flags
        "red_flags": {
            "messages": [
                "Hey there, you look great in your photos!",
                "Thanks! You too!",
                "I'm not on here much. Follow me on Instagram @model_lifestyle",
                "Oh, what kind of content do you post there?",
                "Mostly travel and lifestyle. I have way more photos there. Check my bio for the link.",
                "I'd rather chat here first if that's okay.",
                "Sure, but I'm not very active here. If you want to see more of me, my Instagram is better."
            ],
            "timestamps": [
                int((now - timedelta(days=3, hours=12)).timestamp()),
                int((now - timedelta(days=3, hours=11)).timestamp()),
                int((now - timedelta(days=3, hours=10)).timestamp()),
                int((now - timedelta(days=2, hours=15)).timestamp()),
                int((now - timedelta(days=2, hours=14)).timestamp()),
                int((now - timedelta(days=2, hours=13)).timestamp()),
                int((now - timedelta(days=2, hours=12)).timestamp())
            ]
        },
        
        # Conversation with slow responses
        "slow_responses": {
            "messages": [
                "Hi there! How's your week going?",
                "It's going well, thanks for asking. How about yours?",
                "Pretty busy with work but looking forward to the weekend. Any plans?",
                "Not much, probably just relaxing at home. You?",
                "Thinking of going hiking if the weather's nice. Do you enjoy outdoor activities?"
            ],
            "timestamps": [
                int((now - timedelta(days=14)).timestamp()),
                int((now - timedelta(days=12)).timestamp()),
                int((now - timedelta(days=10)).timestamp()),
                int((now - timedelta(days=7)).timestamp()),
                int((now - timedelta(days=5)).timestamp())
            ]
        },
        
        # Conversation with potential scam indicators
        "potential_scam": {
            "messages": [
                "Hello handsome, how are you today?",
                "I'm good, thanks! How about you?",
                "I'm great! I just moved here and looking to meet new people.",
                "Oh cool, where did you move from?",
                "I moved from overseas. I'm a model but also starting a business. Do you want to support me on Venmo?",
                "Uh, I'd rather get to know you first.",
                "Sure, check my profile for more pics or send me money at cashapp $modelname"
            ],
            "timestamps": [
                int((now - timedelta(days=1, hours=8)).timestamp()),
                int((now - timedelta(days=1, hours=7, minutes=50)).timestamp()),
                int((now - timedelta(days=1, hours=7, minutes=40)).timestamp()),
                int((now - timedelta(days=1, hours=7, minutes=30)).timestamp()),
                int((now - timedelta(days=1, hours=7, minutes=20)).timestamp()),
                int((now - timedelta(days=1, hours=7, minutes=10)).timestamp()),
                int((now - timedelta(days=1, hours=7)).timestamp())
            ]
        }
    }
    
    return conversations

def test_message_filter():
    """Test the message filter functionality."""
    logger.info("Testing message filter functionality")
    
    # Load configuration
    config = load_config()
    logger.info(f"Loaded configuration: {json.dumps(config, indent=2)}")
    
    # Create filter instance
    message_filter = TimewasterFilter(config)
    
    # Generate test conversations
    conversations = generate_test_conversations()
    
    # Test results
    results = {}
    
    # Test each conversation
    for name, conversation in conversations.items():
        logger.info(f"Testing conversation: {name}")
        
        # Analyze the conversation
        result = message_filter.analyze_conversation(
            conversation["messages"],
            conversation["timestamps"]
        )
        
        # Store the result
        results[name] = result
        
        # Log the result
        logger.info(f"Result for {name}: is_timewaster={result['is_timewaster']}, confidence={result['confidence']:.2f}")
        logger.info(f"Flags: {result['flags']}")
    
    # Print summary
    print("\n" + "="*50)
    print("MESSAGE FILTER TEST RESULTS")
    print("="*50)
    
    for name, result in results.items():
        status = "❌ TIMEWASTER" if result["is_timewaster"] else "✅ QUALITY MATCH"
        print(f"\n{name}: {status}")
        print(f"  Confidence: {result['confidence']:.2f}")
        print(f"  Overall Score: {result['overall_score']:.2f}")
        print(f"  Content Score: {result['content_score']:.2f}")
        print(f"  Pattern Score: {result['pattern_score']:.2f}")
        print(f"  Time Score: {result['time_score']:.2f}")
        
        if result["flags"]:
            print("  Flags:")
            for flag in result["flags"]:
                print(f"    - {flag}")
    
    print("\n" + "="*50)
    
    # Verify expected outcomes
    expected_outcomes = {
        "good_conversation": False,  # Not a timewaster
        "short_responses": True,     # Is a timewaster
        "red_flags": True,           # Is a timewaster
        "slow_responses": True,      # Is a timewaster
        "potential_scam": True       # Is a timewaster
    }
    
    all_passed = True
    for name, expected in expected_outcomes.items():
        actual = results[name]["is_timewaster"]
        if actual == expected:
            print(f"✅ {name}: Correctly identified as {'timewaster' if expected else 'quality match'}")
        else:
            print(f"❌ {name}: Incorrectly identified as {'timewaster' if actual else 'quality match'} (expected {'timewaster' if expected else 'quality match'})")
            all_passed = False
    
    if all_passed:
        print("\n✅ All tests passed! The message filter is working correctly.")
    else:
        print("\n❌ Some tests failed. The message filter may need adjustment.")

if __name__ == "__main__":
    test_message_filter()