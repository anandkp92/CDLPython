# CDL Python Examples

This directory contains example implementations demonstrating how to use the CDL Python library to create control logic by composing elementary CDL blocks.

## Available Examples

### `task1_custom_p_with_limiter_demo.ipynb` 🆕 **Jupyter Notebook**

**Description:** Interactive demonstration of the Custom P Controller with Limiter in both simulation and real-time modes

**What it demonstrates:**
- **Simulation Mode:** Using CDL source blocks (Constant, Sin) with fine timesteps for smooth curves
- **Real-Time Mode:** Mimicking BACnet controller receiving sensor data every 1 second
- Data collection with pandas DataFrames
- Visualization of controller behavior and limiter activation
- Wall-clock timestamping for real-time mode

**Prerequisites:**
```bash
# Install package
pip install -e .

# Install notebook dependencies
pip install jupyter pandas numpy matplotlib
```

**Run:**
```bash
jupyter notebook examples/task1_custom_p_with_limiter_demo.ipynb
```

**Or test imports first:**
```bash
cd examples
python test_notebook_imports.py
```

---

### `custom_p_with_limiter.py`

**Description:** Custom proportional controller with variable output limiter

**Based on:** [CustomPWithLimiter.mo](https://github.com/lbl-srg/modelica-json/blob/master/test/FromModelica/CustomPWithLimiter.mo)

**CDL Blocks Used:**
- `Buildings.Controls.OBC.CDL.Reals.MultiplyByParameter`
- `Buildings.Controls.OBC.CDL.Reals.Min`

**Control Logic:** `y = min(yMax, k * e)`
- Multiplies control error by gain constant
- Limits output to maximum allowable value

**Run:**
```bash
python examples/custom_p_with_limiter.py
```

**Key Learning Points:**
- How to translate CDL Modelica models to Python
- How to instantiate and compose CDL blocks
- How to connect block outputs to inputs through method calls
- Pattern for creating reusable control components

## Running Examples

### Prerequisites

1. Install the CDL Python library:
   ```bash
   # From repository root
   pip install -e .
   ```

2. Run any example:
   ```bash
   python examples/<example_name>.py
   ```

### Using a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install -e .

# Run examples
python examples/custom_p_with_limiter.py
```

## Creating Your Own Examples

To create a new control sequence using the CDL Python library:

1. **Identify the CDL blocks needed** from the [CDL specification](https://obc.lbl.gov/specification/cdl.html)

2. **Import the blocks:**
   ```python
   from cdl_python.CDL.Reals import Add, Multiply, PID
   from cdl_python.CDL.Logical import And, Or
   ```

3. **Instantiate blocks in `__init__`:**
   ```python
   class MyController:
       def __init__(self, param1, param2):
           self.block1 = Add()
           self.block2 = Multiply()
   ```

4. **Connect blocks in `compute` method:**
   ```python
       def compute(self, input1, input2):
           result1 = self.block1.compute(u1=input1, u2=input2)
           result2 = self.block2.compute(u1=result1['y'], u2=3.0)
           return {'y': result2['y']}
   ```

5. **Test your controller:**
   ```python
   controller = MyController(param1=1.0, param2=2.0)
   output = controller.compute(input1=5.0, input2=3.0)
   print(output['y'])
   ```

## Translation Pattern: CDL to Python

### CDL Model Structure
```modelica
block MyController
  parameter Real k = 1.0;

  RealInput u1;
  RealInput u2;
  RealOutput y;

  Add adder;
  MultiplyByParameter gain(k=k);

equation
  connect(u1, adder.u1);
  connect(u2, adder.u2);
  connect(adder.y, gain.u);
  connect(gain.y, y);
end MyController;
```

### Python Translation
```python
from cdl_python.CDL.Reals import Add, MultiplyByParameter

class MyController:
    def __init__(self, k=1.0):
        self.k = k
        self.adder = Add()
        self.gain = MultiplyByParameter(k=self.k)

    def compute(self, u1, u2):
        # u1, u2 → adder.u1, adder.u2
        adder_output = self.adder.compute(u1=u1, u2=u2)

        # adder.y → gain.u
        gain_output = self.gain.compute(u=adder_output['y'])

        # gain.y → y
        return {'y': gain_output['y']}
```

### Key Translation Rules

1. **Parameters** → `__init__` arguments
2. **Inputs** → `compute` method arguments
3. **Outputs** → `compute` method return values (as dict)
4. **Block declarations** → Instance variables in `__init__`
5. **Connections** → Method calls in `compute`

## Available CDL Blocks

See the main [README.md](../README.md) for a complete list of implemented blocks.

**Currently Available: ALL 122 CDL blocks (100% complete!) 🎉**

**All Packages Complete:**
- Integers: 21 blocks ✅ (arithmetic, comparison, control flow)
- Conversions: 4 blocks ✅ (type conversions)
- Types: 4 enumerations ✅ (controller types, time specs)
- Routing: 15 blocks ✅ (extractors, replicators, filters)
- Discrete: 7 blocks ✅ (sampling, hold, delay, triggered operations)
- Reals: 45 blocks ✅ (arithmetic, math, comparison, control, sources, continuous-time)
- Logical: 21 blocks ✅ (logic gates, timers, edge detection, verification)
- Utilities: 2 blocks ✅ (Assert, SunRiseSet)
- Psychrometrics: 3 blocks ✅ (dew point, enthalpy, wet bulb)

## Need Help?

- **CDL Specification:** https://obc.lbl.gov/specification/cdl.html
- **CDL Block Documentation:** https://simulationresearch.lbl.gov/modelica/releases/v12.0.0/help/Buildings_Controls_OBC_CDL.html
- **Main README:** [../README.md](../README.md)
