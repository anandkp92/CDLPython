# ABOUTME: Sort block - sorts elements in ascending or descending order
# ABOUTME: Returns sorted values and indices
from typing import Any, Dict, List
import numpy as np
from cdl_python.base import CDLBlock


class Sort(CDLBlock):
    """
    Sort block

    Sorts input vector in ascending or descending order.
    Also returns indices of sorted elements.

    Parameters:
        ascending: If true, sort in ascending order; otherwise descending (default: True)

    Inputs:
        u: List of real values to sort

    Outputs:
        y: Sorted values
        yIdx: 1-based indices of sorted elements with respect to original vector
    """

    def __init__(self, ascending: bool = True, **kwargs):
        """
        Initialize Sort block.

        Args:
            ascending: Sort order (True for ascending, False for descending)
        """
        super().__init__(**kwargs)
        self.ascending = ascending

    def compute(self, u: List[float]) -> Dict[str, Any]:
        """
        Sort input vector.

        Args:
            u: List of values to sort

        Returns:
            Dictionary with keys 'y' (sorted values) and 'yIdx' (1-based indices)
        """
        if len(u) == 0:
            return {'y': [], 'yIdx': []}

        # Get indices that would sort the array (0-based)
        indices = np.argsort(u)

        # Reverse if descending
        if not self.ascending:
            indices = indices[::-1]

        # Sort the values
        y = [u[i] for i in indices]

        # Convert to 1-based indices (Modelica convention)
        yIdx = [i + 1 for i in indices]

        return {'y': y, 'yIdx': yIdx}
