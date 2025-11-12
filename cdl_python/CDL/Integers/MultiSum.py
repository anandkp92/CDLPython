# ABOUTME: Weighted sum of multiple integer inputs
# ABOUTME: Outputs y = k[1]*u[1] + k[2]*u[2] + ... + k[n]*u[n]
from typing import Any, Dict, List
from cdl_python.base import CDLBlock


class MultiSum(CDLBlock):
    """
    Weighted sum of integers: y = k[1]*u[1] + k[2]*u[2] + ... + k[n]*u[n]

    Computes weighted sum of multiple inputs with gain factors.

    Parameters:
        k: List of gain factors for each input (default: all ones)

    Inputs:
        u: List of integer inputs

    Outputs:
        y: Weighted sum of inputs
    """

    def __init__(self, k: List[int] = None, **kwargs):
        """
        Initialize MultiSum block.

        Args:
            k: List of gain factors
        """
        super().__init__(**kwargs)
        self.k = k if k is not None else []

    def compute(self, u: List[int]) -> Dict[str, Any]:
        """
        Compute weighted sum of inputs.

        Args:
            u: List of integer inputs

        Returns:
            Dictionary with key 'y' containing weighted sum
        """
        if len(u) == 0:
            return {'y': 0}

        # Compute weighted sum: sum(k[i] * u[i])
        result = sum(k_i * u_i for k_i, u_i in zip(self.k, u))
        return {'y': result}
