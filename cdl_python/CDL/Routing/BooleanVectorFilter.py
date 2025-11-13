# ABOUTME: BooleanVectorFilter - Filter boolean vector by boolean mask
from typing import Any, Dict, List
from cdl_python.base import CDLBlock


class BooleanVectorFilter(CDLBlock):
    """Filter boolean vector by boolean mask

    Filters input vector by keeping only elements where mask is True.
    Example: u=[T,F,T,F], msk=[True,False,True,False] → y=[T,T]
    """

    def __init__(self, nin: int, nout: int, msk: List[bool] = None):
        """Initialize BooleanVectorFilter block

        Args:
            nin: Number of input elements
            nout: Number of output elements (must equal True count in mask)
            msk: Boolean mask (default: all True)
        """
        super().__init__()
        self.nin = nin
        self.nout = nout
        self.msk = msk if msk is not None else [True] * nin

        true_count = sum(1 for m in self.msk if m)
        if true_count != nout:
            raise ValueError(f"nout must equal True count in mask (got nout={nout}, True count={true_count})")

    def compute(self, u: List[bool]) -> Dict[str, Any]:
        """Filter u by mask

        Args:
            u: Input vector

        Returns:
            Dictionary with 'y': filtered vector
        """
        y = [u[i] for i in range(self.nin) if self.msk[i]]
        return {'y': y}
