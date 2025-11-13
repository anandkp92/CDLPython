# ABOUTME: SpecificEnthalpy_TDryBulPhi - Specific enthalpy from dry bulb temp and RH
from typing import Any, Dict
import math
from cdl_python.base import CDLBlock


class SpecificEnthalpy_TDryBulPhi(CDLBlock):
    """Compute specific enthalpy from dry bulb temperature and relative humidity

    Calculates the specific enthalpy of moist air using dry bulb temperature
    and relative humidity. Enthalpy includes both sensible and latent heat.

    Inputs:
    - TDryBul: Dry bulb temperature (K)
    - phi: Relative humidity (0-1)

    Output:
    - h: Specific enthalpy (J/kg)

    Used for:
    - HVAC energy calculations
    - Cooling/heating load determination
    - Air conditioning system design
    - Energy efficiency analysis
    """

    def __init__(self, p_atm: float = 101325.0):
        """Initialize SpecificEnthalpy_TDryBulPhi block

        Args:
            p_atm: Atmospheric pressure in Pa (default: 101325 Pa = 1 atm)
        """
        super().__init__()
        self.p_atm = p_atm

    def _saturation_pressure(self, T: float) -> float:
        """Calculate saturation vapor pressure using Antoine equation

        Args:
            T: Temperature in Kelvin

        Returns:
            Saturation pressure in Pa
        """
        T_C = T - 273.15  # Convert to Celsius

        # Antoine equation constants for water (10°C to 60°C range)
        A = 8.07131
        B = 1730.63
        C = 233.426

        # Calculate log10(p_sat) in mmHg
        log_p_sat = A - B / (C + T_C)
        p_sat_mmHg = 10 ** log_p_sat

        # Convert mmHg to Pa
        p_sat = p_sat_mmHg * 133.322

        return p_sat

    def compute(self, TDryBul: float, phi: float) -> Dict[str, Any]:
        """Compute specific enthalpy

        Args:
            TDryBul: Dry bulb temperature in Kelvin
            phi: Relative humidity (0 to 1)

        Returns:
            Dictionary with 'h': specific enthalpy in J/kg
        """
        # Constants
        cp_air = 1006.0  # Specific heat of dry air (J/kg·K)
        cp_vapor = 1860.0  # Specific heat of water vapor (J/kg·K)
        h_fg = 2501000.0  # Latent heat of vaporization at 0°C (J/kg)

        # Clamp relative humidity
        phi = max(0.0, min(1.0, phi))

        # Calculate saturation pressure
        p_sat = self._saturation_pressure(TDryBul)

        # Partial pressure of water vapor
        p_vapor = phi * p_sat

        # Humidity ratio (kg water / kg dry air)
        W = 0.622 * p_vapor / (self.p_atm - p_vapor)

        # Specific enthalpy (J/kg dry air)
        T_ref = 273.15  # Reference temperature (0°C)
        h = cp_air * (TDryBul - T_ref) + W * (h_fg + cp_vapor * (TDryBul - T_ref))

        return {'h': h}
