# ABOUTME: MatrixMax block - finds maximum value in a vector
# ABOUTME: Returns the largest element from the input vector
from typing import Any, Dict, List
from cdl_python.base import CDLBlock


class MatrixMax(CDLBlock):
    """
    Matrix maximum block

    Finds and returns the maximum value from input vector.

    Inputs:
        u: Input vector

    Outputs:
        y: Maximum value from input vector
    """

    def compute(self, u: List[float]) -> Dict[str, Any]:
        """
        Find maximum value in input vector.

        Args:
            u: Input vector

        Returns:
            Dictionary with key 'y' containing maximum value
        """
        if len(u) == 0:
            raise ValueError("Input vector cannot be empty")

        return {'y': max(u)}
