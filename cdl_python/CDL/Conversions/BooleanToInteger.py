# ABOUTME: BooleanToInteger block - converts boolean to integer.
# ABOUTME: Implements y = 1 if u else 0 for CDL boolean-to-integer conversion.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class BooleanToInteger(CDLBlock):
    """
    Convert Boolean to Integer signal.

    Outputs y = 1 if u is True, else y = 0

    Inputs:
        u: Boolean input

    Outputs:
        y: Integer output (0 or 1)
    """

    def compute(self, u: bool) -> Dict[str, Any]:
        """
        Convert boolean to integer.

        Args:
            u: Boolean value

        Returns:
            Dictionary with output 'y' = 1 if u else 0
        """
        return {'y': 1 if u else 0}
