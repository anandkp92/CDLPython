# ABOUTME: Toggle block
# ABOUTME: Toggles output on each rising edge of input
from typing import Any, Dict
from cdl_python.base import CDLBlock


class Toggle(CDLBlock):
    """
    Toggle block

    Toggles output between true and false on each rising edge of u.
    Can be cleared to false with clr input.

    Inputs:
        u: Toggle input
        clr: Clear input

    Outputs:
        y: Toggled output signal
    """

    def __init__(self, **kwargs):
        """Initialize Toggle block."""
        super().__init__(**kwargs)
        self._y = False
        self._prev_u = False
        self._prev_clr = False

    def compute(self, u: bool, clr: bool) -> Dict[str, Any]:
        """
        Compute toggle output.

        Args:
            u: Toggle input
            clr: Clear input

        Returns:
            Dictionary with key 'y' containing the toggled output
        """
        # Detect rising edges
        u_rising = u and not self._prev_u
        clr_rising = clr and not self._prev_clr

        # Clear takes priority
        if clr_rising or clr:
            self._y = False
        # Toggle on rising edge of u when clr is false
        elif u_rising and not clr:
            self._y = not self._y
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
