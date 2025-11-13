# ABOUTME: UnitDelay - Unit delay (z^-1 operator)
from typing import Any, Dict
from cdl_python.base import CDLBlock


class UnitDelay(CDLBlock):
    """Unit delay block - outputs previous input value

    Implements the discrete-time z^-1 operator.
    On first call, outputs y_start.
    On subsequent calls, outputs the previous input value.

    This is a fundamental discrete-time block used for:
    - Creating feedback loops
    - Implementing discrete-time filters
    - Breaking algebraic loops
    - Storing previous values
    """

    def __init__(self, y_start: float = 0.0):
        """Initialize UnitDelay block

        Args:
            y_start: Initial output value (before first input is received)
        """
        super().__init__()
        self.y_start = y_start
        self._previous_u = y_start
        self._first_call = True

    def compute(self, u: float) -> Dict[str, Any]:
        """Compute delayed output

        Args:
            u: Current input value

        Returns:
            Dictionary with 'y': previous input value (or y_start on first call)
        """
        # Output is the previous input value
        if self._first_call:
            y = self.y_start
            self._first_call = False
        else:
            y = self._previous_u

        # Store current input for next call
        self._previous_u = u

        return {'y': y}
