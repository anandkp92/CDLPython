"""
Logical (Boolean) time table source block.

Table look-up with respect to time with constant segments, outputs boolean values.
"""

from typing import Dict, Any, List
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager
from cdl_python.CDL.Integers.Sources.TimeTable import TimeTable as IntegerTimeTable


class TimeTable(CDLBlock):
    """Table look-up with respect to time with constant segments for Boolean values

    Block that outputs True/False time table values. Internally uses integer time table
    and converts to boolean (value > 0 => True).

    The table format is:
        table = [[time1, value1_1, value1_2, ...],
                 [time2, value2_1, value2_2, ...],
                 ...]

    where the first column is time (in seconds if timeScale=1) and remaining
    columns are 0 (False) or 1 (True).

    The table is repeated periodically with the specified period.

    Parameters:
        table: Table matrix (time = first column, 0/1 values = remaining columns)
        timeScale: Time scale of first column (default=1, set to 3600 if time in hours)
        period: Periodicity of table (seconds, must be > 0)

    Outputs:
        y: Output with tabulated boolean values (list if multiple columns, single value if one column)
    """

    def __init__(self, time_manager: TimeManager, table: List[List[float]],
                 timeScale: float = 1.0, period: float = 86400.0):
        """Initialize TimeTable block

        Args:
            time_manager: Time manager for getting current time
            table: Table matrix with time in first column and 0/1 values in other columns
            timeScale: Time scale of first column (e.g., 3600 for hours)
            period: Periodicity of table (seconds)
        """
        super().__init__(time_manager)

        # Validate that all values are 0 or 1
        for i, row in enumerate(table):
            for j, val in enumerate(row[1:], start=1):
                if not (abs(val) < 1e-6 or abs(val - 1.0) < 1e-6):
                    raise ValueError(f"Table value table[{i}, {j}] = {val} is not 0 or 1")

        # Create internal integer time table
        self._int_time_table = IntegerTimeTable(
            time_manager=time_manager,
            table=table,
            timeScale=timeScale,
            period=period
        )

    def compute(self) -> Dict[str, Any]:
        """Compute table output

        Returns:
            Dictionary with 'y': boolean table value(s) at current time
        """
        # Get integer output
        int_output = self._int_time_table.compute()

        # Convert to boolean (> 0 => True)
        y_val = int_output['y']

        if isinstance(y_val, list):
            # Multiple outputs
            bool_vals = [val > 0 for val in y_val]
            return {'y': bool_vals}
        else:
            # Single output
            return {'y': y_val > 0}
