# CDL to Python Translation Guide

## Quick Start

### One Function for Everything

Use `translate_cxf()` for all translation tasks - it automatically handles both simple and complex models:

```python
from cdl_translator.translator import translate_cxf

# Works for any CXF file!
generated = translate_cxf(
    cxf_path='path/to/model.jsonld',
    output_dir='generated/',
    search_paths=['path/to/custom_blocks/']  # Optional
)
```

### What It Does

**For simple models** (only standard CDL blocks):
- Generates **one** Python file
- Example: `SimpleController.jsonld` → `SimpleController.py`

**For complex models** (with custom blocks):
- Automatically detects custom blocks
- Finds and translates dependencies
- Generates **one Python file per block**
- Example: `MyController.jsonld` → `SubController.py` + `MyController.py`

## Examples

### Example 1: Simple Model (Standard CDL Blocks Only)

```python
from cdl_translator.translator import translate_cxf

# Model uses only standard CDL blocks (Add, Multiply, etc.)
generated = translate_cxf(
    cxf_path='CustomPWithLimiter.jsonld',
    output_dir='generated/'
)

# Result: generated/CustomPWithLimiter.py
```

### Example 2: Complex Model (With Custom Blocks)

```python
from cdl_translator.translator import translate_cxf

# Model uses custom blocks (SubController)
# Custom block CXF file must be in same directory or search_paths
generated = translate_cxf(
    cxf_path='MyController.jsonld',
    output_dir='generated/'
)

# Result:
#   generated/SubController.py (custom block)
#   generated/MyController.py (main model, imports SubController)
```

### Example 3: Custom Blocks in Different Directory

```python
from cdl_translator.translator import translate_cxf

# Custom blocks located elsewhere
generated = translate_cxf(
    cxf_path='controllers/MainController.jsonld',
    output_dir='generated/',
    search_paths=[
        'custom_blocks/',
        'shared/components/'
    ]
)

# Translator will search for custom block CXF files in:
# 1. controllers/ (same directory as MainController.jsonld)
# 2. custom_blocks/
# 3. shared/components/
```

### Example 4: Generate Code Without Writing Files

```python
from cdl_translator.translator import translate_cxf

# Generate code in memory only
generated = translate_cxf(
    cxf_path='MyController.jsonld',
    output_dir=None  # Don't write files
)

# Access generated code
for block_name, code in generated.items():
    print(f"{block_name}: {len(code)} bytes")
    # Do something with the code...
```

## How It Works

1. **Parse** the main CXF file
2. **Detect** if model uses custom blocks (blocks without 'CDL' in type path)
3. If custom blocks found:
   - Search for custom block CXF files (`.jsonld` or `.json`)
   - Recursively translate dependencies (depth-first)
4. **Generate** Python code:
   - One file per block
   - Custom blocks imported automatically
   - All connections properly wired
5. **Validate**:
   - Check for circular dependencies
   - Verify all connections are valid
   - Ensure correct computation order

## Custom Block Requirements

For custom blocks to work:

1. **Naming**: Custom block CXF files must be named:
   - `{BlockName}.jsonld` or
   - `{BlockName}.json`

2. **Location**: Must be in:
   - Same directory as the parent CXF file, OR
   - One of the directories in `search_paths`

3. **Nesting**: Custom blocks can use other custom blocks (recursive)

4. **Type Path**: Custom blocks identified by NOT having 'CDL' in their type path:
   - Custom: `ex:SubController`, `MyPackage.CustomBlock`
   - Standard: `Buildings.Controls.OBC.CDL.Reals.Add`

## Error Handling

### File Not Found

```python
try:
    generated = translate_cxf('NonExistent.jsonld')
except FileNotFoundError as e:
    print(f"CXF file not found: {e}")
```

### Custom Block Not Found

```python
try:
    generated = translate_cxf('MyController.jsonld')
except FileNotFoundError as e:
    # Custom block CXF file not found
    print(f"Custom block missing: {e}")
    # Hint: Add directory to search_paths or move CXF file
```

### Circular Dependencies

```python
try:
    generated = translate_cxf('CircularModel.jsonld')
except ValueError as e:
    print(f"Circular dependency: {e}")
    # Shows dependency chain: A -> B -> C -> A
```

### Invalid Model

```python
from cdl_translator.translator import translate_cxf

try:
    generated = translate_cxf('invalid_model.jsonld')
except ValueError as e:
    print(f"Model validation failed: {e}")
    # Shows specific validation errors
```

## Advanced Usage

### Using RecursiveTranslator Class Directly

For more control over the translation process:

```python
from cdl_translator.translator import RecursiveTranslator
from pathlib import Path

# Create translator with custom configuration
translator = RecursiveTranslator(
    search_paths=[Path('custom_blocks'), Path('shared')]
)

# Translate
generated = translator.translate_file(
    cxf_path=Path('MyController.jsonld'),
    output_dir=Path('generated/')
)

# Access translator state
print(f"Translated blocks: {translator.translated}")
print(f"Dependency chain: {translator.dependency_chain}")
```

### Checking Model Structure Before Translation

```python
from cdl_translator.parser import CXFParser
import json

# Parse model to inspect structure
with open('MyController.jsonld', 'r') as f:
    parser = CXFParser()
    model = parser.parse_dict(json.load(f))

# Check for custom blocks
custom_blocks = [inst for inst in model.instances if inst.is_custom_block()]
print(f"Found {len(custom_blocks)} custom blocks:")
for inst in custom_blocks:
    print(f"  - {inst.instance_name}: {inst.get_custom_block_name()}")

# Validate before translating
is_valid, errors = model.validate()
if not is_valid:
    print("Validation errors:")
    for error in errors:
        print(f"  - {error}")
else:
    # Safe to translate
    from cdl_translator.translator import translate_cxf
    generated = translate_cxf(cxf_path='MyController.jsonld')
```

## Testing Generated Code

```python
from cdl_translator.translator import translate_cxf
import sys

# Generate code
generated = translate_cxf(
    cxf_path='MyController.jsonld',
    output_dir='generated/'
)

# Add to Python path
sys.path.insert(0, 'generated/')

# Import and test
from MyController import MyController

controller = MyController()
result = controller.compute(u1=10.0, u2=20.0)
print(f"Output: {result}")

# Clean up
sys.path.remove('generated/')
```

## Complete Workflow

```python
from pathlib import Path
from cdl_translator.translator import translate_cxf

# 1. Translate CXF to Python
print("Translating CXF to Python...")
generated = translate_cxf(
    cxf_path='MyController.jsonld',
    output_dir='generated/',
    search_paths=['custom_blocks/']
)

print(f"✓ Generated {len(generated)} file(s)")
for block_name in generated.keys():
    print(f"  - {block_name}.py")

# 2. Import and use generated code
import sys
sys.path.insert(0, 'generated/')

from MyController import MyController

# 3. Create instance
controller = MyController()

# 4. Use it
result = controller.compute(u1=25.0, u2=30.0)
print(f"Result: {result}")

# 5. Clean up
sys.path.remove('generated/')
if 'MyController' in sys.modules:
    del sys.modules['MyController']
```

## Tips

1. **Use absolute paths** to avoid confusion:
   ```python
   from pathlib import Path
   cxf_path = Path('/full/path/to/model.jsonld').resolve()
   ```

2. **Check generated code** is syntactically valid:
   ```python
   for block_name, code in generated.items():
       try:
           compile(code, f"{block_name}.py", 'exec')
           print(f"✓ {block_name}.py is valid")
       except SyntaxError as e:
           print(f"✗ {block_name}.py has syntax error: {e}")
   ```

3. **Organize custom blocks** in a dedicated directory:
   ```
   project/
   ├── models/
   │   └── MainController.jsonld
   ├── custom_blocks/
   │   ├── SubController.jsonld
   │   └── Utilities.jsonld
   └── generated/
   ```

4. **Version control**: Commit CXF files, not generated Python files

5. **Regenerate** Python code when CXF changes:
   ```bash
   # After updating CXF files
   python scripts/regenerate_all.py
   ```

## See Also

- [README.md](README.md) - Project overview
- [examples/translation_example.ipynb](examples/translation_example.ipynb) - Jupyter notebook tutorial
- [examples/recursive_translation_example.py](examples/recursive_translation_example.py) - Complete examples
- [tests/translator/test_recursive_translation.py](tests/translator/test_recursive_translation.py) - Test suite
