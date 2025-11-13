# ABOUTME: Assert - Print warning when condition becomes false
from typing import Any, Dict
import warnings
from cdl_python.base import CDLBlock


class Assert(CDLBlock):
    """Print warning message when input becomes false

    This block is used for debugging and validation in control sequences.
    When the input u becomes false, it prints a warning with the specified message.

    This is useful for:
    - Detecting unexpected conditions in control logic
    - Validating assumptions during simulation
    - Debugging control sequences
    """

    def __init__(self, message: str = "Assertion failed"):
        """Initialize Assert block

        Args:
            message: Warning message to print when assertion fails
        """
        super().__init__()
        self.message = message

    def compute(self, u: bool) -> Dict[str, Any]:
        """Check assertion and print warning if false

        Args:
            u: Boolean input to check

        Returns:
            Empty dictionary (block has no outputs)
        """
        if not u:
            warnings.warn(self.message, UserWarning, stacklevel=2)
        return {}
