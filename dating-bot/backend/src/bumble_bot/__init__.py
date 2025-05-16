"""
Bumble Bot - Core functionality for automating Bumble interactions.

This package provides modules for automating interactions with Bumble's web interface,
including login, navigation, and swiping functionality.
"""

from .bot import BumbleBot
from .login import BumbleLogin
from .navigator import BumbleNavigator
from .swiper import BumbleSwiper

__all__ = ['BumbleBot', 'BumbleLogin', 'BumbleNavigator', 'BumbleSwiper']