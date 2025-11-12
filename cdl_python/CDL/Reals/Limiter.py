# ABOUTME: Limiter block - limits real input to specified range.
# ABOUTME: Implements y = max(uMin, min(uMax, u)) for CDL real-valued limiting.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Limiter(CDLBlock):
    """
    Limit the range of a signal.

    Outputs y = max(uMin, min(uMax, u))

    Parameters:
        uMax: Upper limit of input signal
        uMin: Lower limit of input signal

    Inputs:
        u: Input to be limited

    Outputs:
        y: Limited value of input signal

    Raises:
        ValueError: If uMin >= uMax
    """

    def __init__(self, uMax: float, uMin: float, **kwargs):
        """
        Initialize Limiter.

        Args:
            uMax: Upper limit
            uMin: Lower limit
            **kwargs: Additional arguments for CDLBlock

        Raises:
            ValueError: If uMin >= uMax
        """
        super().__init__(**kwargs)
        if uMin >= uMax:
            raise ValueError(f"uMin ({uMin}) must be smaller than uMax ({uMax})")
        self.uMax = uMax
        self.uMin = uMin

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Compute limited value.

        Args:
            u: Input value

        Returns:
            Dictionary with output 'y' = max(uMin, min(uMax, u))
        """
        return {'y': max(self.uMin, min(self.uMax, u))}
