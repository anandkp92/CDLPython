# ABOUTME: BooleanScalarReplicator - Replicate boolean scalar to vector
from typing import Any, Dict
from cdl_python.base import CDLBlock


class BooleanScalarReplicator(CDLBlock):
    """Replicate boolean scalar to vector

    Creates output vector by replicating scalar input nout times.
    Example: u=True, nout=3 → y=[True,True,True]
    """

    def __init__(self, nout: int = 1):
        """Initialize BooleanScalarReplicator block

        Args:
            nout: Number of output elements
        """
        super().__init__()
        self.nout = nout

    def compute(self, u: bool) -> Dict[str, Any]:
        """Replicate u

        Args:
            u: Input scalar

        Returns:
            Dictionary with 'y': replicated vector
        """
        return {'y': [u] * self.nout}
