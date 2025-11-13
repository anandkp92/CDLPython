# ABOUTME: SunRiseSet - Compute sunrise and sunset times
from typing import Any, Dict
import math
from cdl_python.base import CDLBlock


class SunRiseSet(CDLBlock):
    """Compute sunrise and sunset times for a given location and date

    Calculates sunrise and sunset times using simplified astronomical algorithms.
    Based on NOAA solar position algorithms.

    Inputs:
    - time: Current time in seconds since start (used to determine day of year)
    - latitude: Latitude in degrees (-90 to 90, positive north)
    - longitude: Longitude in degrees (-180 to 180, positive east)

    Outputs:
    - tSunRis: Sunrise time in seconds since midnight (local solar time)
    - tSunSet: Sunset time in seconds since midnight (local solar time)

    Used for:
    - Daylighting control strategies
    - Shading device control
    - Optimal start/stop times for HVAC
    - Solar tracking systems
    """

    def __init__(self, year: int = 2024):
        """Initialize SunRiseSet block

        Args:
            year: Year for calculations (affects leap year handling)
        """
        super().__init__()
        self.year = year
        self._is_leap_year = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def _day_of_year(self, time: float) -> int:
        """Calculate day of year from time in seconds

        Args:
            time: Time in seconds since start of year

        Returns:
            Day of year (1-365 or 1-366 for leap years)
        """
        seconds_per_day = 86400
        day = int(time / seconds_per_day) + 1
        max_days = 366 if self._is_leap_year else 365
        return min(max(day, 1), max_days)

    def _solar_declination(self, day_of_year: int) -> float:
        """Calculate solar declination angle

        Args:
            day_of_year: Day of year (1-365/366)

        Returns:
            Declination angle in radians
        """
        # Simplified formula (Spencer 1971)
        # Day angle in radians
        gamma = 2.0 * math.pi * (day_of_year - 1) / 365.0

        # Declination in radians
        decl = 0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma) \
               - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma) \
               - 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma)

        return decl

    def _equation_of_time(self, day_of_year: int) -> float:
        """Calculate equation of time (correction for solar time)

        Args:
            day_of_year: Day of year (1-365/366)

        Returns:
            Equation of time in minutes
        """
        # Day angle
        gamma = 2.0 * math.pi * (day_of_year - 1) / 365.0

        # Equation of time in minutes (Spencer 1971)
        eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma)
                          - 0.032077 * math.sin(gamma)
                          - 0.014615 * math.cos(2 * gamma)
                          - 0.040849 * math.sin(2 * gamma))

        return eqtime

    def compute(self, time: float, latitude: float, longitude: float) -> Dict[str, Any]:
        """Compute sunrise and sunset times

        Args:
            time: Current time in seconds since start of year
            latitude: Latitude in degrees (-90 to 90, north positive)
            longitude: Longitude in degrees (-180 to 180, east positive)

        Returns:
            Dictionary with:
                - 'tSunRis': Sunrise time in seconds since midnight (local solar time)
                - 'tSunSet': Sunset time in seconds since midnight (local solar time)
        """
        # Convert angles to radians
        lat_rad = math.radians(latitude)

        # Get day of year
        day_of_year = self._day_of_year(time)

        # Calculate solar declination
        decl = self._solar_declination(day_of_year)

        # Calculate hour angle at sunrise/sunset (sun at horizon, zenith = 90°)
        # cos(hour_angle) = -tan(lat) * tan(decl)
        cos_ha = -math.tan(lat_rad) * math.tan(decl)

        # Check for polar day/night
        if cos_ha > 1.0:
            # Polar night (sun never rises)
            return {'tSunRis': 0.0, 'tSunSet': 0.0}
        elif cos_ha < -1.0:
            # Polar day (sun never sets)
            return {'tSunRis': 0.0, 'tSunSet': 86400.0}

        # Hour angle in radians
        ha = math.acos(cos_ha)

        # Convert hour angle to time (radians to hours)
        ha_hours = ha * 12.0 / math.pi

        # Equation of time correction
        eqtime = self._equation_of_time(day_of_year)

        # Solar noon (local solar time) in minutes
        solar_noon = 720.0 - 4.0 * longitude - eqtime

        # Sunrise and sunset in minutes since midnight
        sunrise_minutes = solar_noon - ha_hours * 60.0
        sunset_minutes = solar_noon + ha_hours * 60.0

        # Convert to seconds
        tSunRis = sunrise_minutes * 60.0
        tSunSet = sunset_minutes * 60.0

        # Clamp to valid range [0, 86400]
        tSunRis = max(0.0, min(86400.0, tSunRis))
        tSunSet = max(0.0, min(86400.0, tSunSet))

        return {
            'tSunRis': tSunRis,
            'tSunSet': tSunSet
        }
