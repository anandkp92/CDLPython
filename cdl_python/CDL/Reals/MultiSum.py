# ABOUTME: MultiSum block - weighted sum of multiple real inputs.
# ABOUTME: Implements y = k[1]*u[1] + k[2]*u[2] + ... + k[n]*u[n] for CDL multi-input sum.

from typing import Dict, Any, List
from cdl_python.base import CDLBlock


class MultiSum(CDLBlock):
    """
    Sum of Reals, y = k[1]*u[1] + k[2]*u[2] + ... + k[n]*u[n]

    Outputs weighted sum of input vector.

    Parameters:
        nin: Number of input signals (default: 0)
        k: Input gains (default: all ones)

    Inputs:
        u: List of input values (length must match nin)

    Outputs:
        y: Sum of inputs times gains
    """

    def __init__(self, nin: int = 0, k: List[float] = None, **kwargs):
        """
        Initialize MultiSum.

        Args:
            nin: Number of inputs
            k: Gain coefficients (defaults to all ones if not provided)
            **kwargs: Additional arguments for CDLBlock
        """
        super().__init__(**kwargs)
        self.nin = nin
        if k is None:
            self.k = [1.0] * nin
        else:
            if len(k) != nin:
                raise ValueError(f"Length of k ({len(k)}) must match nin ({nin})")
            self.k = k

    def compute(self, u: List[float]) -> Dict[str, Any]:
        """
        Compute weighted sum of inputs.

        Args:
            u: List of input values

        Returns:
            Dictionary with output 'y' = sum(k[i] * u[i])
        """
        if len(u) == 0:
            return {'y': 0.0}

        if len(u) != self.nin:
            raise ValueError(f"Expected {self.nin} inputs, got {len(u)}")

        y = sum(ki * ui for ki, ui in zip(self.k, u))
        return {'y': y}
