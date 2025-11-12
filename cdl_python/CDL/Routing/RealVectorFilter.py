# ABOUTME: RealVectorFilter - Filter vector by boolean mask
# ABOUTME: Extracts elements where mask is True
from typing import Any, Dict, List
from cdl_python.base import CDLBlock


class RealVectorFilter(CDLBlock):
    """
    Filter a real vector based on a boolean mask

    Parameters:
        nin: Size of input vector
        nout: Size of output vector (must match number of True values in mask)
        msk: Boolean mask array

    Inputs:
        u: Input vector

    Outputs:
        y: Filtered output with elements where msk is True
    """

    def __init__(self, nin: int, nout: int, msk: List[bool] = None):
        """
        Initialize RealVectorFilter.

        Args:
            nin: Size of input vector
            nout: Size of output vector
            msk: Boolean mask (defaults to all True)
        """
        super().__init__()
        self.nin = nin
        self.nout = nout
        self.msk = msk if msk is not None else [True] * nin

        # Validate that nout matches number of True values in mask
        true_count = sum(1 for m in self.msk if m)
        if true_count != nout:
            raise ValueError(f"nout={nout} must equal number of True values in mask ({true_count})")

    def compute(self, u: List[float]) -> Dict[str, Any]:
        """
        Filter vector by mask.

        Args:
            u: Input vector

        Returns:
            Dictionary with 'y' containing filtered values
        """
        y = [u[i] for i in range(self.nin) if self.msk[i]]
        return {'y': y}
