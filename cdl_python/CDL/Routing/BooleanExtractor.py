# ABOUTME: BooleanExtractor - Extract scalar from boolean vector by index
from typing import Any, Dict, List
from cdl_python.base import CDLBlock


class BooleanExtractor(CDLBlock):
    """Extract scalar from boolean vector by index

    Extracts the element at position 'index' from the input vector.
    Index is 1-based and clamped to valid range [1, nin].
    """

    def __init__(self, nin: int = 1):
        """Initialize BooleanExtractor block

        Args:
            nin: Number of input elements
        """
        super().__init__()
        self.nin = nin

    def compute(self, u: List[bool], index: int) -> Dict[str, Any]:
        """Extract u[index]

        Args:
            u: Input vector
            index: Index to extract (1-based)

        Returns:
            Dictionary with 'y': extracted value
        """
        clamped = max(1, min(self.nin, index))
        return {'y': u[clamped - 1]}
