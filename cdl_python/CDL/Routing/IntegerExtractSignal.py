# ABOUTME: IntegerExtractSignal - Extract scalar from integer vector by index parameter
from typing import Any, Dict, List
from cdl_python.base import CDLBlock


class IntegerExtractSignal(CDLBlock):
    """Extract scalar from integer vector by index parameter

    Extracts the element at position 'extract' from the input vector.
    Index is 1-based and clamped to valid range [1, nin].
    """

    def __init__(self, nin: int = 1, extract: int = 1):
        """Initialize IntegerExtractSignal block

        Args:
            nin: Number of input elements
            extract: Index of element to extract (1-based)
        """
        super().__init__()
        self.nin = nin
        self.extract = extract

    def compute(self, u: List[int]) -> Dict[str, Any]:
        """Extract u[extract]

        Args:
            u: Input vector

        Returns:
            Dictionary with 'y': extracted value
        """
        clamped = max(1, min(self.nin, self.extract))
        return {'y': u[clamped - 1]}
