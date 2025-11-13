# CDL to Python Translator

A translator for Control Description Language (CDL) sequences to Python, enabling execution of ASHRAE Standard 231P control sequences in real-time building automation systems.

## Overview

This project translates CDL control sequences (written in Modelica) to executable Python code that can run in both simulation and real-time modes with BACnet integration.

### Project Goals

1. **Vendor Independence**: Execute CDL control sequences without vendor-specific tools
2. **Real-time Operation**: Run control logic with real building systems and BACnet points
3. **Simulation Support**: Verify control sequences before deployment
4. **Standards Compliance**: Implement ASHRAE Standard 231P (CDL) specification

## Architecture

The translator works in three steps:

```
┌─────────────┐
│ CDL File    │  Modelica control sequence
│ (.mo)       │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│ Step 1: modelica-json               │  Convert to CXF format
│ ($MODELICAJSONPATH)                 │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────┐
│ CXF File    │  Control eXchange Format (JSON)
│ (.json)     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│ Step 2: CXF Parser                  │  Parse and translate
│                                     │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────┐
│ Python Code │  Executable control sequence
│ (.py)       │  using CDL Python library
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│ Step 3: CDL Python Runtime (CPRE)  │  Execute in simulation
│         + CDL Python Library        │  or real-time mode
└─────────────────────────────────────┘
```

## Installation

```bash
# Clone the repository
git clone http://github.com/anandkp92/CDLPython
cd CDLPython

# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the CDL Python library
pip install -e .

# Run example
python examples/custom_p_with_limiter.py

# Set up modelica-json (required for Step 2 - Translation)
# Clone and install modelica-json: https://github.com/lbl-srg/modelica-json
# Set environment variable to modelica-json installation directory
export MODELICAJSONPATH=/path/to/modelica-json

# Requires: Java and Node.js ≥ 18 (for modelica-json only)
```

## Usage

### Translating a CDL Sequence

```bash
# Step 1: Convert CDL to CXF using modelica-json
node $MODELICAJSONPATH/app.js \
    -f path/to/sequence.mo \
    -o cxf \
    -d output_dir

# This generates CXF JSON files in output_dir/
```

```python
# Step 2: Translate CXF to Python
from pathlib import Path
from cdl_translator.translator import translate_cxf

# Translate any CXF file - automatically handles both simple and complex models
generated_code = translate_cxf(
    cxf_path='output_dir/sequence.jsonld',
    output_dir='generated/',
    search_paths=['path/to/custom_blocks/']  # Optional: for custom blocks
)

# For simple models (only standard CDL blocks):
#   - Generates one Python file (e.g., generated/SimpleController.py)
#
# For complex models (with custom blocks):
#   - Automatically finds and translates custom block dependencies
#   - Generates one Python file per block
#   - Example: generated/SubController.py, generated/MyController.py
```

**How Translation Works:**
1. Parses the main CXF file
2. If custom blocks are detected (blocks without 'CDL' in type path):
   - Searches for custom block CXF files in same directory and search paths
   - Recursively translates all dependencies (depth-first)
   - Generates one Python file per block
3. If only standard CDL blocks are used:
   - Generates a single Python file
4. Automatically detects and reports circular dependencies

**Custom Block Requirements:**
- Custom block CXF files must be named `{BlockName}.jsonld` or `{BlockName}.json`
- Must be in the same directory as parent CXF or in search paths
- Can be nested (custom blocks can use other custom blocks)

```bash
# Step 3: Run the generated Python sequence
python generated/sequence.py --mode simulation  # or --mode realtime
```

> **📖 For detailed examples and complete API reference, see [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md)**

### Direct Library Usage (Advanced)

If you just want to use the CDL Python library directly without translation:

```python
from cdl_python.CDL.Reals import PID
from cdl_python.time_manager import TimeManager, ExecutionMode

# Create time manager
tm = TimeManager(mode=ExecutionMode.REALTIME)

# Create and use blocks
pid = PID(time_manager=tm, k=0.5, Ti=1.0, Td=0.1)
output = pid.compute(u_s=25.0, u_m=22.0)
```

## Implementation Status

### ✅ Step 1: CDL Python Library (100% Complete!) 🎉

Core elementary block library for executing CDL sequences in Python.

**Status:** 122/122 blocks implemented ✅
- Core Infrastructure: ✅ Complete (TimeManager, CDLBlock, tests)
- Integers: ✅ 21/21 blocks (100%)
- Conversions: ✅ 4/4 blocks (100%)
- Types: ✅ 4/4 enumerations (100%)
- Routing: ✅ 15/15 blocks (100%)
- Discrete: ✅ 7/7 blocks (100%)
- Reals: ✅ 45/45 blocks (100%)
- Logical: ✅ 21/21 blocks (100%)
- Utilities: ✅ 2/2 blocks (100%)
- Psychrometrics: ✅ 3/3 blocks (100%)

See [CDL Python Library Documentation](#cdl-python-library) below for details.

### ✅ Step 2: CXF to Python Translator (100% Complete!) 🎉

Parser to convert CXF JSON format to executable Python code.

**Status:** Production ready for S231P format ✅
- ✅ CXF JSON parsing (S231P namespace support)
- ✅ @graph and @id resolution
- ✅ Block instantiation code generation
- ✅ Connection mapping (all types, including multi-target)
- ✅ Parameter assignment
- ✅ Python code generation (template-based)
- ✅ Model validation with error reporting
- ✅ Topological sorting for computation order
- ✅ **Recursive translation with custom blocks**
- ✅ **CXF file resolution (relative and absolute paths)**
- ✅ **Circular dependency detection**
- ✅ Comprehensive test suite (40 tests, 100% passing)

**Test Results:** 343/349 tests passing (98.3%)
- ✅ 100% success for S231P format (production standard)
- ✅ Generated code executes correctly
- ✅ Full validation pipeline working
- ✅ Custom blocks translate and execute correctly

**Key Features:**
- **Custom Block Support:** Translates user-defined composite blocks recursively
- **Multi-file Generation:** Each custom block becomes a separate Python file
- **Smart Import Management:** Automatically generates imports for both standard CDL blocks and custom blocks
- **Connection Handling:** Supports ports connected to multiple targets (fan-out)

See [Translation Example](#translation-example) below for a complete demonstration.

### ⏳ Step 3: CDL Python Runtime Environment (Not Started)

Runtime system for executing translated sequences.

**Will implement:**
- Asynchronous time management (background process)
- Block network execution
- Connection propagation
- BACnet integration interface
- Simulation vs real-time mode switching

## Project Structure

```
CDLPython/
├── cdl_python/              # Step 1: Elementary block library
│   ├── base.py             # Base classes
│   ├── time_manager.py     # Time management
│   └── CDL/                # CDL blocks (mirrors CDL library structure)
│       ├── Reals/          # Real-valued blocks (42 implemented)
│       ├── Logical/        # Boolean blocks (19 implemented)
│       ├── Integers/       # Integer blocks (21 implemented - complete!)
│       ├── Conversions/    # Type conversions (4 implemented - complete!)
│       ├── Types/          # Type enumerations (4 implemented - complete!)
│       ├── Routing/        # Array/vector routing (15 implemented - complete!)
│       ├── Discrete/       # Sampling/delay blocks (7 implemented - complete!)
│       ├── Utilities/      # Utility blocks (1 implemented)
│       └── Psychrometrics/ # Air properties (not yet implemented)
│
├── cdl_translator/          # Step 2: CXF parser (COMPLETE!)
│   ├── parser.py           # CXF JSON parser (S231P support)
│   ├── model.py            # Internal model representation
│   ├── codegen.py          # Python code generator
│   └── templates/          # Code generation templates
│
├── cdl_runtime/             # Step 3: Runtime environment (NOT YET IMPLEMENTED)
│   ├── executor.py         # Sequence executor
│   ├── network.py          # Block network manager
│   └── bacnet.py           # BACnet integration
│
├── tests/                   # Test suite
│   ├── test_*.py           # Unit tests for library
│   └── integration/        # Integration tests
│
├── CDL/                     # Reference CDL blocks from Buildings library
└── Example/                 # Example sequences for testing
```

**Note:** The `cdl_python/CDL/` structure exactly mirrors the CDL library structure to simplify Step 2 (translator). For example:
- `CDL/Reals/AddParameter.mo` → `cdl_python/CDL/Reals/AddParameter.py`
- No case conversion or mapping needed!

## Translation Example

See the complete translation example in the Jupyter notebook:
- **Notebook:** `examples/translation_example.ipynb`
- **Input:** CustomPWithLimiter.jsonld (S231P format CXF)
- **Output:** Executable Python code

The notebook demonstrates:
1. Loading and parsing a CXF file
2. Visualizing the model structure (blocks, connections, parameters)
3. Generating Python code
4. Testing the generated code
5. Comparing with hand-written implementation

**Quick Start:**
```bash
jupyter notebook examples/translation_example.ipynb
```

Or view the generated Python code directly:
```bash
cat tests/translator/output/generated/CustomPWithLimiter.py
```

## CDL Python Library

The elementary block library (Step 1) provides Python implementations of all CDL blocks.

### Features

- **Complete CDL Implementation**: All 122 CDL elementary blocks implemented
- **Dual Execution Modes**: Simulation (fixed/variable timesteps) and Real-time (wall-clock)
- **Stateful Blocks**: Proper state management for integrators, PIDs, timers, delays
- **Discrete-Time Operations**: Sampling, hold, delay, and triggered blocks
- **Continuous-Time Operations**: Derivatives, rate limiting, moving averages
- **Psychrometric Calculations**: Dew point, enthalpy, wet bulb temperature
- **Astronomical Calculations**: Sunrise/sunset times for any location
- **Type Safety**: Strong typing with type hints
- **Comprehensively Tested**: 274 passing unit tests
- **Clean Architecture**: Separation of time management from control logic

### Library Quick Start

#### Basic Block Usage

```python
from cdl_python.CDL.Reals import Add

adder = Add()
result = adder.compute(u1=5.0, u2=3.0)
print(result['y'])  # 8.0
```

#### Stateful Block with Simulation

```python
from cdl_python.CDL.Reals import IntegratorWithReset
from cdl_python.time_manager import TimeManager, ExecutionMode

tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
integrator = IntegratorWithReset(time_manager=tm, k=1.0, y_start=0.0)

for i in range(10):
    result = integrator.compute(u=2.0, trigger=False, y_reset_in=0.0)
    print(f"t={tm.get_time():.1f}, y={result['y']:.2f}")
    tm.advance()
```

#### Real-time Mode

```python
from cdl_python.CDL.Reals import PID
from cdl_python.time_manager import TimeManager, ExecutionMode
import time

tm = TimeManager(mode=ExecutionMode.REALTIME)
pid = PID(time_manager=tm, k=0.5, Ti=1.0, Td=0.1, yMax=100.0, yMin=0.0)

setpoint = 25.0
while True:
    measured = read_from_bacnet()  # Your BACnet integration
    tm.advance()

    output = pid.compute(u_s=setpoint, u_m=measured)
    write_to_bacnet(output['y'])

    time.sleep(0.1)
```

### Complete Example: Custom P Controller with Limiter

This example shows how to compose multiple CDL blocks to create custom control logic, translating a CDL model to Python. Based on [CustomPWithLimiter.mo](https://github.com/lbl-srg/modelica-json/blob/master/test/FromModelica/CustomPWithLimiter.mo).

**Original CDL Model** (`CustomPWithLimiter.mo`):
```modelica
block CustomPWithLimiter
  "P controller with variable output limiter"
  parameter Real k = 2 "Constant gain";

  // Inputs
  RealInput yMax "Maximum value of output signal";
  RealInput e "Control error";

  // Output
  RealOutput y "Control signal";

  // Blocks
  MultiplyByParameter gain(final k=k);
  Min minValue;

equation
  connect(e, gain.u);
  connect(gain.y, minValue.u2);
  connect(yMax, minValue.u1);
  connect(minValue.y, y);
end CustomPWithLimiter;
```

**Python Translation** (see `examples/custom_p_with_limiter.py`):
```python
from cdl_python.CDL.Reals import MultiplyByParameter, Min

class CustomPWithLimiter:
    """P controller with variable output limiter: y = min(yMax, k*e)"""

    def __init__(self, k=2.0):
        """Initialize with gain k"""
        self.k = k
        self.gain = MultiplyByParameter(k=self.k)  # Multiply error by gain
        self.min_value = Min()  # Take minimum of two inputs

    def compute(self, e, yMax):
        """
        Compute control output.

        Args:
            e: Control error
            yMax: Maximum output value

        Returns:
            {'y': control signal} = min(yMax, k*e)
        """
        # Connect blocks: e → gain.u
        gain_output = self.gain.compute(u=e)

        # yMax → minValue.u1, gain.y → minValue.u2
        min_output = self.min_value.compute(u1=yMax, u2=gain_output['y'])

        # minValue.y → y
        return {'y': min_output['y']}

# Usage
controller = CustomPWithLimiter(k=2.0)
result = controller.compute(e=10.0, yMax=5.0)
print(result['y'])  # Output: 5.0 (limited by yMax)

result = controller.compute(e=1.0, yMax=5.0)
print(result['y'])  # Output: 2.0 (k*e = 2.0*1.0)
```

**Run the complete example:**
```bash
python examples/custom_p_with_limiter.py
```

**Example output:**
```
============================================================
Custom P Controller with Limiter Example
============================================================

Controller parameters:
  Gain (k) = 2.0

Test Results:
------------------------------------------------------------
Error (e)    Max (yMax)   Output (y)   k*e
------------------------------------------------------------
1.00         5.00         2.00         2.00
5.00         5.00         5.00         10.00        ← limited
10.00        5.00         5.00         20.00        ← limited
-2.00        5.00         -4.00        -4.00
3.00         10.00        6.00         6.00
------------------------------------------------------------

Time-series simulation (setpoint tracking):
------------------------------------------------------------
Setpoint: 20.0
Output limit: 15.0

Time     Measured     Error        Output
------------------------------------------------------------
0        0.0          20.0         15.00
1        5.0          15.0         15.00
2        10.0         10.0         15.00
3        15.0         5.0          10.00
4        18.0         2.0          4.00
5        19.0         1.0          2.00
6        19.5         0.5          1.00
7        20.0         0.0          0.00
------------------------------------------------------------
```

This example demonstrates:
- ✅ Composing multiple CDL blocks into custom control logic
- ✅ Direct translation pattern from CDL Modelica to Python
- ✅ Block instantiation and connection through method calls
- ✅ Clean, readable Python code that mirrors CDL structure

### Implemented Blocks

**ALL PACKAGES COMPLETE (100%):** ✅

- ✅ **Integers (21/21)**: All arithmetic, comparison, and control flow blocks
- ✅ **Conversions (4/4)**: All type conversions between Real, Integer, Boolean
- ✅ **Types (4/4)**: Enumerations for controller types and time specifications
- ✅ **Routing (15/15)**: Array/vector manipulation (extractors, replicators, filters)
- ✅ **Discrete (7/7)**: Sampling, hold, delay, and triggered operations
- ✅ **Reals (45/45)**: Arithmetic, math, comparison, control, sources, continuous-time operations
- ✅ **Logical (21/21)**: Boolean logic, edge detection, timers, latches, verification
- ✅ **Utilities (2/2)**: Assert block and sunrise/sunset calculations
- ✅ **Psychrometrics (3/3)**: Dew point, specific enthalpy, wet bulb temperature

## Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_time_manager.py -v

# Run with coverage
python -m pytest tests/ --cov=cdl_python --cov-report=html
```

### Adding New Blocks

Follow the established patterns in the existing code:
1. Inherit from `CDLBlock` base class
2. Implement `compute()` method returning dictionary
3. Use `TimeManager` for time-based blocks
4. Add comprehensive tests following pytest patterns
5. Update package `__init__.py` to export the new block

## References

- **CDL Specification**: https://obc.lbl.gov/specification/cdl.html
- **CXF Specification**: https://obc.lbl.gov/specification/cxf.html
- **CDL Block Documentation**: https://simulationresearch.lbl.gov/modelica/releases/v12.0.0/help/Buildings_Controls_OBC_CDL.html
- **modelica-json Tool**: https://github.com/lbl-srg/modelica-json
- **ASHRAE Standard 231P**: https://www.ashrae.org/
- **Buildings Library**: https://github.com/lbl-srg/modelica-buildings

## Roadmap

### ✅ COMPLETE: Step 1 - Elementary Block Library (100%!) 🎉
- [x] Core infrastructure (TimeManager, CDLBlock)
- [x] Test framework (274 tests passing)
- [x] Integers package (100%)
- [x] Conversions package (100%)
- [x] Types package (100%)
- [x] Routing package (100%)
- [x] Discrete package (100%)
- [x] Reals package (100%) - Including continuous-time blocks
- [x] Logical package (100%) - Including Proof and VariablePulse
- [x] Utilities package (100%) - Including SunRiseSet
- [x] Psychrometrics package (100%) - All air property calculations

### ✅ COMPLETE: Step 2 - CXF to Python Translator (100%!) 🎉
- [x] CXF JSON parser (S231P namespace support)
- [x] Internal model representation with validation
- [x] Block instantiation generator
- [x] Connection mapper (all connection types, including multi-target)
- [x] Parameter assignment
- [x] Python code generation (template-based)
- [x] Topological sorting for computation order
- [x] Recursive translation with custom blocks
- [x] CXF file resolution (relative and absolute paths)
- [x] Circular dependency detection
- [x] Multi-file generation for custom blocks
- [x] Test suite (40 tests, 100% passing)
- [x] Test with example sequences (4/4 production files)

### Future: Step 3 - Runtime Environment (CPRE)
- [ ] Asynchronous time management
- [ ] Block network execution engine
- [ ] Connection propagation
- [ ] BACnet integration layer
- [ ] Mode switching (simulation ↔ realtime)
- [ ] Performance optimization

## Contributing

This is an active development project.

### Priority Areas
1. ✅ **Complete elementary blocks library** - DONE! 122/122 blocks (100%)
2. Implement CXF parser and code generator (Step 2)
3. Build runtime environment (Step 3)
4. Add integration tests with real CDL sequences
5. BACnet integration examples

## License

TBD

## Acknowledgments

- LBNL Buildings Library for CDL reference implementations
- ASHRAE for CDL/Standard 231P specification
- modelica-json tool for CXF generation
