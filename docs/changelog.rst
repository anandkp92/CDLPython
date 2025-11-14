Changelog
=========

All notable changes to this project will be documented in this file.

Version 0.1.0 (Current)
-----------------------

Initial release of CDL Python.

Features
~~~~~~~~

* **Core CDL Library**

  * Complete implementation of CDL elementary blocks
  * Support for Real, Integer, and Logical signal types
  * Time management for simulation and real-time modes
  * 120+ elementary blocks across multiple packages

* **Source Blocks**

  * Constant, Sin, Pulse, Ramp sources for Real signals
  * TimeTable with linear and constant interpolation
  * CalendarTime and CivilTime for time-based operations
  * Integer and Boolean source blocks
  * SampleTrigger for edge-triggered sampling

* **Mathematical Operations**

  * Basic arithmetic (Add, Subtract, Multiply, Divide)
  * Advanced math (Abs, Sign, Sqrt, Exp, Log)
  * Trigonometric functions
  * Min, Max, and limit operations
  * Gain and MultiplyByParameter blocks

* **Logical Operations**

  * Boolean logic (And, Or, Not, Xor)
  * Comparisons (Greater, Less, Equal)
  * Edge detection (Rising, Falling)
  * Latches and flip-flops

* **Control Blocks**

  * PID controller with anti-windup
  * Limiters and saturators
  * Hysteresis and dead-band

* **Discrete-Time Blocks**

  * UnitDelay, ZeroOrderHold, FirstOrderHold
  * Sampler and TriggeredSampler
  * TriggeredMax, TriggeredMovingMean

* **Type Conversions**

  * BooleanToReal, BooleanToInteger
  * IntegerToReal, RealToInteger
  * Type-safe conversions

* **CXF Translator**

  * Parse CXF (CDL Exchange Format) JSON files
  * Generate executable Python code
  * Automatic dependency resolution
  * Command-line interface

* **Testing**

  * Comprehensive test suite with 380+ tests
  * >90% code coverage
  * Tests for all elementary blocks

* **Documentation**

  * Sphinx-based documentation
  * API reference with autodoc
  * Examples and tutorials
  * Quick start guide

Known Issues
~~~~~~~~~~~~

* Some advanced PID features may need refinement
* Limited error messages in CXF parser
* Documentation examples need expansion

Upcoming Features
~~~~~~~~~~~~~~~~~

* Additional Psychrometric blocks
* More routing and multiplexing blocks
* Enhanced visualization tools
* Performance optimizations
* Real-time execution improvements
