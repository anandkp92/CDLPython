# ABOUTME: IntegerToReal block - converts integer to real.
# ABOUTME: Implements y = float(u) for CDL integer-to-real conversion.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class IntegerToReal(CDLBlock):
    """
    Convert Integer to Real signal.

    Outputs y = float(u)

    Inputs:
        u: Integer input

    Outputs:
        y: Real output
    """

    def compute(self, u: int) -> Dict[str, Any]:
        """
        Convert integer to real.

        Args:
            u: Integer value

        Returns:
            Dictionary with output 'y' = float(u)
        """
        return {'y': float(u)}
