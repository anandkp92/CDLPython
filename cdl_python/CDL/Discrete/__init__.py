"""CDL Discrete Package - Discrete-time sampling and delay blocks

This package provides blocks for discrete-time signal processing including:
- Sampling: Convert continuous signals to discrete
- Hold: Maintain sampled values
- Delay: Time-shift signals
- Triggered operations: Event-driven processing

Blocks:
- Sampler: Sample at fixed intervals
- UnitDelay: z^-1 delay operator
- ZeroOrderHold: Staircase (piecewise constant) output
- FirstOrderHold: Linear interpolation between samples
- TriggeredSampler: Sample on boolean trigger
- TriggeredMax: Track maximum between triggers
- TriggeredMovingMean: Average between triggers
"""

from .Sampler import Sampler
from .UnitDelay import UnitDelay
from .ZeroOrderHold import ZeroOrderHold
from .FirstOrderHold import FirstOrderHold
from .TriggeredSampler import TriggeredSampler
from .TriggeredMax import TriggeredMax
from .TriggeredMovingMean import TriggeredMovingMean

__all__ = [
    'Sampler',
    'UnitDelay',
    'ZeroOrderHold',
    'FirstOrderHold',
    'TriggeredSampler',
    'TriggeredMax',
    'TriggeredMovingMean',
]
