CXF Translation Examples
========================

The cdl_translator package converts CXF (CDL Exchange Format) files into executable Python code.

Basic Translation
-----------------

Using the Python API
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from cdl_translator.parser import CXFParser
    from cdl_translator.translator import PythonTranslator

    # Parse CXF file
    parser = CXFParser()
    model = parser.parse_file('controller.json')

    # Inspect the model
    print(f"Model name: {model.model_name}")
    print(f"Number of blocks: {len(model.instances)}")
    print(f"Number of connections: {len(model.connections)}")

    # List all blocks
    for instance in model.instances:
        print(f"  - {instance.instance_name}: {instance.block_type}")

    # Translate to Python
    translator = PythonTranslator()
    python_code = translator.translate(model)

    # Save to file
    output_path = 'generated_controller.py'
    with open(output_path, 'w') as f:
        f.write(python_code)

    print(f"Generated code saved to {output_path}")

Using the Command-Line Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Basic translation
    python -m cdl_translator.cli input.json -o output.py

    # With verbose output
    python -m cdl_translator.cli input.json -o output.py -v

    # Display help
    python -m cdl_translator.cli --help

Example CXF File
----------------

A simple proportional controller in CXF format:

.. code-block:: json

    {
      "@context": "https://obc.lbl.gov/schema/cxf/1.0/context.jsonld",
      "@graph": [
        {
          "@id": "SimpleController",
          "@type": "CompositeBlock",
          "parameters": {
            "gain": {"@type": "Real", "value": 2.5}
          },
          "instances": [
            {
              "@id": "gain",
              "@type": "CDL.Reals.MultiplyByParameter",
              "parameters": {"k": "gain"}
            }
          ],
          "connections": [
            {
              "from": "u",
              "to": "gain.u"
            },
            {
              "from": "gain.y",
              "to": "y"
            }
          ]
        }
      ]
    }

Generated Python Code
---------------------

The translator generates runnable Python code:

.. code-block:: python

    """
    Auto-generated from CXF file: controller.json
    Model: SimpleController
    Generated: 2024-01-15 10:30:00
    """

    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Reals import MultiplyByParameter


    class SimpleController:
        """SimpleController composite block"""

        def __init__(self, time_manager: TimeManager, gain: float = 2.5):
            """Initialize SimpleController

            Args:
                time_manager: Time manager instance
                gain: Proportional gain
            """
            self.time_manager = time_manager

            # Create block instances
            self.gain = MultiplyByParameter(k=gain)

        def compute(self, u: float) -> dict:
            """Compute outputs

            Args:
                u: Input signal

            Returns:
                Dictionary with output 'y'
            """
            # Compute blocks
            gain_out = self.gain.compute(u=u)

            # Output
            return {'y': gain_out['y']}

Using Generated Code
--------------------

.. code-block:: python

    from generated_controller import SimpleController
    from cdl_python.time_manager import TimeManager, ExecutionMode

    # Create time manager
    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)

    # Create controller instance
    controller = SimpleController(time_manager=tm, gain=3.0)

    # Use the controller
    for i in range(10):
        error = 5.0 - i  # Decreasing error
        result = controller.compute(u=error)
        print(f"Error: {error:.1f}, Output: {result['y']:.1f}")

Inspecting Parsed Models
-------------------------

.. code-block:: python

    from cdl_translator.parser import CXFParser

    parser = CXFParser()
    model = parser.parse_file('complex_controller.json')

    # Model information
    print(f"Model: {model.model_name}")
    print(f"Type: {model.model_type}")

    # Parameters
    print("\nParameters:")
    for name, param in model.parameters.items():
        print(f"  {name}: {param.value} ({param.param_type})")

    # Block instances
    print("\nBlock Instances:")
    for inst in model.instances:
        print(f"  {inst.instance_name}:")
        print(f"    Type: {inst.block_type}")
        if inst.parameters:
            print(f"    Parameters: {inst.parameters}")

    # Connections
    print("\nConnections:")
    for conn in model.connections:
        print(f"  {conn.from_port} -> {conn.to_port}")

    # Computation order
    print("\nComputation Order:")
    order = model.get_computation_order()
    for i, inst in enumerate(order, 1):
        print(f"  {i}. {inst.instance_name}")

Batch Translation
-----------------

Translate multiple files:

.. code-block:: python

    from pathlib import Path
    from cdl_translator.parser import CXFParser
    from cdl_translator.translator import PythonTranslator

    parser = CXFParser()
    translator = PythonTranslator()

    # Find all CXF files
    cxf_files = Path('cxf_models').glob('*.json')

    for cxf_path in cxf_files:
        print(f"Translating {cxf_path.name}...")

        try:
            # Parse and translate
            model = parser.parse_file(str(cxf_path))
            python_code = translator.translate(model)

            # Save with same name, .py extension
            output_path = Path('generated') / cxf_path.with_suffix('.py').name
            output_path.parent.mkdir(exist_ok=True)

            with open(output_path, 'w') as f:
                f.write(python_code)

            print(f"  ✓ Generated {output_path}")

        except Exception as e:
            print(f"  ✗ Error: {e}")
