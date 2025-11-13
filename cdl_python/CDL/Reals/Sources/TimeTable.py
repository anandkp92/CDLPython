"""
Real-valued time table source block.

Table look-up with respect to time with configurable interpolation and extrapolation.
"""

from typing import Dict, Any, List
import numpy as np
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager
from enum import Enum


class Smoothness(Enum):
    """Table interpolation method"""
    LINEAR_SEGMENTS = "LinearSegments"
    CONSTANT_SEGMENTS = "ConstantSegments"


class Extrapolation(Enum):
    """Table extrapolation method"""
    PERIODIC = "Periodic"
    HOLD_LAST_POINT = "HoldLastPoint"
    LAST_TWO_POINTS = "LastTwoPoints"


class TimeTable(CDLBlock):
    """Table look-up with respect to time with interpolation and extrapolation

    Block that outputs Real time table values with configurable interpolation
    and extrapolation.

    The table format is:
        table = [[time1, value1_1, value1_2, ...],
                 [time2, value2_1, value2_2, ...],
                 ...]

    where the first column is time (in seconds if timeScale=1) and remaining
    columns are the table values.

    Parameters:
        table: Table matrix (time = first column, values = remaining columns)
        smoothness: Interpolation method (LINEAR_SEGMENTS or CONSTANT_SEGMENTS)
        extrapolation: Extrapolation method (PERIODIC, HOLD_LAST_POINT, or LAST_TWO_POINTS)
        offset: Offset added to output values (list with length = number of output columns)
        timeScale: Time scale of first column (default=1, set to 3600 if time in hours)

    Outputs:
        y: Output with tabulated values (list if multiple columns, single value if one column)
    """

    def __init__(self, time_manager: TimeManager, table: List[List[float]],
                 smoothness: Smoothness = Smoothness.LINEAR_SEGMENTS,
                 extrapolation: Extrapolation = Extrapolation.PERIODIC,
                 offset: List[float] = None,
                 timeScale: float = 1.0):
        """Initialize TimeTable block

        Args:
            time_manager: Time manager for getting current time
            table: Table matrix with time in first column and values in other columns
            smoothness: Interpolation method
            extrapolation: Extrapolation method
            offset: Offset for each output column (default: all zeros)
            timeScale: Time scale of first column (e.g., 3600 for hours)
        """
        super().__init__(time_manager)

        if not table or len(table) == 0:
            raise ValueError("Table must have at least one row")

        if any(len(row) < 2 for row in table):
            raise ValueError("Table must have at least 2 columns (time + at least one value)")

        # Convert to numpy array
        self.table = np.array(table, dtype=float)
        self.smoothness = smoothness
        self.extrapolation = extrapolation
        self.timeScale = timeScale

        # Extract time stamps and scale them
        self.time_stamps = self.table[:, 0] * timeScale
        # Extract values
        self.values = self.table[:, 1:]

        # Number of outputs
        self.nout = self.values.shape[1]

        # Set offset
        if offset is None:
            self.offset = np.zeros(self.nout)
        else:
            if len(offset) != self.nout:
                raise ValueError(f"offset length ({len(offset)}) must match number of output columns ({self.nout})")
            self.offset = np.array(offset)

        # Time range
        self.time_range = self.time_stamps[-1] - self.time_stamps[0]

        # For periodic extrapolation, compute t0
        if extrapolation == Extrapolation.PERIODIC and self.time_range > 0:
            # Align start time to make it periodic
            self.t0 = 0.0  # Simplified - could round to align periods
        else:
            self.t0 = 0.0

    def _interpolate(self, t: float) -> np.ndarray:
        """Interpolate table values at time t

        Args:
            t: Time value

        Returns:
            Interpolated values as numpy array
        """
        # Handle extrapolation
        if t < self.time_stamps[0]:
            # Before first point
            if self.extrapolation == Extrapolation.HOLD_LAST_POINT:
                return self.values[0, :]
            elif self.extrapolation == Extrapolation.LAST_TWO_POINTS:
                # Extrapolate using first two points
                if len(self.time_stamps) >= 2:
                    dt = self.time_stamps[1] - self.time_stamps[0]
                    dv = self.values[1, :] - self.values[0, :]
                    dt_extrap = t - self.time_stamps[0]
                    return self.values[0, :] + (dt_extrap / dt) * dv
                else:
                    return self.values[0, :]
            else:  # PERIODIC
                # Wrap time into periodic range
                if self.time_range > 0:
                    t = self.time_stamps[0] + ((t - self.time_stamps[0]) % self.time_range)
                else:
                    return self.values[0, :]

        elif t > self.time_stamps[-1]:
            # After last point
            if self.extrapolation == Extrapolation.HOLD_LAST_POINT:
                return self.values[-1, :]
            elif self.extrapolation == Extrapolation.LAST_TWO_POINTS:
                # Extrapolate using last two points
                if len(self.time_stamps) >= 2:
                    dt = self.time_stamps[-1] - self.time_stamps[-2]
                    dv = self.values[-1, :] - self.values[-2, :]
                    dt_extrap = t - self.time_stamps[-1]
                    return self.values[-1, :] + (dt_extrap / dt) * dv
                else:
                    return self.values[-1, :]
            else:  # PERIODIC
                # Wrap time into periodic range
                if self.time_range > 0:
                    t = self.time_stamps[0] + ((t - self.time_stamps[0]) % self.time_range)
                else:
                    return self.values[-1, :]

        # t is within table range - find surrounding points
        idx = np.searchsorted(self.time_stamps, t, side='right') - 1
        idx = max(0, min(idx, len(self.time_stamps) - 2))

        if self.smoothness == Smoothness.CONSTANT_SEGMENTS:
            # Zero-order hold (constant segments)
            return self.values[idx, :]
        else:
            # Linear interpolation
            t0, t1 = self.time_stamps[idx], self.time_stamps[idx + 1]
            v0, v1 = self.values[idx, :], self.values[idx + 1, :]

            if abs(t1 - t0) < 1e-12:
                # Time stamps are equal, return first value
                return v0
            else:
                # Linear interpolation
                alpha = (t - t0) / (t1 - t0)
                return v0 + alpha * (v1 - v0)

    def compute(self) -> Dict[str, Any]:
        """Compute table output

        Returns:
            Dictionary with 'y': table value(s) at current time (with offset applied)
        """
        current_time = self.get_time()

        # Interpolate
        values = self._interpolate(current_time)

        # Apply offset
        values = values + self.offset

        # Return single value if only one output, otherwise return array
        if self.nout == 1:
            return {'y': float(values[0])}
        else:
            return {'y': values.tolist()}
