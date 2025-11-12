# ABOUTME: BooleanToReal block - converts boolean to real.
# ABOUTME: Implements y = 1.0 if u else 0.0 for CDL boolean-to-real conversion.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class BooleanToReal(CDLBlock):
    """
    Convert Boolean to Real signal.

    Outputs y = 1.0 if u is True, else y = 0.0

    Inputs:
        u: Boolean input

    Outputs:
        y: Real output (0.0 or 1.0)
    """

    def compute(self, u: bool) -> Dict[str, Any]:
        """
        Convert boolean to real.

        Args:
            u: Boolean value

        Returns:
            Dictionary with output 'y' = 1.0 if u else 0.0
        """
        return {'y': 1.0 if u else 0.0}
