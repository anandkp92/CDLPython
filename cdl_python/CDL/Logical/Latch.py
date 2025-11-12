# ABOUTME: SR latch block
# ABOUTME: Maintains true signal until cleared, set-reset flip-flop
from typing import Any, Dict
from cdl_python.base import CDLBlock


class Latch(CDLBlock):
    """
    SR Latch block

    Sets output to true on rising edge of u (if clr is false).
    Clears output to false on rising edge of clr.
    Maintains state between edges.

    Inputs:
        u: Latch (set) input
        clr: Clear (reset) input

    Outputs:
        y: Latched output signal
    """

    def __init__(self, **kwargs):
        """Initialize Latch block."""
        super().__init__(**kwargs)
        self._y = False
        self._prev_u = False
        self._prev_clr = False

    def compute(self, u: bool, clr: bool) -> Dict[str, Any]:
        """
        Compute latch output.

        Args:
            u: Latch input
            clr: Clear input

        Returns:
            Dictionary with key 'y' containing the latched output
        """
        # Detect rising edges
        u_rising = u and not self._prev_u
        clr_rising = clr and not self._prev_clr

        # Clear takes priority
        if clr_rising or clr:
            self._y = False
        # Set on rising edge of u when clr is false
        elif u_rising and not clr:
            self._y = True
        # Otherwise maintain state

        # Update previous values
        self._prev_u = u
        self._prev_clr = clr

        return {'y': self._y}

    def reset_state(self):
        """Reset the block state"""
        self._y = False
        self._prev_u = False
        self._prev_clr = False
