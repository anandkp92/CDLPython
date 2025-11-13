"""
Calendar time source block.

Computes calendar time (year, month, day, hour, minute, weekday) from simulation time.
"""

from typing import Dict, Any
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager
from datetime import datetime, timedelta
from enum import Enum


class ZeroTime(Enum):
    """Reference time definition for time = 0"""
    NY2010 = "NY2010"  # New Year 2010
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
    UNIX_TIME_STAMP = "UnixTimeStamp"  # 1970-01-01 00:00:00
    CUSTOM = "Custom"


class CalendarTime(CDLBlock):
    """Computes calendar time from simulation time

    Block that outputs year, month, day, hour, minute, and weekday based on
    simulation time and a reference time.

    Parameters:
        zerTim: How reference time (time = 0) should be defined
        yearRef: Year when time = 0 (used if zerTim=CUSTOM, default=2016)
        offset: Offset in seconds added to time (for timezone adjustment, default=0)

    Outputs:
        year: Year
        month: Month of the year (1-12)
        day: Day of the month (1-31)
        hour: Hour of the day (0-23)
        minute: Minute of the hour (0-59.999...)
        weekDay: Day of week (1=Monday, 7=Sunday)
    """

    # Reference dates for each ZeroTime option
    _REFERENCE_DATES = {
        ZeroTime.NY2010: datetime(2010, 1, 1, 0, 0, 0),
        ZeroTime.NY2011: datetime(2011, 1, 1, 0, 0, 0),
        ZeroTime.NY2012: datetime(2012, 1, 1, 0, 0, 0),
        ZeroTime.NY2013: datetime(2013, 1, 1, 0, 0, 0),
        ZeroTime.NY2014: datetime(2014, 1, 1, 0, 0, 0),
        ZeroTime.NY2015: datetime(2015, 1, 1, 0, 0, 0),
        ZeroTime.NY2016: datetime(2016, 1, 1, 0, 0, 0),
        ZeroTime.NY2017: datetime(2017, 1, 1, 0, 0, 0),
        ZeroTime.NY2018: datetime(2018, 1, 1, 0, 0, 0),
        ZeroTime.NY2019: datetime(2019, 1, 1, 0, 0, 0),
        ZeroTime.NY2020: datetime(2020, 1, 1, 0, 0, 0),
        ZeroTime.UNIX_TIME_STAMP: datetime(1970, 1, 1, 0, 0, 0),
    }

    def __init__(self, time_manager: TimeManager, zerTim: ZeroTime = ZeroTime.NY2016,
                 yearRef: int = 2016, offset: float = 0.0):
        """Initialize CalendarTime block

        Args:
            time_manager: Time manager for getting current time
            zerTim: Reference time definition
            yearRef: Year when time = 0 (used if zerTim=CUSTOM)
            offset: Offset in seconds (for timezone adjustment)
        """
        super().__init__(time_manager)

        self.zerTim = zerTim
        self.yearRef = yearRef
        self.offset = offset

        # Determine reference date
        if zerTim == ZeroTime.CUSTOM:
            if not (2010 <= yearRef <= 2031):
                raise ValueError(f"yearRef must be between 2010 and 2031, got {yearRef}")
            self.reference_date = datetime(yearRef, 1, 1, 0, 0, 0)
        else:
            self.reference_date = self._REFERENCE_DATES[zerTim]

    def compute(self) -> Dict[str, Any]:
        """Compute calendar time outputs

        Returns:
            Dictionary with calendar time components:
                'year': Year
                'month': Month (1-12)
                'day': Day of month (1-31)
                'hour': Hour of day (0-23)
                'minute': Minute of hour (0.0-59.999...)
                'weekDay': Day of week (1=Monday, 7=Sunday)
        """
        current_time = self.get_time()

        # Add offset
        adjusted_time = current_time + self.offset

        # Calculate actual datetime
        dt = self.reference_date + timedelta(seconds=adjusted_time)

        # Extract components
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour
        minute = dt.minute + dt.second / 60.0 + dt.microsecond / 60000000.0

        # Weekday: Python's weekday() returns 0=Monday, 6=Sunday
        # CDL expects 1=Monday, 7=Sunday
        weekDay = dt.weekday() + 1

        return {
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'minute': minute,
            'weekDay': weekDay
        }
