"""
Example: Recursive Translation with Custom Blocks

This example demonstrates how to translate CDL models that contain
user-defined custom blocks. The translator will automatically:
1. Identify custom blocks in the main model
2. Find their CXF definition files
3. Recursively translate all dependencies
4. Generate one Python file per block

Example Structure:
  MyController.jsonld (uses SubController)
    └─> SubController.jsonld (uses standard CDL blocks)

Result:
  generated/SubController.py
  generated/MyController.py (imports SubController)
"""

from pathlib import Path
from cdl_translator.translator import translate_cxf_recursive, RecursiveTranslator
import sys
import json

# Example 1: Basic recursive translation
print("=" * 70)
print("Example 1: Basic Recursive Translation")
print("=" * 70)
print()

# Path to test fixtures
fixtures_dir = Path(__file__).parent.parent / "tests" / "translator" / "fixtures" / "modelica-json" / "cxf"
output_dir = Path(__file__).parent / "output" / "recursive"

# Translate MyController (which uses custom SubController blocks)
print(f"Translating: {fixtures_dir / 'MyController.jsonld'}")
print(f"Output dir: {output_dir}")
print()

generated_code = translate_cxf_recursive(
    cxf_path=fixtures_dir / "MyController.jsonld",
    output_dir=output_dir
)

print(f"✓ Generated {len(generated_code)} files:")
for block_name in generated_code.keys():
    file_path = output_dir / f"{block_name}.py"
    print(f"  - {file_path} ({len(generated_code[block_name])} bytes)")
print()


# Example 2: Test the generated code
print("=" * 70)
print("Example 2: Testing Generated Code")
print("=" * 70)
print()

# Add output directory to Python path
sys.path.insert(0, str(output_dir))

try:
    # Import generated modules
    from SubController import SubController
    from MyController import MyController

    # Test SubController
    print("Testing SubController (multiplies input by 0.5):")
    sub = SubController()

    test_cases = [10.0, 20.0, -5.0, 0.0]
    for u_val in test_cases:
        result = sub.compute(u=u_val)
        print(f"  SubController.compute(u={u_val:6.1f}) = {result['y']:6.2f}")
    print()

    # Test MyController
    print("Testing MyController (adds two inputs):")
    controller = MyController()

    test_cases = [(10.0, 20.0), (5.0, 15.0), (-10.0, 30.0), (0.0, 0.0)]
    for u1_val, u2_val in test_cases:
        result = controller.compute(u1=u1_val, u2=u2_val)
        print(f"  MyController.compute(u1={u1_val:6.1f}, u2={u2_val:6.1f}) = {result['y']:6.2f}")
    print()

finally:
    # Clean up sys.path and imported modules
    sys.path.remove(str(output_dir))
    if 'SubController' in sys.modules:
        del sys.modules['SubController']
    if 'MyController' in sys.modules:
        del sys.modules['MyController']


# Example 3: Using the RecursiveTranslator class directly
print("=" * 70)
print("Example 3: Using RecursiveTranslator Class")
print("=" * 70)
print()

# Create translator with additional search paths
search_paths = [
    fixtures_dir,  # Look for custom blocks in fixtures directory
]

translator = RecursiveTranslator(search_paths=search_paths)

# Translate without writing files
print("Translating without writing to disk...")
generated = translator.translate_file(
    cxf_path=fixtures_dir / "MyController.jsonld",
    output_dir=None  # Don't write files
)

print(f"✓ Generated code for {len(generated)} blocks in memory")
print()

# Show what was translated
print("Translation summary:")
print(f"  Translated blocks: {list(translator.translated)}")
print(f"  Code generated for: {list(generated.keys())}")
print()


# Example 4: Viewing model structure
print("=" * 70)
print("Example 4: Model Structure Analysis")
print("=" * 70)
print()

from cdl_translator.parser import CXFParser

# Parse and analyze MyController
with open(fixtures_dir / "MyController.jsonld", 'r') as f:
    data = json.load(f)

parser = CXFParser()
model = parser.parse_dict(data)

print("MyController Model Structure:")
print()

print("Inputs:")
for inp in model.metadata.inputs:
    print(f"  - {inp.name}: {inp.type.value}")
print()

print("Outputs:")
for out in model.metadata.outputs:
    print(f"  - {out.name}: {out.type.value}")
print()

print("Block Instances:")
for inst in model.instances:
    block_kind = "CUSTOM" if inst.is_custom_block() else "STANDARD CDL"
    print(f"  - {inst.instance_name}: {inst.block_type} [{block_kind}]")
    if inst.parameters:
        for param_name, param_value in inst.parameters.items():
            print(f"      {param_name} = {param_value}")
print()

print("Connections:")
for conn in model.connections:
    src = conn.source_port if conn.is_from_input() else f"{conn.source_block}.{conn.source_port}"
    tgt = conn.target_port if conn.is_to_output() else f"{conn.target_block}.{conn.target_port}"
    print(f"  {src} → {tgt}")
print()

print("Computation Order (topologically sorted):")
for i, inst in enumerate(model.get_computation_order(), 1):
    print(f"  {i}. {inst.instance_name} ({inst.block_type})")
print()


# Example 5: Error handling
print("=" * 70)
print("Example 5: Error Handling")
print("=" * 70)
print()

# Try to translate a non-existent file
print("Testing error handling for missing file...")
try:
    translate_cxf_recursive(
        cxf_path=fixtures_dir / "NonExistent.jsonld",
        output_dir=output_dir
    )
except FileNotFoundError as e:
    print(f"✓ Caught expected error: {type(e).__name__}")
    print(f"  Message: {str(e)[:100]}...")
print()

# Try to parse invalid model
print("Testing validation errors...")
invalid_model = {
    "@graph": [{
        "@id": "test",
        "@type": "S231P:Block",
        "S231P:label": "TestBlock",
        "S231P:hasInput": {
            "@id": "test.in",
            "@type": "S231P:RealInput",
            "S231P:label": "in",
            "S231P:isConnectedTo": {"@id": "test.nonexistent"}  # Invalid connection
        }
    }]
}

try:
    parser = CXFParser()
    model = parser.parse_dict(invalid_model)
    is_valid, errors = model.validate()
    if not is_valid:
        print(f"✓ Validation caught {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
except Exception as e:
    print(f"✓ Caught error: {type(e).__name__}: {e}")

print()
print("=" * 70)
print("All examples completed successfully!")
print("=" * 70)
