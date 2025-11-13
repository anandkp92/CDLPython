"""
Integer time table source block.

Table look-up with respect to time with constant segments (piecewise constant).
"""

from typing import Dict, Any, List
import numpy as np
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class TimeTable(CDLBlock):
    """Table look-up with respect to time with constant segments

    Block that outputs Integer time table values. The table is repeated
    periodically with the specified period.

    The table format is:
        table = [[time1, value1_1, value1_2, ...],
                 [time2, value2_1, value2_2, ...],
                 ...]

    where the first column is time (in seconds if timeScale=1) and remaining
    columns are the table values.

    Until a new tabulated value is set, the previous tabulated value is returned
    (piecewise constant / zero-order hold).

    Parameters:
        table: Table matrix (time = first column, values = remaining columns)
        timeScale: Time scale of first column (default=1, set to 3600 if time in hours)
        period: Periodicity of table (seconds, must be > 0)

    Outputs:
        y: Output with tabulated values (list if multiple columns, single value if one column)
    """

    def __init__(self, time_manager: TimeManager, table: List[List[float]],
                 timeScale: float = 1.0, period: float = 86400.0):
        """Initialize TimeTable block

        Args:
            time_manager: Time manager for getting current time
            table: Table matrix with time in first column and values in other columns
            timeScale: Time scale of first column (e.g., 3600 for hours)
            period: Periodicity of table (seconds)
        """
        super().__init__(time_manager)

        if not table or len(table) == 0:
            raise ValueError("Table must have at least one row")

        if any(len(row) < 2 for row in table):
            raise ValueError("Table must have at least 2 columns (time + at least one value)")

        # Convert to numpy array for easier manipulation
        self.table = np.array(table, dtype=float)
        self.timeScale = timeScale
        self.period = period

        # Extract time stamps and scale them
        self.time_stamps = self.table[:, 0] * timeScale
        # Extract values and convert to integers
        self.values = np.round(self.table[:, 1:]).astype(int)

        # Number of outputs
        self.nout = self.values.shape[1]

        # Validate
        if not np.isclose(self.time_stamps[0], 0.0, atol=1e-6):
            raise ValueError("First time stamp must be zero")

        if self.time_stamps[-1] >= period:
            raise ValueError(f"Last time stamp ({self.time_stamps[-1]}) must be smaller than period ({period})")

        # Verify all values are integers
        if not np.allclose(self.table[:, 1:], np.round(self.table[:, 1:]), atol=1e-6):
            raise ValueError("All table values must be integers")

    def _get_index(self, t: float) -> int:
        """Get the index for table lookup

        Args:
            t: Current time

        Returns:
            Index in table for current time
        """
        # Shift time to be within period
        t_shifted = t % self.period

        # Find the last time stamp that is <= t_shifted
        # Using searchsorted with side='right' gives us index where t_shifted would be inserted
        # We want the index before that (the last value <= t_shifted)
        idx = np.searchsorted(self.time_stamps, t_shifted + 1e-6, side='right') - 1

        # Clamp to valid range
        idx = max(0, min(idx, len(self.time_stamps) - 1))

        return idx

    def compute(self) -> Dict[str, Any]:
        """Compute table output

        Returns:
            Dictionary with 'y': table value(s) at current time
        """
        current_time = self.get_time()

        # Get index for current time
        idx = self._get_index(current_time)

        # Get values
        values = self.values[idx, :]

        # Return single value if only one output, otherwise return array
        if self.nout == 1:
            return {'y': int(values[0])}
        else:
            return {'y': values.tolist()}
