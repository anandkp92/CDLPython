# ABOUTME: Log block - outputs natural logarithm of real input.
# ABOUTME: Implements y = log(u) for CDL real-valued natural logarithm (u > 0 required).

import math
from typing import Dict, Any
from cdl_python.base import CDLBlock


class Log(CDLBlock):
    """
    Output the natural logarithm of the input.

    Outputs y = log(u) (natural logarithm, base e)
    Input u must be positive.

    Inputs:
        u: Input for the logarithm function (must be > 0)

    Outputs:
        y: Natural logarithm of input

    Raises:
        ValueError: If input is non-positive
    """

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Compute natural logarithm of input.

        Args:
            u: Input value (must be > 0)

        Returns:
            Dictionary with output 'y' = log(u)

        Raises:
            ValueError: If u <= 0
        """
        if u <= 0:
            raise ValueError(f"Log requires positive input, got {u}")
        return {'y': math.log(u)}
