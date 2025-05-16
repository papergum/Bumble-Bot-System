"""
Message content analysis for Bumble automation.
This module provides functionality to analyze message content and detect patterns.
"""

import re
import string
import logging
from typing import List, Dict, Any, Tuple
from collections import Counter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MessageAnalyzer:
    """
    Analyzes message content to detect patterns and extract insights.
    """
    
    def __init__(self, config=None):
        """
        Initialize the message analyzer.
        
        Args:
            config (dict, optional): Configuration for the analyzer
        """
        self.config = config or {}
        
        # Common filler words that don't add much value
        self.filler_words = self.config.get('filler_words', [
            'um', 'uh', 'like', 'so', 'yeah', 'just', 'lol', 'haha', 'ok', 'okay'
        ])
        
        # Positive engagement indicators
        self.engagement_indicators = self.config.get('engagement_indicators', [
            r'\?',                      # Questions
            r'(?i)what do you think',   # Asking for opinion
            r'(?i)tell me more',        # Showing interest
            r'(?i)how about you',       # Reciprocating
            r'(?i)that\'s interesting'  # Showing engagement
        ])
        
        # Compile regex patterns
        self.engagement_patterns = [re.compile(pattern) for pattern in self.engagement_indicators]
        
        # Placeholder for future NLP model integration
        self.nlp_model = None
        
    def analyze_message(self, message: str) -> Dict[str, Any]:
        """
        Analyze a single message.
        
        Args:
            message (str): Message content
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        if not message:
            return {'length': 0, 'engagement_score': 0, 'sentiment': 'neutral'}
            
        # Basic metrics
        word_count = len(message.split())
        char_count = len(message)
        
        # Check for engagement indicators
        engagement_count = sum(1 for pattern in self.engagement_patterns if pattern.search(message))
        
        # Calculate engagement score (0-1)
        engagement_score = min(1.0, engagement_count / 2)  # Cap at 1.0
        
        # Simple sentiment analysis
        # This is a placeholder for more sophisticated sentiment analysis
        sentiment = self._simple_sentiment(message)
        
        # Check for filler content
        filler_count = sum(1 for word in message.lower().split() if word in self.filler_words)
        filler_ratio = filler_count / word_count if word_count > 0 else 0
        
        # Prepare result
        result = {
            'length': word_count,
            'char_count': char_count,
            'engagement_score': engagement_score,
            'sentiment': sentiment,
            'filler_ratio': filler_ratio,
            'has_question': '?' in message,
            'has_url': bool(re.search(r'https?://\S+', message)),
            'has_emoji': bool(re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]', message))
        }
        
        return result
        
    def analyze_conversation(self, messages: List[str]) -> Dict[str, Any]:
        """
        Analyze a full conversation.
        
        Args:
            messages (List[str]): List of messages in the conversation
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        if not messages:
            return {'message_count': 0, 'avg_length': 0, 'overall_engagement': 0}
            
        # Analyze individual messages
        message_analyses = [self.analyze_message(message) for message in messages]
        
        # Calculate conversation-level metrics
        avg_length = sum(analysis['length'] for analysis in message_analyses) / len(message_analyses)
        avg_engagement = sum(analysis['engagement_score'] for analysis in message_analyses) / len(message_analyses)
        
        # Count sentiment distribution
        sentiment_counts = Counter(analysis['sentiment'] for analysis in message_analyses)
        
        # Calculate question ratio
        question_count = sum(1 for analysis in message_analyses if analysis['has_question'])
        question_ratio = question_count / len(message_analyses)
        
        # Analyze conversation flow
        flow_score = self._analyze_conversation_flow(messages)
        
        # Identify common topics
        topics = self._extract_topics(messages)
        
        # Prepare result
        result = {
            'message_count': len(messages),
            'avg_length': avg_length,
            'overall_engagement': avg_engagement,
            'sentiment_distribution': dict(sentiment_counts),
            'question_ratio': question_ratio,
            'flow_score': flow_score,
            'topics': topics
        }
        
        return result
        
    def detect_intent(self, message: str) -> str:
        """
        Detect the intent of a message.
        
        Args:
            message (str): Message content
            
        Returns:
            str: Detected intent
        """
        # This is a simple implementation and could be enhanced with ML
        message = message.lower()
        
        # Check for common intents
        if '?' in message:
            return 'question'
        elif any(word in message for word in ['hi', 'hello', 'hey', 'sup']):
            return 'greeting'
        elif any(word in message for word in ['bye', 'goodbye', 'see you', 'talk later']):
            return 'farewell'
        elif any(word in message for word in ['thanks', 'thank you', 'appreciate']):
            return 'gratitude'
        elif any(pattern.search(message) for pattern in [
            re.compile(r'(?i)what are you doing'),
            re.compile(r'(?i)how are you'),
            re.compile(r'(?i)how\'s your day')
        ]):
            return 'small_talk'
        elif any(pattern.search(message) for pattern in [
            re.compile(r'(?i)meet up'),
            re.compile(r'(?i)get together'),
            re.compile(r'(?i)coffee'),
            re.compile(r'(?i)drink'),
            re.compile(r'(?i)dinner')
        ]):
            return 'date_request'
        elif any(pattern.search(message) for pattern in [
            re.compile(r'(?i)number'),
            re.compile(r'(?i)instagram'),
            re.compile(r'(?i)snapchat'),
            re.compile(r'(?i)contact')
        ]):
            return 'contact_request'
        else:
            return 'general'
            
    def prepare_for_openai(self, conversation: List[str]) -> Dict[str, Any]:
        """
        Prepare conversation data for OpenAI API integration.
        
        Args:
            conversation (List[str]): List of messages in the conversation
            
        Returns:
            Dict[str, Any]: Prepared data for OpenAI
        """
        # This is a placeholder for future OpenAI API integration
        # The actual implementation would depend on the OpenAI API requirements
        
        # Basic conversation analysis
        analysis = self.analyze_conversation(conversation)
        
        # Extract key conversation features
        prepared_data = {
            'messages': conversation,
            'message_count': len(conversation),
            'avg_message_length': analysis['avg_length'],
            'engagement_level': analysis['overall_engagement'],
            'topics': analysis['topics']
        }
        
        return prepared_data
        
    def _simple_sentiment(self, message: str) -> str:
        """
        Perform simple sentiment analysis on a message.
        
        Args:
            message (str): Message content
            
        Returns:
            str: Sentiment ('positive', 'negative', or 'neutral')
        """
        # This is a very simple implementation
        # In a production system, this would be replaced with a proper NLP model
        
        message = message.lower()
        
        # Simple positive and negative word lists
        positive_words = [
            'good', 'great', 'awesome', 'amazing', 'love', 'happy', 'excited',
            'thanks', 'thank', 'cool', 'nice', 'fun', 'enjoy', 'like', 'glad'
        ]
        
        negative_words = [
            'bad', 'terrible', 'awful', 'hate', 'sad', 'upset', 'angry',
            'annoyed', 'disappointed', 'sorry', 'unfortunate', 'boring'
        ]
        
        # Count positive and negative words
        positive_count = sum(1 for word in message.split() if word.strip(string.punctuation) in positive_words)
        negative_count = sum(1 for word in message.split() if word.strip(string.punctuation) in negative_words)
        
        # Determine sentiment
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
            
    def _analyze_conversation_flow(self, messages: List[str]) -> float:
        """
        Analyze the flow of a conversation.
        
        Args:
            messages (List[str]): List of messages
            
        Returns:
            float: Flow score (0-1)
        """
        if len(messages) < 3:
            return 0.5  # Not enough messages to analyze flow
            
        # Calculate message length variance
        lengths = [len(message) for message in messages]
        avg_length = sum(lengths) / len(lengths)
        variance = sum((length - avg_length) ** 2 for length in lengths) / len(lengths)
        
        # Some variance is good (indicates dynamic conversation)
        # But too much variance might indicate disjointed conversation
        normalized_variance = min(1.0, variance / 1000)  # Cap at 1.0
        
        # Check for conversation continuity
        continuity_score = 0
        for i in range(1, len(messages)):
            prev_words = set(messages[i-1].lower().split())
            curr_words = set(messages[i].lower().split())
            
            # Check for word overlap (indicates topic continuity)
            overlap = len(prev_words.intersection(curr_words))
            if overlap > 0:
                continuity_score += 1
                
        continuity_ratio = continuity_score / (len(messages) - 1) if len(messages) > 1 else 0
        
        # Combine metrics
        flow_score = (0.7 * continuity_ratio + 0.3 * (1 - normalized_variance))
        
        return flow_score
        
    def _extract_topics(self, messages: List[str]) -> List[str]:
        """
        Extract common topics from a conversation.
        
        Args:
            messages (List[str]): List of messages
            
        Returns:
            List[str]: List of identified topics
        """
        # This is a simple implementation
        # In a production system, this would use more sophisticated NLP techniques
        
        # Combine all messages
        all_text = ' '.join(messages).lower()
        
        # Remove punctuation and split into words
        translator = str.maketrans('', '', string.punctuation)
        words = all_text.translate(translator).split()
        
        # Remove common stop words
        stop_words = [
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 
            'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 
            'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 
            'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 
            'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 
            'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 
            'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 
            'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 
            'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
            'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 
            'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 
            'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
            'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 
            't', 'can', 'will', 'just', 'don', 'should', 'now'
        ]
        
        filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Count word frequencies
        word_counts = Counter(filtered_words)
        
        # Get most common words as topics
        topics = [word for word, count in word_counts.most_common(5) if count > 1]
        
        return topics