# CDL Python Setup Guide

Complete guide for setting up CDL Python for development and documentation.

## Table of Contents

- [Basic Installation](#basic-installation)
- [Development Setup](#development-setup)
- [Documentation Setup](#documentation-setup)
- [Virtual Environment Setup](#virtual-environment-setup)
- [Verification](#verification)

## Basic Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- git

### Quick Install

For basic usage:

```bash
git clone https://github.com/yourusername/CDLPython.git
cd CDLPython
pip install -e .
```

This installs the package with core dependencies only (numpy).

## Development Setup

### Option 1: Using pip install with extras

```bash
# Install package with development dependencies
pip install -e ".[dev]"
```

### Option 2: Using requirements files

```bash
# Install development dependencies
pip install -r requirements-dev.txt
```

This includes:
- pytest and pytest-cov (testing)
- black, flake8, mypy, pylint (code quality)
- All core dependencies

### Running Tests

After installation, verify everything works:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=cdl_python --cov=cdl_translator --cov-report=html

# Run specific test file
pytest tests/test_sources.py -v
```

## Documentation Setup

### Option 1: Using pip install with extras

```bash
# Install package with documentation dependencies
pip install -e ".[docs]"
```

### Option 2: Using requirements files

```bash
# Install documentation dependencies
pip install -r requirements-docs.txt
```

This includes:
- Sphinx (documentation generator)
- sphinx-rtd-theme (Read the Docs theme)
- sphinx-autodoc-typehints (type hints in docs)
- Other documentation tools

### Building Documentation

```bash
cd docs

# On Linux/macOS
make html

# On Windows
make.bat html
```

View the generated documentation:

```bash
# macOS
open _build/html/index.html

# Linux
xdg-open _build/html/index.html

# Windows
start _build/html/index.html
```

### Clean and Rebuild

```bash
# Clean all generated files
make clean

# Full rebuild
make clean && make html
```

## Virtual Environment Setup

Using a virtual environment is highly recommended to avoid dependency conflicts.

### Using venv (Python 3.8+)

**Linux/macOS:**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt          # For basic usage
pip install -r requirements-dev.txt      # For development
pip install -r requirements-docs.txt     # For documentation

# Or install everything at once
pip install -e ".[dev,docs]"

# Deactivate when done
deactivate
```

**Windows:**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt          # For basic usage
pip install -r requirements-dev.txt      # For development
pip install -r requirements-docs.txt     # For documentation

# Or install everything at once
pip install -e ".[dev,docs]"

# Deactivate when done
deactivate
```

### Using conda

```bash
# Create conda environment
conda create -n cdl_python python=3.11

# Activate environment
conda activate cdl_python

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -r requirements-docs.txt

# Or install everything
pip install -e ".[dev,docs]"

# Deactivate when done
conda deactivate
```

## Complete Setup Workflow

Here's a recommended workflow for getting everything set up:

### 1. Clone and Create Virtual Environment

```bash
# Clone repository
git clone https://github.com/yourusername/CDLPython.git
cd CDLPython

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

### 2. Install All Dependencies

```bash
# Install everything (recommended for contributors)
pip install -e ".[dev,docs]"

# Or install separately
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -r requirements-docs.txt
```

### 3. Verify Installation

```bash
# Run tests
pytest tests/

# Build documentation
cd docs
make html
cd ..
```

### 4. Configure IDE (Optional)

**VSCode:**

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"],
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black"
}
```

**PyCharm:**

1. File → Settings → Project → Python Interpreter
2. Click gear icon → Add
3. Select "Virtualenv Environment" → Existing environment
4. Browse to `venv/bin/python` (or `venv\Scripts\python.exe` on Windows)

## Requirements Files Summary

The project uses three requirements files:

### requirements.txt
Core dependencies needed to use the package:
- numpy

Install with: `pip install -r requirements.txt`

### requirements-dev.txt
Development dependencies for testing and code quality:
- Includes all from requirements.txt
- pytest, pytest-cov
- black, flake8, mypy, pylint

Install with: `pip install -r requirements-dev.txt`

### requirements-docs.txt
Documentation dependencies for building docs:
- Includes all from requirements.txt
- Sphinx and extensions
- Sphinx themes and plugins

Install with: `pip install -r requirements-docs.txt`

## Verification

### Verify Core Installation

```python
# Test basic import
python -c "from cdl_python.CDL.Reals.Sources import Constant; print('Core installed!')"
```

### Verify Development Tools

```bash
# Check pytest
pytest --version

# Check code formatters
black --version
flake8 --version
mypy --version
```

### Verify Documentation Tools

```bash
# Check Sphinx
sphinx-build --version
```

## Troubleshooting

### "No module named 'numpy'"

```bash
pip install numpy>=1.20.0
```

### "No module named 'cdl_python'"

Make sure you installed the package:

```bash
pip install -e .
```

### "sphinx-build: command not found"

Install documentation dependencies:

```bash
pip install -r requirements-docs.txt
```

### Virtual environment not activating

**Linux/macOS:**
- Make sure you're using `source venv/bin/activate`
- Check permissions: `chmod +x venv/bin/activate`

**Windows:**
- Use `venv\Scripts\activate` (not `source`)
- If you get execution policy errors, run PowerShell as admin:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### Tests failing

```bash
# Make sure all dependencies are installed
pip install -r requirements-dev.txt

# Try running specific test file
pytest tests/test_sources.py -v

# Run with verbose output to see errors
pytest tests/ -vv
```

## Next Steps

After setup:

1. Read the [Quick Start Guide](docs/quickstart.rst)
2. Explore the [API Documentation](docs/api/index.rst)
3. Check out [Examples](docs/examples/index.rst)
4. See [Contributing Guide](docs/contributing.rst) if you want to contribute

## Additional Resources

- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [pip User Guide](https://pip.pypa.io/en/stable/user_guide/)
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [pytest Documentation](https://docs.pytest.org/)
