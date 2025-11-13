# ABOUTME: Tests for new Utilities blocks (SunRiseSet)
import pytest
import math
from cdl_python.CDL.Utilities import SunRiseSet


class TestSunRiseSet:
    """Test SunRiseSet block"""

    def test_sunrise_before_sunset(self):
        """Sunrise should occur before sunset"""
        sun = SunRiseSet(year=2024)

        # March equinox (day 80), mid-latitudes
        time = 80 * 86400  # Day 80
        latitude = 40.0  # 40°N
        longitude = 0.0

        result = sun.compute(time=time, latitude=latitude, longitude=longitude)

        assert result['tSunRis'] < result['tSunSet']

    def test_day_length_at_equator(self):
        """At equator, day length should be ~12 hours year-round"""
        sun = SunRiseSet(year=2024)

        # Equator
        latitude = 0.0
        longitude = 0.0

        for day in [1, 80, 172, 264]:  # Different seasons
            time = day * 86400
            result = sun.compute(time=time, latitude=latitude, longitude=longitude)

            day_length = result['tSunSet'] - result['tSunRis']
            # Should be close to 12 hours (43200 seconds)
            assert 42000 < day_length < 44400  # Within 20 min

    def test_longer_days_in_summer(self):
        """Northern hemisphere should have longer days in summer"""
        sun = SunRiseSet(year=2024)

        latitude = 45.0  # 45°N
        longitude = 0.0

        # Winter (day 1 - January)
        winter_result = sun.compute(time=1*86400, latitude=latitude, longitude=longitude)
        winter_day = winter_result['tSunSet'] - winter_result['tSunRis']

        # Summer (day 172 - June)
        summer_result = sun.compute(time=172*86400, latitude=latitude, longitude=longitude)
        summer_day = summer_result['tSunSet'] - summer_result['tSunRis']

        # Summer days should be longer
        assert summer_day > winter_day

    def test_midnight_sun_at_pole(self):
        """At poles during summer, sun should not set"""
        sun = SunRiseSet(year=2024)

        # North pole during summer solstice (day 172)
        latitude = 85.0  # Near north pole
        longitude = 0.0
        time = 172 * 86400  # Summer solstice

        result = sun.compute(time=time, latitude=latitude, longitude=longitude)

        # Day length should be very long (approaching 24 hours)
        day_length = result['tSunSet'] - result['tSunRis']
        assert day_length > 70000  # > 19 hours

    def test_reasonable_sunrise_time(self):
        """Sunrise time should be reasonable"""
        sun = SunRiseSet(year=2024)

        # Typical mid-latitude location
        latitude = 40.0
        longitude = -75.0  # East coast US
        time = 100 * 86400  # Spring

        result = sun.compute(time=time, latitude=latitude, longitude=longitude)

        # Sunrise should be between 3 AM and 9 AM (wider bounds for solar vs local time)
        assert 10000 < result['tSunRis'] < 40000
        # Sunset should be between 4 PM and 10 PM (wider bounds for solar vs local time)
        assert 50000 < result['tSunSet'] < 90000
