# ABOUTME: MatrixMin block - finds minimum value in a vector
# ABOUTME: Returns the smallest element from the input vector
from typing import Any, Dict, List
from cdl_python.base import CDLBlock


class MatrixMin(CDLBlock):
    """
    Matrix minimum block

    Finds and returns the minimum value from input vector.

    Inputs:
        u: Input vector

    Outputs:
        y: Minimum value from input vector
    """

    def compute(self, u: List[float]) -> Dict[str, Any]:
        """
        Find minimum value in input vector.

        Args:
            u: Input vector

        Returns:
            Dictionary with key 'y' containing minimum value
        """
        if len(u) == 0:
            raise ValueError("Input vector cannot be empty")

        return {'y': min(u)}
