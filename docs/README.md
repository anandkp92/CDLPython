# CDL Python Documentation

This directory contains the Sphinx documentation for CDL Python.

## Building the Documentation

### Prerequisites

Install the documentation dependencies:

```bash
pip install -e ".[docs]"
```

This will install:
- Sphinx
- sphinx-rtd-theme (Read the Docs theme)
- sphinx-autodoc-typehints

### Build HTML Documentation

On Linux/macOS:
```bash
cd docs
make html
```

On Windows:
```bash
cd docs
make.bat html
```

The generated documentation will be in `docs/_build/html/`.

### View the Documentation

Open `docs/_build/html/index.html` in your web browser:

**macOS:**
```bash
open _build/html/index.html
```

**Linux:**
```bash
xdg-open _build/html/index.html
```

**Windows:**
```bash
start _build/html/index.html
```

### Clean Build Files

To remove all generated files:

**Linux/macOS:**
```bash
make clean
```

**Windows:**
```bash
make.bat clean
```

## Building Other Formats

Sphinx can generate documentation in various formats:

### PDF (requires LaTeX)
```bash
make latexpdf
```

### ePub
```bash
make epub
```

### Plain Text
```bash
make text
```

### Man Pages
```bash
make man
```

## Documentation Structure

```
docs/
├── conf.py              # Sphinx configuration
├── index.rst            # Main documentation index
├── installation.rst     # Installation guide
├── quickstart.rst       # Quick start guide
├── changelog.rst        # Version history
├── contributing.rst     # Contribution guidelines
├── license.rst          # License information
├── api/                 # API reference
│   ├── index.rst
│   ├── cdl_python.rst
│   └── cdl_translator.rst
├── examples/            # Usage examples
│   ├── index.rst
│   ├── sources.rst
│   ├── control_systems.rst
│   ├── time_tables.rst
│   └── cxf_translation.rst
├── _static/             # Static files (CSS, images, etc.)
└── _templates/          # Custom Sphinx templates
```

## Auto-Generated API Documentation

The API documentation is automatically generated from docstrings using Sphinx's `autodoc` extension. The documentation includes:

### cdl_python package
- Core modules (base, time_manager)
- CDL blocks organized by package:
  - Reals (math, sources, limiters, PID, etc.)
  - Integers (math, sources, conversions)
  - Logical (operations, sources)
  - Conversions
  - Discrete
  - Routing
  - Utilities
  - Psychrometrics

### cdl_translator package
- CXF Parser
- Python Code Generator
- CLI tools

## Updating Documentation

### Adding New Modules

When you add new modules or blocks:

1. Ensure they have proper docstrings
2. Add them to the appropriate `.rst` file in `docs/api/`
3. Rebuild the documentation to verify

### Docstring Format

Use Google-style docstrings:

```python
def my_function(param1: str, param2: int) -> bool:
    """Brief description.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When something is wrong

    Example:
        >>> my_function("hello", 42)
        True
    """
    return True
```

## Continuous Integration

The documentation is automatically built and deployed on Read the Docs when changes are pushed to the main branch.

Configuration: `.readthedocs.yaml` in the project root.

## Troubleshooting

### "sphinx-build: command not found"
Install Sphinx: `pip install sphinx`

### "Theme not found"
Install the theme: `pip install sphinx-rtd-theme`

### Module import errors
Make sure the package is installed: `pip install -e .`

### Outdated API docs
Run `make clean` then `make html` to rebuild from scratch

## Contributing to Documentation

See [Contributing Guide](contributing.rst) for guidelines on:
- Writing clear documentation
- Adding examples
- Improving API docs
- Fixing typos and errors

## Resources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- [Read the Docs](https://docs.readthedocs.io/)
