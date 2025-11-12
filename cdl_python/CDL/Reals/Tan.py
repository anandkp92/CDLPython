# ABOUTME: Tan block - outputs tangent of real input in radians.
# ABOUTME: Implements y = tan(u) for CDL real-valued tangent function.

import math
from typing import Dict, Any
from cdl_python.base import CDLBlock


class Tan(CDLBlock):
    """
    Output the tangent of the input.

    Outputs y = tan(u) where u is in radians.

    Inputs:
        u: Input for the tangent function (in radians)

    Outputs:
        y: Tangent of input
    """

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Compute tangent of input.

        Args:
            u: Input value in radians

        Returns:
            Dictionary with output 'y' = tan(u)
        """
        return {'y': math.tan(u)}
