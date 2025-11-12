# ABOUTME: Logical CDL blocks for boolean operations.
# ABOUTME: Includes logic gates, edge detection, and boolean signal processing.

# Import from keyword-named modules using importlib to avoid syntax issues
import importlib
And = importlib.import_module('cdl_python.CDL.Logical.And').And
Or = importlib.import_module('cdl_python.CDL.Logical.Or').Or
Not = importlib.import_module('cdl_python.CDL.Logical.Not').Not

from cdl_python.CDL.Logical.Edge import Edge

__all__ = [
    "And",
    "Or",
    "Not",
    "Edge",
]
