# ABOUTME: Sqrt block - outputs square root of real input.
# ABOUTME: Implements y = sqrt(u) for CDL real-valued square root (u >= 0 required).

import math
from typing import Dict, Any
from cdl_python.base import CDLBlock


class Sqrt(CDLBlock):
    """
    Output the square root of the input.

    Outputs y = sqrt(u)
    Input u must be non-negative.

    Inputs:
        u: Input to square root function (must be >= 0)

    Outputs:
        y: Square root of the input

    Raises:
        ValueError: If input is negative
    """

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Compute square root of input.

        Args:
            u: Input value (must be >= 0)

        Returns:
            Dictionary with output 'y' = sqrt(u)

        Raises:
            ValueError: If u < 0
        """
        if u < 0:
            raise ValueError(f"Sqrt requires non-negative input, got {u}")
        return {'y': math.sqrt(u)}
