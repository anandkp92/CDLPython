# ABOUTME: Log10 block - outputs base-10 logarithm of real input.
# ABOUTME: Implements y = log10(u) for CDL real-valued base-10 logarithm (u > 0 required).

import math
from typing import Dict, Any
from cdl_python.base import CDLBlock


class Log10(CDLBlock):
    """
    Output the base 10 logarithm of the input.

    Outputs y = log10(u) (logarithm base 10)
    Input u must be positive.

    Inputs:
        u: Input for the logarithm function (must be > 0)

    Outputs:
        y: Base-10 logarithm of input

    Raises:
        ValueError: If input is non-positive
    """

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Compute base-10 logarithm of input.

        Args:
            u: Input value (must be > 0)

        Returns:
            Dictionary with output 'y' = log10(u)

        Raises:
            ValueError: If u <= 0
        """
        if u <= 0:
            raise ValueError(f"Log10 requires positive input, got {u}")
        return {'y': math.log10(u)}
