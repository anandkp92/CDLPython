# ABOUTME: RealExtractor - Extract scalar from real vector by index
# ABOUTME: Returns u[index] with bounds checking
from typing import Any, Dict, List
from cdl_python.base import CDLBlock


class RealExtractor(CDLBlock):
    """
    Extract scalar signal out of real signal vector dependent on integer input index

    Parameters:
        nin: Number of inputs in the vector

    Inputs:
        u: Real input vector
        index: Index of element to extract (1-based indexing like Modelica)

    Outputs:
        y: Extracted value u[index], clamped to valid range [1, nin]
    """

    def __init__(self, nin: int = 1):
        """
        Initialize RealExtractor.

        Args:
            nin: Number of inputs in the vector
        """
        super().__init__()
        self.nin = nin

    def compute(self, u: List[float], index: int) -> Dict[str, Any]:
        """
        Extract element from vector by index.

        Args:
            u: Input vector of real values
            index: 1-based index (Modelica convention)

        Returns:
            Dictionary with 'y' containing u[index]
        """
        # Clamp index to valid range [1, nin] (Modelica 1-based indexing)
        clamped_index = max(1, min(self.nin, index))
        # Convert to Python 0-based indexing
        py_index = clamped_index - 1
        return {'y': u[py_index]}
