# ABOUTME: Tests for Psychrometrics blocks
import pytest
from cdl_python.CDL.Psychrometrics import (
    DewPoint_TDryBulPhi,
    SpecificEnthalpy_TDryBulPhi,
    WetBulb_TDryBulPhi,
)


class TestDewPoint:
    """Test DewPoint_TDryBulPhi block"""

    def test_dew_point_calculation(self):
        """Test dew point at typical conditions"""
        dp = DewPoint_TDryBulPhi()

        # 20°C, 50% RH
        TDryBul = 293.15  # 20°C in K
        phi = 0.5
        result = dp.compute(TDryBul=TDryBul, phi=phi)

        TDewPoi_C = result['TDewPoi'] - 273.15
        # Dew point should be around 9-10°C
        assert 8 < TDewPoi_C < 11

    def test_dew_point_at_saturation(self):
        """At 100% RH, dew point equals dry bulb"""
        dp = DewPoint_TDryBulPhi()

        TDryBul = 298.15  # 25°C
        phi = 1.0
        result = dp.compute(TDryBul=TDryBul, phi=phi)

        # Should be very close to dry bulb
        assert abs(result['TDewPoi'] - TDryBul) < 0.5

    def test_handles_low_humidity(self):
        """Test at low relative humidity"""
        dp = DewPoint_TDryBulPhi()

        TDryBul = 300.15  # 27°C
        phi = 0.1  # 10% RH
        result = dp.compute(TDryBul=TDryBul, phi=phi)

        # Dew point should be well below dry bulb
        assert result['TDewPoi'] < TDryBul - 10


class TestSpecificEnthalpy:
    """Test SpecificEnthalpy_TDryBulPhi block"""

    def test_enthalpy_increases_with_temperature(self):
        """Enthalpy should increase with temperature"""
        enthalpy = SpecificEnthalpy_TDryBulPhi()

        h1 = enthalpy.compute(TDryBul=283.15, phi=0.5)['h']  # 10°C
        h2 = enthalpy.compute(TDryBul=293.15, phi=0.5)['h']  # 20°C

        assert h2 > h1

    def test_enthalpy_increases_with_humidity(self):
        """Enthalpy should increase with humidity (latent heat)"""
        enthalpy = SpecificEnthalpy_TDryBulPhi()

        h1 = enthalpy.compute(TDryBul=293.15, phi=0.3)['h']  # 30% RH
        h2 = enthalpy.compute(TDryBul=293.15, phi=0.8)['h']  # 80% RH

        assert h2 > h1

    def test_enthalpy_reasonable_value(self):
        """Test enthalpy at typical conditions"""
        enthalpy = SpecificEnthalpy_TDryBulPhi()

        # 20°C, 50% RH - typical indoor conditions
        h = enthalpy.compute(TDryBul=293.15, phi=0.5)['h']

        # Should be positive and reasonable (order of 10^4 J/kg)
        assert 10000 < h < 100000


class TestWetBulb:
    """Test WetBulb_TDryBulPhi block"""

    def test_wet_bulb_below_dry_bulb(self):
        """Wet bulb should be at or below dry bulb"""
        wb = WetBulb_TDryBulPhi()

        TDryBul = 303.15  # 30°C
        phi = 0.4  # 40% RH
        result = wb.compute(TDryBul=TDryBul, phi=phi)

        assert result['TWetBul'] <= TDryBul

    def test_wet_bulb_at_saturation(self):
        """At 100% RH, wet bulb equals dry bulb"""
        wb = WetBulb_TDryBulPhi()

        TDryBul = 298.15  # 25°C
        phi = 1.0
        result = wb.compute(TDryBul=TDryBul, phi=phi)

        # Should be very close
        assert abs(result['TWetBul'] - TDryBul) < 1.0

    def test_wet_bulb_reasonable_depression(self):
        """Test wet bulb depression at moderate conditions"""
        wb = WetBulb_TDryBulPhi()

        TDryBul = 300.15  # 27°C
        phi = 0.5  # 50% RH
        result = wb.compute(TDryBul=TDryBul, phi=phi)

        TWetBul_C = result['TWetBul'] - 273.15
        TDry_C = TDryBul - 273.15

        # Depression should be a few degrees
        depression = TDry_C - TWetBul_C
        assert 0 < depression < 10
