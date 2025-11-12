# ABOUTME: RealScalarReplicator - Replicate scalar to vector
# ABOUTME: Returns array filled with input value
from typing import Any, Dict, List
from cdl_python.base import CDLBlock


class RealScalarReplicator(CDLBlock):
    """
    Real signal replicator

    Replicates a scalar Real input to an array of identical outputs.

    Parameters:
        nout: Number of outputs

    Inputs:
        u: Scalar input to replicate

    Outputs:
        y: Vector of replicated values [u, u, ..., u]
    """

    def __init__(self, nout: int = 1):
        """
        Initialize RealScalarReplicator.

        Args:
            nout: Number of outputs
        """
        super().__init__()
        self.nout = nout

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Replicate scalar to vector.

        Args:
            u: Scalar input

        Returns:
            Dictionary with 'y' containing [u, u, ..., u]
        """
        return {'y': [u] * self.nout}
