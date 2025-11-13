# ABOUTME: RealVectorReplicator - Replicate real vector multiple times
from typing import Any, Dict, List
from cdl_python.base import CDLBlock


class RealVectorReplicator(CDLBlock):
    """Replicate real vector nrep times

    Creates output vector by concatenating input vector nrep times.
    Example: u=[1,2], nrep=3 → y=[1,2,1,2,1,2]
    """

    def __init__(self, nin: int = 1, nrep: int = 1):
        """Initialize RealVectorReplicator block

        Args:
            nin: Number of input elements
            nrep: Number of times to replicate
        """
        super().__init__()
        self.nin = nin
        self.nrep = nrep
        self.nout = nin * nrep

    def compute(self, u: List[float]) -> Dict[str, Any]:
        """Replicate u nrep times

        Args:
            u: Input vector

        Returns:
            Dictionary with 'y': replicated vector
        """
        y = u * self.nrep  # [u1, u2] * 2 = [u1, u2, u1, u2]
        return {'y': y}
