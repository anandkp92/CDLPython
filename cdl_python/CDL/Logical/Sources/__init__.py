"""
Logical source blocks for CDL

This package contains blocks that generate boolean signals.
"""

from .Constant import Constant
from .Pulse import Pulse
from .SampleTrigger import SampleTrigger
from .TimeTable import TimeTable

__all__ = [
    'Constant',
    'Pulse',
    'SampleTrigger',
    'TimeTable',
]
