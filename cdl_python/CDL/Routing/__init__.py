"""CDL Routing Package - Array and vector manipulation blocks

This package provides blocks for routing, extracting, replicating, and filtering
array/vector signals.

Block Types:
- Extractors: Extract single element by index
- ExtractSignal: Extract single element by parameter
- ScalarReplicators: Replicate scalar to vector
- VectorReplicators: Replicate entire vector
- VectorFilters: Filter vector by boolean mask

Each block type is available for Real, Integer, and Boolean data types.
"""

# Real routing blocks
from .RealExtractor import RealExtractor
from .RealExtractSignal import RealExtractSignal
from .RealScalarReplicator import RealScalarReplicator
from .RealVectorFilter import RealVectorFilter
from .RealVectorReplicator import RealVectorReplicator

# Integer routing blocks
from .IntegerExtractor import IntegerExtractor
from .IntegerExtractSignal import IntegerExtractSignal
from .IntegerScalarReplicator import IntegerScalarReplicator
from .IntegerVectorFilter import IntegerVectorFilter
from .IntegerVectorReplicator import IntegerVectorReplicator

# Boolean routing blocks
from .BooleanExtractor import BooleanExtractor
from .BooleanExtractSignal import BooleanExtractSignal
from .BooleanScalarReplicator import BooleanScalarReplicator
from .BooleanVectorFilter import BooleanVectorFilter
from .BooleanVectorReplicator import BooleanVectorReplicator

__all__ = [
    # Real blocks
    'RealExtractor',
    'RealExtractSignal',
    'RealScalarReplicator',
    'RealVectorFilter',
    'RealVectorReplicator',
    # Integer blocks
    'IntegerExtractor',
    'IntegerExtractSignal',
    'IntegerScalarReplicator',
    'IntegerVectorFilter',
    'IntegerVectorReplicator',
    # Boolean blocks
    'BooleanExtractor',
    'BooleanExtractSignal',
    'BooleanScalarReplicator',
    'BooleanVectorFilter',
    'BooleanVectorReplicator',
]
