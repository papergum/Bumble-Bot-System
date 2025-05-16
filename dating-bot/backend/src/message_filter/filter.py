"""
Timewaster detection logic for Bumble automation.
This module provides functionality to filter out matches based on message content.
"""

import re
import logging
from typing import List, Dict, Any, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TimewasterFilter:
    """
    Detects potential timewasters in Bumble conversations.
    """
    
    def __init__(self, config=None):
        """
        Initialize the timewaster filter.
        
        Args:
            config (dict, optional): Configuration for the filter
        """
        self.config = config or {}
        
        # Default thresholds
        self.thresholds = {
            'min_message_length': self.config.get('min_message_length', 5),
            'max_response_time': self.config.get('max_response_time', 24 * 60 * 60),  # 24 hours in seconds
            'min_engagement_score': self.config.get('min_engagement_score', 0.5),
            'min_question_ratio': self.config.get('min_question_ratio', 0.2),
            'max_one_word_ratio': self.config.get('max_one_word_ratio', 0.5)
        }
        
        # Red flag patterns
        self.red_flag_patterns = self.config.get('red_flag_patterns', [
            r'(?i)instagram',
            r'(?i)snapchat',
            r'(?i)follow me',
            r'(?i)my profile',
            r'(?i)venmo',
            r'(?i)cashapp',
            r'(?i)paypal',
            r'(?i)send money',
            r'(?i)not here often',
            r'(?i)check my bio'
        ])
        
        # Compile regex patterns
        self.compiled_patterns = [re.compile(pattern) for pattern in self.red_flag_patterns]
        
    def analyze_conversation(self, messages: List[str], timestamps: List[int] = None) -> Dict[str, Any]:
        """
        Analyze a conversation to determine if it's a potential timewaster.
        
        Args:
            messages (List[str]): List of messages in the conversation
            timestamps (List[int], optional): List of message timestamps
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        if not messages:
            return {'is_timewaster': False, 'confidence': 0, 'reason': 'No messages to analyze'}
            
        # Analyze message content
        content_score, content_flags = self._analyze_content(messages)
        
        # Analyze message patterns
        pattern_score, pattern_flags = self._analyze_patterns(messages)
        
        # Analyze response times if timestamps are provided
        time_score, time_flags = self._analyze_response_times(timestamps) if timestamps else (1.0, [])
        
        # Calculate overall score
        # Weight factors can be adjusted based on importance
        weights = {'content': 0.4, 'pattern': 0.4, 'time': 0.2}
        overall_score = (
            content_score * weights['content'] +
            pattern_score * weights['pattern'] +
            time_score * weights['time']
        )
        
        # Determine if it's a timewaster
        is_timewaster = overall_score < self.thresholds['min_engagement_score']
        
        # Combine all flags
        all_flags = content_flags + pattern_flags + time_flags
        
        # Determine confidence level
        confidence = 1.0 - overall_score if is_timewaster else overall_score
        
        # Prepare result
        result = {
            'is_timewaster': is_timewaster,
            'confidence': confidence,
            'overall_score': overall_score,
            'content_score': content_score,
            'pattern_score': pattern_score,
            'time_score': time_score,
            'flags': all_flags,
            'reason': 'Low engagement detected' if is_timewaster else 'Sufficient engagement'
        }
        
        return result
        
    def filter_conversations(self, conversations: Dict[str, List[str]]) -> Dict[str, Dict[str, Any]]:
        """
        Filter multiple conversations to identify potential timewasters.
        
        Args:
            conversations (Dict[str, List[str]]): Dictionary of conversations with match names as keys
            
        Returns:
            Dict[str, Dict[str, Any]]: Analysis results for each conversation
        """
        results = {}
        
        for match_name, messages in conversations.items():
            logger.info(f"Analyzing conversation with {match_name}")
            result = self.analyze_conversation(messages)
            results[match_name] = result
            
            if result['is_timewaster']:
                logger.info(f"{match_name} identified as potential timewaster (confidence: {result['confidence']:.2f})")
            else:
                logger.info(f"{match_name} appears to be engaged (score: {result['overall_score']:.2f})")
                
        return results
        
    def _analyze_content(self, messages: List[str]) -> Tuple[float, List[str]]:
        """
        Analyze message content for potential timewaster indicators.
        
        Args:
            messages (List[str]): List of messages
            
        Returns:
            Tuple[float, List[str]]: Content score and list of flags
        """
        flags = []
        
        # Check for red flag patterns
        red_flag_count = 0
        for message in messages:
            for pattern in self.compiled_patterns:
                if pattern.search(message):
                    red_flag_count += 1
                    match = pattern.search(message).group()
                    flags.append(f"Contains potential red flag: '{match}'")
                    
        # Calculate average message length
        message_lengths = [len(message.split()) for message in messages]
        avg_message_length = sum(message_lengths) / len(messages) if messages else 0
        
        if avg_message_length < self.thresholds['min_message_length']:
            flags.append(f"Short messages (avg {avg_message_length:.1f} words)")
            
        # Calculate one-word message ratio
        one_word_messages = sum(1 for length in message_lengths if length <= 1)
        one_word_ratio = one_word_messages / len(messages) if messages else 0
        
        if one_word_ratio > self.thresholds['max_one_word_ratio']:
            flags.append(f"High ratio of one-word responses ({one_word_ratio:.1%})")
            
        # Calculate question ratio (engagement indicator)
        questions = sum(1 for message in messages if '?' in message)
        question_ratio = questions / len(messages) if messages else 0
        
        if question_ratio < self.thresholds['min_question_ratio']:
            flags.append(f"Low question ratio ({question_ratio:.1%})")
            
        # Calculate content score
        # Higher score is better (less likely to be a timewaster)
        red_flag_factor = max(0, 1 - (red_flag_count / len(messages) * 2)) if messages else 0
        length_factor = min(1, avg_message_length / self.thresholds['min_message_length'])
        one_word_factor = 1 - (one_word_ratio / self.thresholds['max_one_word_ratio'])
        question_factor = min(1, question_ratio / self.thresholds['min_question_ratio'])
        
        # Combine factors with weights
        content_score = (
            red_flag_factor * 0.4 +
            length_factor * 0.3 +
            one_word_factor * 0.2 +
            question_factor * 0.1
        )
        
        return content_score, flags
        
    def _analyze_patterns(self, messages: List[str]) -> Tuple[float, List[str]]:
        """
        Analyze message patterns for potential timewaster indicators.
        
        Args:
            messages (List[str]): List of messages
            
        Returns:
            Tuple[float, List[str]]: Pattern score and list of flags
        """
        flags = []
        
        # Not enough messages to analyze patterns
        if len(messages) < 3:
            return 0.5, []
            
        # Check for repetitive messages
        unique_messages = set(messages)
        repetition_ratio = len(unique_messages) / len(messages)
        
        if repetition_ratio < 0.7:  # More than 30% repetition
            flags.append(f"High message repetition ({(1-repetition_ratio):.1%} repeated)")
            
        # Check for conversation flow
        # This is a simple implementation and could be enhanced
        response_lengths = [len(message) for message in messages]
        length_variance = sum(abs(response_lengths[i] - response_lengths[i-1]) 
                             for i in range(1, len(response_lengths))) / (len(response_lengths) - 1)
        
        if length_variance < 10:  # Low variance in message length
            flags.append("Low variance in message length")
            
        # Calculate pattern score
        pattern_score = (repetition_ratio * 0.7 + min(1, length_variance / 20) * 0.3)
        
        return pattern_score, flags
        
    def _analyze_response_times(self, timestamps: List[int]) -> Tuple[float, List[str]]:
        """
        Analyze response times for potential timewaster indicators.
        
        Args:
            timestamps (List[int]): List of message timestamps
            
        Returns:
            Tuple[float, List[str]]: Time score and list of flags
        """
        flags = []
        
        # Not enough timestamps to analyze
        if not timestamps or len(timestamps) < 2:
            return 0.5, []
            
        # Calculate response times
        response_times = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]
        avg_response_time = sum(response_times) / len(response_times)
        
        if avg_response_time > self.thresholds['max_response_time']:
            flags.append(f"Slow average response time ({avg_response_time/3600:.1f} hours)")
            
        # Check for inconsistent response patterns
        time_variance = sum(abs(response_times[i] - response_times[i-1]) 
                           for i in range(1, len(response_times))) / (len(response_times) - 1)
        
        if time_variance > self.thresholds['max_response_time']:
            flags.append("Highly inconsistent response times")
            
        # Calculate time score
        time_score = max(0, 1 - (avg_response_time / self.thresholds['max_response_time']))
        
        return time_score, flags