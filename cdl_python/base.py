# ABOUTME: Base class for all CDL blocks providing common interface and state management.
# ABOUTME: Separates control logic from time management using TimeManager queries.

from typing import Any, Dict, Optional
from cdl_python.time_manager import TimeManager


class CDLBlock:
    """
    Base class for all CDL elementary blocks.

    Provides:
    - Access to TimeManager for time-dependent blocks
    - State persistence between compute() calls
    - Common interface for all blocks

    Subclasses must implement compute() method.
    """

    def __init__(self, time_manager: Optional[TimeManager] = None):
        """
        Initialize CDL block.

        Args:
            time_manager: TimeManager instance (optional, but required for stateful blocks)
        """
        self.time_manager = time_manager
        self._state: Dict[str, Any] = {}

    def compute(self, **inputs) -> Dict[str, Any]:
        """
        Compute block outputs from inputs.

        This is the main computation method that subclasses must override.
        Should be pure logic: inputs -> outputs, using self._state for persistence.

        Args:
            **inputs: Named input values (type depends on block)

        Returns:
            Dictionary of output names to values

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError(
            f"{self.__class__.__name__}.compute() must be implemented"
        )

    def reset_state(self):
        """
        Reset internal state to initial conditions.

        Subclasses should override if they need custom reset logic.
        """
        self._state = {}

    def get_time(self) -> float:
        """
        Get current time from TimeManager.

        Returns:
            Current time in seconds

        Raises:
            RuntimeError: If no TimeManager is set
        """
        if self.time_manager is None:
            raise RuntimeError(
                f"{self.__class__.__name__} requires a TimeManager for time-dependent operations"
            )
        return self.time_manager.get_time()

    def _validate_inputs(self, required_inputs: list, provided_inputs: dict):
        """
        Validate that all required inputs are provided.

        Args:
            required_inputs: List of required input names
            provided_inputs: Dictionary of provided inputs

        Raises:
            ValueError: If required inputs are missing
        """
        missing = set(required_inputs) - set(provided_inputs.keys())
        if missing:
            raise ValueError(
                f"{self.__class__.__name__} missing required inputs: {missing}"
            )

    def _initialize_state_if_needed(self, **defaults):
        """
        Initialize state variables if not already set.

        Args:
            **defaults: Default values for state variables
        """
        for key, value in defaults.items():
            if key not in self._state:
                self._state[key] = value
