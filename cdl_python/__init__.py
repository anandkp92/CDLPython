# ABOUTME: CDLPython library - Python implementation of Control Description Language blocks.
# ABOUTME: Provides elementary blocks for building control sequences with simulation and real-time execution support.

from cdl_python.time_manager import TimeManager, ExecutionMode
from cdl_python.base import CDLBlock

__version__ = "0.1.0"

__all__ = [
    "TimeManager",
    "ExecutionMode",
    "CDLBlock",
    "CDL",
]

# Package-level imports for convenience
from cdl_python import CDL
