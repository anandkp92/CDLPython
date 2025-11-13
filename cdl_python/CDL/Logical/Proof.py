# ABOUTME: Proof - Verify boolean signal matches setpoint and detect locked conditions
from typing import Any, Dict
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class Proof(CDLBlock):
    """Proof block - verifies boolean signals and detects locked conditions

    Verifies that a measured boolean signal (u) matches the setpoint (uSet).
    Detects when equipment is locked in on or off position.

    The block monitors:
    - Whether the signal matches the setpoint after a test delay
    - Whether signal is locked on (stuck at true) for extended time
    - Whether signal is locked off (stuck at false) for extended time

    Used for:
    - Equipment health monitoring
    - Fault detection (stuck dampers, valves, etc.)
    - Control sequence verification
    - Safety interlocks
    """

    def __init__(
        self,
        time_manager: TimeManager,
        delTes: float = 180.0,
        delTim: float = 3600.0
    ):
        """Initialize Proof block

        Args:
            time_manager: Time manager for timing
            delTes: Test delay - time to wait before testing if signal matches setpoint (seconds)
            delTim: Tracking time - duration signal must be constant to detect locked condition (seconds)
        """
        super().__init__(time_manager)
        self.delTes = delTes
        self.delTim = delTim

        # State variables
        self._last_u = None  # Use None to detect first call
        self._last_u_set = None
        self._time_at_setpoint_change = None
        self._time_u_became_true = None
        self._time_u_became_false = None
        self._previous_u = None

    def compute(self, u: bool, uSet: bool) -> Dict[str, Any]:
        """Compute proof outputs

        Args:
            u: Measured boolean signal
            uSet: Boolean setpoint

        Returns:
            Dictionary with:
                - 'yTest': True if signal matches setpoint after test delay
                - 'yLocOn': True if signal is locked on (true for > delTim)
                - 'yLocOff': True if signal is locked off (false for > delTim)
        """
        current_time = self.get_time()

        # Initialize on first call
        if self._previous_u is None:
            self._previous_u = u
            self._last_u_set = uSet
            self._time_at_setpoint_change = current_time
            if u:
                self._time_u_became_true = current_time
            else:
                self._time_u_became_false = current_time

        # Detect setpoint change
        if uSet != self._last_u_set:
            self._time_at_setpoint_change = current_time
            self._last_u_set = uSet

        # Detect signal transitions
        if u and not self._previous_u:
            # Rising edge
            self._time_u_became_true = current_time
        elif not u and self._previous_u:
            # Falling edge
            self._time_u_became_false = current_time

        self._previous_u = u

        # Test if signal matches setpoint after delay
        time_since_setpoint_change = current_time - self._time_at_setpoint_change
        if time_since_setpoint_change >= self.delTes:
            yTest = (u == uSet)
        else:
            # Still in test delay, don't fail the test yet
            yTest = True

        # Detect locked on condition (signal stuck at true)
        if u:
            if self._time_u_became_true is not None:
                time_at_true = current_time - self._time_u_became_true
                yLocOn = (time_at_true >= self.delTim)
            else:
                yLocOn = False
        else:
            yLocOn = False

        # Detect locked off condition (signal stuck at false)
        if not u:
            if self._time_u_became_false is not None:
                time_at_false = current_time - self._time_u_became_false
                yLocOff = (time_at_false >= self.delTim)
            else:
                yLocOff = False
        else:
            yLocOff = False

        return {
            'yTest': yTest,      # True if signal matches setpoint
            'yLocOn': yLocOn,    # True if locked on
            'yLocOff': yLocOff   # True if locked off
        }
