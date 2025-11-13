# ABOUTME: Logical CDL blocks for boolean operations.
# ABOUTME: Includes logic gates, edge detection, and boolean signal processing.

# Import from keyword-named modules using importlib to avoid syntax issues
import importlib
And = importlib.import_module('cdl_python.CDL.Logical.And').And
Or = importlib.import_module('cdl_python.CDL.Logical.Or').Or
Not = importlib.import_module('cdl_python.CDL.Logical.Not').Not

from cdl_python.CDL.Logical.Edge import Edge
from cdl_python.CDL.Logical.Xor import Xor
from cdl_python.CDL.Logical.Nand import Nand
from cdl_python.CDL.Logical.Nor import Nor
from cdl_python.CDL.Logical.MultiAnd import MultiAnd
from cdl_python.CDL.Logical.MultiOr import MultiOr
from cdl_python.CDL.Logical.FallingEdge import FallingEdge
from cdl_python.CDL.Logical.Change import Change
from cdl_python.CDL.Logical.Pre import Pre
from cdl_python.CDL.Logical.Latch import Latch
from cdl_python.CDL.Logical.Toggle import Toggle
from cdl_python.CDL.Logical.Switch import Switch
from cdl_python.CDL.Logical.Timer import Timer
from cdl_python.CDL.Logical.TimerAccumulating import TimerAccumulating
from cdl_python.CDL.Logical.TrueDelay import TrueDelay
from cdl_python.CDL.Logical.TrueFalseHold import TrueFalseHold
from cdl_python.CDL.Logical.Proof import Proof
from cdl_python.CDL.Logical.VariablePulse import VariablePulse

__all__ = [
    "And",
    "Or",
    "Not",
    "Edge",
    "Xor",
    "Nand",
    "Nor",
    "MultiAnd",
    "MultiOr",
    "FallingEdge",
    "Change",
    "Pre",
    "Latch",
    "Toggle",
    "Switch",
    "Timer",
    "TimerAccumulating",
    "TrueDelay",
    "TrueFalseHold",
    "Proof",
    "VariablePulse",
]
