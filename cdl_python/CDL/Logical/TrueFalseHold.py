# ABOUTME: TrueFalseHold block - holds true/false signals for specified durations
# ABOUTME: Prevents rapid switching by holding each state for a minimum time
from typing import Any, Dict, Optional
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class TrueFalseHold(CDLBlock):
    """
    TrueFalseHold block

    Holds a true or false signal for at least a defined time period.
    When input switches to true, output switches and remains true for
    at least trueHoldDuration. When input switches to false, output
    switches and remains false for at least falseHoldDuration.

    Parameters:
        trueHoldDuration: Duration to hold true signal (seconds)
        falseHoldDuration: Duration to hold false signal (seconds, defaults to trueHoldDuration)

    Inputs:
        u: Boolean input signal

    Outputs:
        y: Boolean output with hold behavior
    """

    def __init__(
        self,
        time_manager: Optional[TimeManager] = None,
        trueHoldDuration: float = 0.0,
        falseHoldDuration: Optional[float] = None
    ):
        """
        Initialize TrueFalseHold block.

        Args:
            time_manager: TimeManager instance
            trueHoldDuration: Duration to hold true (seconds)
            falseHoldDuration: Duration to hold false (seconds), defaults to trueHoldDuration
        """
        super().__init__(time_manager)
        self.trueHoldDuration = trueHoldDuration
        self.falseHoldDuration = falseHoldDuration if falseHoldDuration is not None else trueHoldDuration
        self._y = False
        self._entry_time = None  # Time when output last changed
        self._prev_u = False
        self._initialized = False

    def compute(self, u: bool) -> Dict[str, Any]:
        """
        Compute output with hold behavior.

        Args:
            u: Boolean input

        Returns:
            Dictionary with key 'y' containing output with hold
        """
        current_time = self.get_time()

        # On first call, output equals input
        if not self._initialized:
            self._y = u
            self._prev_u = u
            self._entry_time = current_time
            self._initialized = True
            return {'y': self._y}

        # Calculate how long output has been in current state
        time_in_current_state = current_time - self._entry_time

        # Determine if output can switch based on hold duration
        can_switch_from_true = (
            self._y is True and
            time_in_current_state >= self.trueHoldDuration and
            u is False
        )
        can_switch_from_false = (
            self._y is False and
            time_in_current_state >= self.falseHoldDuration and
            u is True
        )

        # Update output if conditions are met
        if can_switch_from_true:
            self._y = False
            self._entry_time = current_time
        elif can_switch_from_false:
            self._y = True
            self._entry_time = current_time

        # Update previous input
        self._prev_u = u

        return {'y': self._y}

    def reset_state(self):
        """Reset the block state"""
        self._y = False
        self._entry_time = None
        self._prev_u = False
        self._initialized = False
