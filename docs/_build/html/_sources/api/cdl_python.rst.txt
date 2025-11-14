cdl_python package
==================

The ``cdl_python`` package provides Python implementations of CDL (Control Description Language) blocks
for building automation and control systems.

Core Modules
------------

.. autosummary::
   :toctree: generated/
   :recursive:

   cdl_python.base
   cdl_python.time_manager

CDL Blocks
----------

Reals Package
~~~~~~~~~~~~~

Real-valued signal processing blocks.

.. autosummary::
   :toctree: generated/
   :recursive:

   cdl_python.CDL.Reals

Reals.Sources
^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/

   cdl_python.CDL.Reals.Sources.Constant
   cdl_python.CDL.Reals.Sources.Sin
   cdl_python.CDL.Reals.Sources.Pulse
   cdl_python.CDL.Reals.Sources.Ramp
   cdl_python.CDL.Reals.Sources.TimeTable
   cdl_python.CDL.Reals.Sources.CalendarTime
   cdl_python.CDL.Reals.Sources.CivilTime

Reals.Math
^^^^^^^^^^

.. autosummary::
   :toctree: generated/

   cdl_python.CDL.Reals.Math

Reals.Limiter
^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/

   cdl_python.CDL.Reals.Limiter

Reals.PIDController
^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/

   cdl_python.CDL.Reals.PIDController

Integers Package
~~~~~~~~~~~~~~~~

Integer signal processing blocks.

.. autosummary::
   :toctree: generated/
   :recursive:

   cdl_python.CDL.Integers

Integers.Sources
^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/

   cdl_python.CDL.Integers.Sources.Constant
   cdl_python.CDL.Integers.Sources.Pulse
   cdl_python.CDL.Integers.Sources.TimeTable

Integers.Math
^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/

   cdl_python.CDL.Integers.Math

Logical Package
~~~~~~~~~~~~~~~

Boolean logic blocks.

.. autosummary::
   :toctree: generated/
   :recursive:

   cdl_python.CDL.Logical

Logical.Sources
^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/

   cdl_python.CDL.Logical.Sources.Constant
   cdl_python.CDL.Logical.Sources.Pulse
   cdl_python.CDL.Logical.Sources.SampleTrigger
   cdl_python.CDL.Logical.Sources.TimeTable

Logical.Operations
^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/

   cdl_python.CDL.Logical

Conversions Package
~~~~~~~~~~~~~~~~~~~

Type conversion blocks.

.. autosummary::
   :toctree: generated/
   :recursive:

   cdl_python.CDL.Conversions

Discrete Package
~~~~~~~~~~~~~~~~

Discrete-time signal processing blocks.

.. autosummary::
   :toctree: generated/
   :recursive:

   cdl_python.CDL.Discrete

Routing Package
~~~~~~~~~~~~~~~

Signal routing and multiplexing blocks.

.. autosummary::
   :toctree: generated/
   :recursive:

   cdl_python.CDL.Routing

Utilities Package
~~~~~~~~~~~~~~~~~

Utility blocks for assertions and validation.

.. autosummary::
   :toctree: generated/
   :recursive:

   cdl_python.CDL.Utilities

Psychrometrics Package
~~~~~~~~~~~~~~~~~~~~~~

Psychrometric calculation blocks.

.. autosummary::
   :toctree: generated/
   :recursive:

   cdl_python.CDL.Psychrometrics

Module Reference
----------------

base module
~~~~~~~~~~~

.. automodule:: cdl_python.base
   :members:
   :undoc-members:
   :show-inheritance:

time_manager module
~~~~~~~~~~~~~~~~~~~

.. automodule:: cdl_python.time_manager
   :members:
   :undoc-members:
   :show-inheritance:
