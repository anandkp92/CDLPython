# ABOUTME: DewPoint_TDryBulPhi - Dew point temperature from dry bulb temp and relative humidity
from typing import Any, Dict
import math
from cdl_python.base import CDLBlock


class DewPoint_TDryBulPhi(CDLBlock):
    """Compute dew point temperature from dry bulb temperature and relative humidity

    Calculates the dew point temperature using the dry bulb temperature and
    relative humidity. Uses the Magnus-Tetens approximation for saturation
    vapor pressure.

    Inputs:
    - TDryBul: Dry bulb temperature (K)
    - phi: Relative humidity (0-1)

    Output:
    - TDewPoi: Dew point temperature (K)

    Used for:
    - HVAC system design
    - Comfort calculations
    - Condensation risk assessment
    - Dehumidification control
    """

    def __init__(self):
        """Initialize DewPoint_TDryBulPhi block"""
        super().__init__()

    def compute(self, TDryBul: float, phi: float) -> Dict[str, Any]:
        """Compute dew point temperature

        Args:
            TDryBul: Dry bulb temperature in Kelvin
            phi: Relative humidity (0 to 1)

        Returns:
            Dictionary with 'TDewPoi': dew point temperature in Kelvin
        """
        # Convert from Kelvin to Celsius for calculation
        T_C = TDryBul - 273.15

        # Clamp relative humidity to valid range
        phi = max(0.01, min(0.99, phi))

        # Magnus-Tetens constants for water
        a = 17.27
        b = 237.7  # °C

        # Calculate gamma
        gamma = (a * T_C) / (b + T_C) + math.log(phi)

        # Dew point in Celsius
        TDewPoi_C = (b * gamma) / (a - gamma)

        # Convert back to Kelvin
        TDewPoi = TDewPoi_C + 273.15

        return {'TDewPoi': TDewPoi}
