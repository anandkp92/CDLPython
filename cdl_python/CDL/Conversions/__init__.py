# ABOUTME: Type conversion CDL blocks.
# ABOUTME: Provides conversions between Boolean, Integer, and Real types.

from cdl_python.CDL.Conversions.BooleanToInteger import BooleanToInteger
from cdl_python.CDL.Conversions.BooleanToReal import BooleanToReal
from cdl_python.CDL.Conversions.IntegerToReal import IntegerToReal
from cdl_python.CDL.Conversions.RealToInteger import RealToInteger

__all__ = [
    "BooleanToInteger",
    "BooleanToReal",
    "IntegerToReal",
    "RealToInteger",
]
