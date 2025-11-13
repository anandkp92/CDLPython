# ABOUTME: IntegerScalarReplicator - Replicate integer scalar to vector
from typing import Any, Dict
from cdl_python.base import CDLBlock


class IntegerScalarReplicator(CDLBlock):
    """Replicate integer scalar to vector

    Creates output vector by replicating scalar input nout times.
    Example: u=5, nout=3 → y=[5,5,5]
    """

    def __init__(self, nout: int = 1):
        """Initialize IntegerScalarReplicator block

        Args:
            nout: Number of output elements
        """
        super().__init__()
        self.nout = nout

    def compute(self, u: int) -> Dict[str, Any]:
        """Replicate u

        Args:
            u: Input scalar

        Returns:
            Dictionary with 'y': replicated vector
        """
        return {'y': [u] * self.nout}
