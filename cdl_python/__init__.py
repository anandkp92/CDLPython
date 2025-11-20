# ABOUTME: CDLPython library - Python implementation of Control Description Language blocks.
# ABOUTME: Provides elementary blocks for building control sequences with simulation and real-time execution support.

from cdl_python.time_manager import TimeManager, ExecutionMode
from cdl_python.base import CDLBlock
from cdl_python.checkpoint import CheckpointManager, AutoCheckpointer

__version__ = "0.1.0"

__all__ = [
    "TimeManager",
    "ExecutionMode",
    "CDLBlock",
    "CheckpointManager",
    "AutoCheckpointer",
    "CDL",
]

# Package-level imports for convenience
from cdl_python import CDL
