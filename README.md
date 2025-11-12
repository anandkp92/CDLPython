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

# Step 2: Translate CXF to Python (NOT YET IMPLEMENTED)
python -m cdl_translator translate output_dir/sequence.json -o sequence.py

# Step 3: Run the generated Python sequence
python sequence.py --mode simulation  # or --mode realtime
```

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

### ✅ Step 1: CDL Python Library (43% Complete)

Core elementary block library for executing CDL sequences in Python.

**Status:** 52/122 blocks implemented
- Core Infrastructure: ✅ Complete (TimeManager, CDLBlock, tests)
- Conversions: ✅ 4/4 blocks (100%)
- Reals: 🟡 34/45 blocks (76%)
- Integers: 🟡 10/21 blocks (48%)
- Logical: 🟡 4/22 blocks (18%)
- Discrete: ⚪ 0/7 blocks
- Routing: ⚪ 0/15 blocks
- Other: ⚪ 0/13 blocks

See [CDL Python Library Documentation](#cdl-python-library) below for details.

### ⏳ Step 2: CXF to Python Translator (Not Started)

Parser to convert CXF JSON format to executable Python code.

**Will implement:**
- CXF JSON parsing
- Block instantiation code generation
- Connection mapping
- Parameter assignment
- Python code generation

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
│       ├── Reals/          # Real-valued blocks (34 implemented)
│       ├── Logical/        # Boolean blocks (4 implemented)
│       ├── Integers/       # Integer blocks (10 implemented)
│       ├── Conversions/    # Type conversions (4 implemented - complete!)
│       ├── Discrete/       # Discrete blocks (not yet implemented)
│       └── Routing/        # Routing blocks (not yet implemented)
│
├── cdl_translator/          # Step 2: CXF parser (NOT YET IMPLEMENTED)
│   ├── parser.py           # CXF JSON parser
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
├── Example/                 # Example sequences for testing
└── claude_log/              # Development logs and documentation
```

**Note:** The `cdl_python/CDL/` structure exactly mirrors the CDL library structure to simplify Step 2 (translator). For example:
- `CDL/Reals/AddParameter.mo` → `cdl_python/CDL/Reals/AddParameter.py`
- No case conversion or mapping needed!

## CDL Python Library

The elementary block library (Step 1) provides Python implementations of all CDL blocks.

### Features

- **Dual Execution Modes**: Simulation (fixed/variable timesteps) and Real-time (wall-clock)
- **Stateful Blocks**: Proper state management for integrators, PIDs, timers
- **Type Safety**: Strong typing with type hints
- **Well Tested**: 43 passing unit tests
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

See [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) for complete details.

**Highlights:**
- ✅ Arithmetic: Add, Subtract, Multiply, Divide
- ✅ Math: Trig functions, logarithms, exponentials
- ✅ Comparison: Greater, Less (with hysteresis)
- ✅ Control: PID controller, Integrator
- ✅ Logic: And, Or, Not, Edge detection
- ✅ Conversions: All type conversions between Real, Integer, Boolean

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

See [FINAL_STATUS_AND_REMAINING.md](FINAL_STATUS_AND_REMAINING.md) for implementation patterns and remaining blocks.

## References

- **CDL Specification**: https://obc.lbl.gov/specification/cdl.html
- **CXF Specification**: https://obc.lbl.gov/specification/cxf.html
- **CDL Block Documentation**: https://simulationresearch.lbl.gov/modelica/releases/v12.0.0/help/Buildings_Controls_OBC_CDL.html
- **modelica-json Tool**: https://github.com/lbl-srg/modelica-json
- **ASHRAE Standard 231P**: https://www.ashrae.org/
- **Buildings Library**: https://github.com/lbl-srg/modelica-buildings

## Roadmap

### Current: Step 1 - Elementary Block Library (43% complete)
- [x] Core infrastructure (TimeManager, CDLBlock)
- [x] Test framework
- [x] Conversions package (100%)
- [ ] Complete Reals package (76% → 100%)
- [ ] Complete Logical package (18% → 100%)
- [ ] Complete Integers package (48% → 100%)
- [ ] Implement Discrete, Routing, Psychrometrics packages
- [ ] Comprehensive test suite

### Next: Step 2 - CXF to Python Translator
- [ ] CXF JSON parser
- [ ] Block instantiation generator
- [ ] Connection mapper
- [ ] Parameter assignment
- [ ] Python code generation
- [ ] Test with example sequences

### Future: Step 3 - Runtime Environment (CPRE)
- [ ] Asynchronous time management
- [ ] Block network execution engine
- [ ] Connection propagation
- [ ] BACnet integration layer
- [ ] Mode switching (simulation ↔ realtime)
- [ ] Performance optimization

## Contributing

This is an active development project. See [FINAL_STATUS_AND_REMAINING.md](FINAL_STATUS_AND_REMAINING.md) for areas that need work.

### Priority Areas
1. Complete remaining elementary blocks in library
2. Implement CXF parser and code generator
3. Build runtime environment
4. Add integration tests with real CDL sequences
5. BACnet integration examples

## License

TBD

## Acknowledgments

- LBNL Buildings Library for CDL reference implementations
- ASHRAE for CDL/Standard 231P specification
- modelica-json tool for CXF generation
- Development accelerated with AI assistance (Claude/Anthropic), with human oversight, architecture design, and comprehensive testing
