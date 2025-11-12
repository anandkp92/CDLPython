# ABOUTME: CDL Types package - Enumerations for CDL blocks
# ABOUTME: Defines type enumerations used across CDL packages
from enum import Enum, auto


class SimpleController(Enum):
    """Enumeration defining P, PI, PD, or PID simple controller type"""
    P = "P"          # P controller
    PI = "PI"        # PI controller
    PD = "PD"        # PD controller
    PID = "PID"      # PID controller


class Extrapolation(Enum):
    """Enumeration defining the extrapolation of time table interpolation"""
    HoldLastPoint = "HoldLastPoint"      # Hold the first/last table point outside of the table scope
    LastTwoPoints = "LastTwoPoints"      # Extrapolate by using the derivative at the first/last table points
    Periodic = "Periodic"                # Repeat the table scope periodically


class Smoothness(Enum):
    """Enumeration defining the smoothness of table interpolation"""
    LinearSegments = "LinearSegments"        # Table points are linearly interpolated
    ConstantSegments = "ConstantSegments"    # Table points are not interpolated, but the previous tabulated value is returned


class ZeroTime(Enum):
    """Enumeration to set the date corresponding to time = 0"""
    UnixTimeStamp = "UnixTimeStamp"          # Thu, 01 Jan 1970 00:00:00 local time
    UnixTimeStampGMT = "UnixTimeStampGMT"    # Thu, 01 Jan 1970 00:00:00 GMT
    Custom = "Custom"                        # User specified local time
    NY2010 = "NY2010"                        # New year 2010, 00:00:00 local time
    NY2011 = "NY2011"
    NY2012 = "NY2012"
    NY2013 = "NY2013"
    NY2014 = "NY2014"
    NY2015 = "NY2015"
    NY2016 = "NY2016"
    NY2017 = "NY2017"
    NY2018 = "NY2018"
    NY2019 = "NY2019"
    NY2020 = "NY2020"
    NY2021 = "NY2021"
    NY2022 = "NY2022"
    NY2023 = "NY2023"
    NY2024 = "NY2024"
    NY2025 = "NY2025"
    NY2026 = "NY2026"
    NY2027 = "NY2027"
    NY2028 = "NY2028"
    NY2029 = "NY2029"
    NY2030 = "NY2030"
    NY2031 = "NY2031"
    NY2032 = "NY2032"
    NY2033 = "NY2033"
    NY2034 = "NY2034"
    NY2035 = "NY2035"
    NY2036 = "NY2036"
    NY2037 = "NY2037"
    NY2038 = "NY2038"
    NY2039 = "NY2039"
    NY2040 = "NY2040"
    NY2041 = "NY2041"
    NY2042 = "NY2042"
    NY2043 = "NY2043"
    NY2044 = "NY2044"
    NY2045 = "NY2045"
    NY2046 = "NY2046"
    NY2047 = "NY2047"
    NY2048 = "NY2048"
    NY2049 = "NY2049"
    NY2050 = "NY2050"


__all__ = [
    "SimpleController",
    "Extrapolation",
    "Smoothness",
    "ZeroTime",
]
