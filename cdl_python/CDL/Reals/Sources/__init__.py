# ABOUTME: Reals Sources package - Signal source blocks for Real values
# ABOUTME: Provides constant and time-based signal generators

from cdl_python.CDL.Reals.Sources.Constant import Constant
from cdl_python.CDL.Reals.Sources.Sin import Sin
from cdl_python.CDL.Reals.Sources.Pulse import Pulse
from cdl_python.CDL.Reals.Sources.Ramp import Ramp
from cdl_python.CDL.Reals.Sources.TimeTable import TimeTable, Smoothness, Extrapolation
from cdl_python.CDL.Reals.Sources.CalendarTime import CalendarTime, ZeroTime
from cdl_python.CDL.Reals.Sources.CivilTime import CivilTime

__all__ = [
    "CalendarTime",
    "CivilTime",
    "Constant",
    "Extrapolation",
    "Pulse",
    "Ramp",
    "Sin",
    "Smoothness",
    "TimeTable",
    "ZeroTime",
]
