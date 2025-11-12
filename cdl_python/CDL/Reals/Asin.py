# ABOUTME: Asin block - outputs arcsine of real input.
# ABOUTME: Implements y = asin(u) for CDL real-valued arcsine function.

import math
from typing import Dict, Any
from cdl_python.base import CDLBlock


class Asin(CDLBlock):
    """
    Output the arcsine of the input.

    Outputs y = asin(u) where result is in radians.
    Input u must be in range [-1, 1].

    Inputs:
        u: Input for the arcsine function (must be in [-1, 1])

    Outputs:
        y: Arcsine of input in radians

    Raises:
        ValueError: If input is outside [-1, 1]
    """

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Compute arcsine of input.

        Args:
            u: Input value (must be in [-1, 1])

        Returns:
            Dictionary with output 'y' = asin(u) in radians

        Raises:
            ValueError: If u not in [-1, 1]
        """
        if u < -1 or u > 1:
            raise ValueError(f"Asin requires input in [-1, 1], got {u}")
        return {'y': math.asin(u)}
