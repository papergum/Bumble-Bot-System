"""
Message Filter - Timewaster detection and message analysis for Bumble automation.

This package provides modules for analyzing message content and detecting potential
timewasters in Bumble conversations.
"""

from .filter import TimewasterFilter
from .analyzer import MessageAnalyzer

__all__ = ['TimewasterFilter', 'MessageAnalyzer']