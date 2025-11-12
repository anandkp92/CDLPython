# ABOUTME: RealToInteger block - converts real to integer by truncation.
# ABOUTME: Implements y = int(u) for CDL real-to-integer conversion.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class RealToInteger(CDLBlock):
    """
    Convert Real to Integer signal by truncation.

    Outputs y = int(u) (truncates toward zero)

    Inputs:
        u: Real input

    Outputs:
        y: Integer output
    """

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Convert real to integer by truncation.

        Args:
            u: Real value

        Returns:
            Dictionary with output 'y' = int(u)
        """
        return {'y': int(u)}
