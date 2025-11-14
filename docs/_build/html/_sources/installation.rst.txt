Installation
============

Requirements
------------

* Python 3.8 or higher
* NumPy >= 1.20.0 (for certain blocks like TimeTable)
* pip (Python package installer)

Virtual Environment Setup (Recommended)
----------------------------------------

Using a virtual environment isolates dependencies and avoids conflicts.

**Linux/macOS:**

.. code-block:: bash

    # Create virtual environment
    python3 -m venv venv

    # Activate virtual environment
    source venv/bin/activate

**Windows:**

.. code-block:: bash

    # Create virtual environment
    python -m venv venv

    # Activate virtual environment
    venv\Scripts\activate

Basic Installation
------------------

Clone the repository and install:

.. code-block:: bash

    git clone https://github.com/yourusername/CDLPython.git
    cd CDLPython
    pip install -e .

Or using requirements file:

.. code-block:: bash

    pip install -r requirements.txt

Development Installation
------------------------

For development with testing and code quality tools:

**Option 1: Using setup.py extras**

.. code-block:: bash

    pip install -e ".[dev]"

**Option 2: Using requirements file**

.. code-block:: bash

    pip install -r requirements-dev.txt

This installs:

* pytest, pytest-cov - for testing
* black, flake8, mypy, pylint - for code quality
* All core dependencies

Documentation Installation
--------------------------

For building documentation:

**Option 1: Using setup.py extras**

.. code-block:: bash

    pip install -e ".[docs]"

**Option 2: Using requirements file**

.. code-block:: bash

    pip install -r requirements-docs.txt

This installs:

* Sphinx - documentation generator
* sphinx-rtd-theme - Read the Docs theme
* sphinx-autodoc-typehints - type hints in documentation
* Additional Sphinx extensions

Complete Installation (Development + Docs)
-------------------------------------------

To install everything at once:

.. code-block:: bash

    pip install -e ".[dev,docs]"

Or using all requirements files:

.. code-block:: bash

    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    pip install -r requirements-docs.txt

Verify Installation
-------------------

Test that the package is installed correctly:

.. code-block:: bash

    # Test basic import
    python -c "from cdl_python.CDL.Reals.Sources import Constant; print('Success!')"

    # Run tests
    pytest tests/

    # Check tools
    pytest --version
    sphinx-build --version

You should see all tests passing.

Building Documentation
----------------------

After installing documentation dependencies, build the docs:

**Linux/macOS:**

.. code-block:: bash

    cd docs
    make html

**Windows:**

.. code-block:: bash

    cd docs
    make.bat html

The generated documentation will be in ``docs/_build/html/``.

View the documentation:

.. code-block:: bash

    # macOS
    open _build/html/index.html

    # Linux
    xdg-open _build/html/index.html

    # Windows
    start _build/html/index.html

Requirements Files
------------------

The project uses three requirements files:

* **requirements.txt** - Core dependencies (numpy)
* **requirements-dev.txt** - Development tools (testing, linting)
* **requirements-docs.txt** - Documentation tools (Sphinx)

See the `SETUP_GUIDE.md <../SETUP_GUIDE.md>`_ for detailed setup instructions.

Troubleshooting
---------------

**Virtual environment issues:**

Make sure the virtual environment is activated before installing packages.

**Import errors:**

Ensure you installed the package with ``pip install -e .``

**Sphinx not found:**

Install documentation dependencies: ``pip install -r requirements-docs.txt``

**Tests failing:**

Install development dependencies: ``pip install -r requirements-dev.txt``

For more help, see the `SETUP_GUIDE.md <../SETUP_GUIDE.md>`_ file.
