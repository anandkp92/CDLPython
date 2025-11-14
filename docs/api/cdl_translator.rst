cdl_translator package
======================

The ``cdl_translator`` package provides tools for translating CXF (CDL Exchange Format)
files into executable Python code using the cdl_python library.

Package Overview
----------------

.. autosummary::
   :toctree: generated/
   :recursive:

   cdl_translator

Modules
-------

parser module
~~~~~~~~~~~~~

The parser module handles parsing of CXF (JSON-LD) files and building CDL model representations.

.. automodule:: cdl_translator.parser
   :members:
   :undoc-members:
   :show-inheritance:

translator module
~~~~~~~~~~~~~~~~~

The translator module converts parsed CXF models into executable Python code.

.. automodule:: cdl_translator.translator
   :members:
   :undoc-members:
   :show-inheritance:

cli module
~~~~~~~~~~

Command-line interface for the CXF to Python translator.

.. automodule:: cdl_translator.cli
   :members:
   :undoc-members:
   :show-inheritance:

Key Classes
-----------

CXFParser
~~~~~~~~~

.. autoclass:: cdl_translator.parser.CXFParser
   :members:
   :special-members: __init__
   :show-inheritance:

CDLModel
~~~~~~~~

.. autoclass:: cdl_translator.parser.CDLModel
   :members:
   :special-members: __init__
   :show-inheritance:

BlockInstance
~~~~~~~~~~~~~

.. autoclass:: cdl_translator.parser.BlockInstance
   :members:
   :special-members: __init__
   :show-inheritance:

Connection
~~~~~~~~~~

.. autoclass:: cdl_translator.parser.Connection
   :members:
   :special-members: __init__
   :show-inheritance:

PythonTranslator
~~~~~~~~~~~~~~~~

.. autoclass:: cdl_translator.translator.PythonTranslator
   :members:
   :special-members: __init__
   :show-inheritance:

Usage Example
-------------

Basic usage of the translator::

    from cdl_translator.parser import CXFParser
    from cdl_translator.translator import PythonTranslator

    # Parse CXF file
    parser = CXFParser()
    model = parser.parse_file('controller.json')

    # Translate to Python
    translator = PythonTranslator()
    python_code = translator.translate(model)

    # Save to file
    with open('controller.py', 'w') as f:
        f.write(python_code)

Command-Line Usage
------------------

The package includes a CLI tool for easy translation::

    # Translate a single file
    python -m cdl_translator.cli input.json -o output.py

    # Translate with verbose output
    python -m cdl_translator.cli input.json -o output.py -v

    # Display help
    python -m cdl_translator.cli --help
