# ABOUTME: Line interpolation block
# ABOUTME: Computes linear interpolation through two points with optional limiting
from typing import Any, Dict
from cdl_python.base import CDLBlock


class Line(CDLBlock):
    """
    Line interpolation block

    Outputs value along a line specified by two points.
    Computes y = a + b*u where the line passes through (x1, f1) and (x2, f2).

    Parameters:
        limitBelow: If true, limit u to be no smaller than x1 (default: True)
        limitAbove: If true, limit u to be no larger than x2 (default: True)

    Inputs:
        x1: x-coordinate of first point (must be < x2 if limits are used)
        f1: y-coordinate of first point, f(x1)
        x2: x-coordinate of second point (must be > x1 if limits are used)
        f2: y-coordinate of second point, f(x2)
        u: Input value to interpolate

    Outputs:
        y: Interpolated output value
    """

    def __init__(self, limitBelow: bool = True, limitAbove: bool = True, **kwargs):
        """
        Initialize Line block.

        Args:
            limitBelow: Enable lower limit
            limitAbove: Enable upper limit
        """
        super().__init__(**kwargs)
        self.limitBelow = limitBelow
        self.limitAbove = limitAbove

    def compute(self, x1: float, f1: float, x2: float, f2: float, u: float) -> Dict[str, Any]:
        """
        Compute linear interpolation.

        Args:
            x1: x-coordinate of first point
            f1: y-coordinate of first point
            x2: x-coordinate of second point
            f2: y-coordinate of second point
            u: Input value

        Returns:
            Dictionary with key 'y' containing interpolated value
        """
        # Calculate slope and intercept
        # y = a + b*x where b = (f2-f1)/(x2-x1) and a = f2 - b*x2
        if x2 == x1:
            # Avoid division by zero
            b = 0.0
            a = f1
        else:
            b = (f2 - f1) / (x2 - x1)
            a = f2 - b * x2

        # Apply limits to input
        xLim = u
        if self.limitBelow and self.limitAbove:
            xLim = min(x2, max(x1, u))
        elif self.limitBelow:
            xLim = max(x1, u)
        elif self.limitAbove:
            xLim = min(x2, u)

        # Compute output
        y = a + b * xLim

        return {'y': y}
