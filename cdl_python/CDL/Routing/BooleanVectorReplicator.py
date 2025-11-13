# ABOUTME: BooleanVectorReplicator - Replicate boolean vector multiple times
from typing import Any, Dict, List
from cdl_python.base import CDLBlock


class BooleanVectorReplicator(CDLBlock):
    """Replicate boolean vector nrep times

    Creates output vector by concatenating input vector nrep times.
    Example: u=[T,F], nrep=3 → y=[T,F,T,F,T,F]
    """

    def __init__(self, nin: int = 1, nrep: int = 1):
        """Initialize BooleanVectorReplicator block

        Args:
            nin: Number of input elements
            nrep: Number of times to replicate
        """
        super().__init__()
        self.nin = nin
        self.nrep = nrep
        self.nout = nin * nrep

    def compute(self, u: List[bool]) -> Dict[str, Any]:
        """Replicate u nrep times

        Args:
            u: Input vector

        Returns:
            Dictionary with 'y': replicated vector
        """
        y = u * self.nrep  # [u1, u2] * 2 = [u1, u2, u1, u2]
        return {'y': y}
