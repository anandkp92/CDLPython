# ABOUTME: Sin block - outputs sine of real input in radians.
# ABOUTME: Implements y = sin(u) for CDL real-valued sine function.

import math
from typing import Dict, Any
from cdl_python.base import CDLBlock


class Sin(CDLBlock):
    """
    Output the sine of the input.

    Outputs y = sin(u) where u is in radians.

    Inputs:
        u: Input for the sine function (in radians)

    Outputs:
        y: Sine of input
    """

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Compute sine of input.

        Args:
            u: Input value in radians

        Returns:
            Dictionary with output 'y' = sin(u)
        """
        return {'y': math.sin(u)}
