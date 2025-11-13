"""CDL to Python Translator

Translates Control Description Language (CDL) models from CXF JSON format
to executable Python code using the CDL Python library.

Main components:
- parser: CXF JSON parser
- model: Internal model representation
- codegen: Python code generator
- cli: Command-line interface
"""

__version__ = "0.1.0"

from cdl_translator.parser import CXFParser
from cdl_translator.codegen import CodeGenerator
from cdl_translator.model import (
    CDLModel,
    ModelMetadata,
    BlockInstance,
    Connection,
    Parameter,
    Port,
)

__all__ = [
    "CXFParser",
    "CodeGenerator",
    "CDLModel",
    "ModelMetadata",
    "BlockInstance",
    "Connection",
    "Parameter",
    "Port",
]
