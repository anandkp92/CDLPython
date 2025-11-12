# ABOUTME: Matrix gain block - multiplies input vector by gain matrix
# ABOUTME: Computes y = K * u where K is a matrix and u is a vector
from typing import Any, Dict, List
import numpy as np
from cdl_python.base import CDLBlock


class MatrixGain(CDLBlock):
    """
    Matrix gain block

    Multiplies input vector by a gain matrix: y = K * u

    Parameters:
        K: Gain matrix (default: identity matrix [[1, 0], [0, 1]])

    Inputs:
        u: Input vector

    Outputs:
        y: Output vector (K * u)
    """

    def __init__(self, K: List[List[float]] = None, **kwargs):
        """
        Initialize MatrixGain block.

        Args:
            K: Gain matrix
        """
        super().__init__(**kwargs)
        if K is None:
            K = [[1.0, 0.0], [0.0, 1.0]]
        self.K = np.array(K)

    def compute(self, u: List[float]) -> Dict[str, Any]:
        """
        Multiply input vector by gain matrix.

        Args:
            u: Input vector

        Returns:
            Dictionary with key 'y' containing output vector
        """
        u_array = np.array(u)
        y = self.K @ u_array
        return {'y': y.tolist()}
