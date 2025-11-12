# ABOUTME: Acos block - outputs arccosine of real input.
# ABOUTME: Implements y = acos(u) for CDL real-valued arccosine function.

import math
from typing import Dict, Any
from cdl_python.base import CDLBlock


class Acos(CDLBlock):
    """
    Output the arccosine of the input.

    Outputs y = acos(u) where result is in radians.
    Input u must be in range [-1, 1].

    Inputs:
        u: Input for the arccosine function (must be in [-1, 1])

    Outputs:
        y: Arccosine of input in radians

    Raises:
        ValueError: If input is outside [-1, 1]
    """

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Compute arccosine of input.

        Args:
            u: Input value (must be in [-1, 1])

        Returns:
            Dictionary with output 'y' = acos(u) in radians

        Raises:
            ValueError: If u not in [-1, 1]
        """
        if u < -1 or u > 1:
            raise ValueError(f"Acos requires input in [-1, 1], got {u}")
        return {'y': math.acos(u)}
