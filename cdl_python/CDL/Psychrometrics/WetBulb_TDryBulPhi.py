# ABOUTME: WetBulb_TDryBulPhi - Wet bulb temperature from dry bulb temp and RH
from typing import Any, Dict
import math
from cdl_python.base import CDLBlock


class WetBulb_TDryBulPhi(CDLBlock):
    """Compute wet bulb temperature from dry bulb temperature and relative humidity

    Calculates the wet bulb temperature using an approximation method.
    Wet bulb temperature is the lowest temperature that can be reached by
    evaporative cooling.

    Inputs:
    - TDryBul: Dry bulb temperature (K)
    - phi: Relative humidity (0-1)

    Output:
    - TWetBul: Wet bulb temperature (K)

    Used for:
    - Evaporative cooling design
    - Natural wet bulb temperature monitoring
    - Cooling tower calculations
    - Heat stress assessment
    """

    def __init__(self, p_atm: float = 101325.0):
        """Initialize WetBulb_TDryBulPhi block

        Args:
            p_atm: Atmospheric pressure in Pa (default: 101325 Pa = 1 atm)
        """
        super().__init__()
        self.p_atm = p_atm

    def _saturation_pressure(self, T: float) -> float:
        """Calculate saturation vapor pressure

        Args:
            T: Temperature in Kelvin

        Returns:
            Saturation pressure in Pa
        """
        T_C = T - 273.15
        A = 8.07131
        B = 1730.63
        C = 233.426
        log_p_sat = A - B / (C + T_C)
        p_sat_mmHg = 10 ** log_p_sat
        return p_sat_mmHg * 133.322

    def compute(self, TDryBul: float, phi: float) -> Dict[str, Any]:
        """Compute wet bulb temperature

        Args:
            TDryBul: Dry bulb temperature in Kelvin
            phi: Relative humidity (0 to 1)

        Returns:
            Dictionary with 'TWetBul': wet bulb temperature in Kelvin
        """
        # Clamp relative humidity
        phi = max(0.01, min(1.0, phi))

        # Convert to Celsius for calculation
        T_C = TDryBul - 273.15

        # Stull's approximation for wet bulb temperature
        # Valid for T between -20°C and 50°C, RH between 5% and 99%
        # Reference: Stull, R. (2011), Journal of Applied Meteorology and Climatology

        # Convert phi (0-1) to percentage (0-100)
        RH = phi * 100.0

        # Stull's formula
        TWet_C = T_C * math.atan(0.151977 * math.sqrt(RH + 8.313659)) + \
                 math.atan(T_C + RH) - \
                 math.atan(RH - 1.676331) + \
                 0.00391838 * (RH ** 1.5) * math.atan(0.023101 * RH) - \
                 4.686035

        # Convert back to Kelvin
        TWetBul = TWet_C + 273.15

        # Wet bulb cannot exceed dry bulb
        TWetBul = min(TWetBul, TDryBul)

        return {'TWetBul': TWetBul}
