"""
Civil time source block.

Outputs the current simulation time (civil time).
"""

from typing import Dict, Any
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class CivilTime(CDLBlock):
    """Civil time block

    Block that outputs the civil time (current simulation time in seconds).

    This block outputs the time of the model. In the case of a building automation
    system, the building automation system synchronizes time, and hence needs to
    assign a value for the output of this block.

    Daylight saving time shall not be taken into account - the block always outputs
    civil time rather than daylight savings time.

    Outputs:
        y: Civil time (simulation time in seconds)
    """

    def __init__(self, time_manager: TimeManager):
        """Initialize CivilTime block

        Args:
            time_manager: Time manager for getting current time
        """
        super().__init__(time_manager)

    def compute(self) -> Dict[str, Any]:
        """Compute civil time output

        Returns:
            Dictionary with 'y': current simulation time in seconds
        """
        return {'y': self.get_time()}
