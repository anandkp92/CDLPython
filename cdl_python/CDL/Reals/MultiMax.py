# ABOUTME: MultiMax block - maximum of multiple real inputs.
# ABOUTME: Implements y = max(u[1], u[2], ..., u[n]) for CDL multi-input maximum.

from typing import Dict, Any, List
from cdl_python.base import CDLBlock


class MultiMax(CDLBlock):
    """
    Output the maximum element of the input vector.

    Parameters:
        nin: Number of input signals (default: 0)

    Inputs:
        u: List of input values (length must match nin)

    Outputs:
        y: Largest element of the input vector
    """

    def __init__(self, nin: int = 0, **kwargs):
        """
        Initialize MultiMax.

        Args:
            nin: Number of inputs
            **kwargs: Additional arguments for CDLBlock
        """
        super().__init__(**kwargs)
        self.nin = nin

    def compute(self, u: List[float]) -> Dict[str, Any]:
        """
        Compute maximum of inputs.

        Args:
            u: List of input values

        Returns:
            Dictionary with output 'y' = max(u)

        Raises:
            ValueError: If input list is empty or wrong size
        """
        if len(u) == 0:
            raise ValueError("MultiMax requires at least one input")

        if len(u) != self.nin:
            raise ValueError(f"Expected {self.nin} inputs, got {len(u)}")

        return {'y': max(u)}
