Contributing
============

We welcome contributions to CDL Python! This guide will help you get started.

Getting Started
---------------

1. Fork the repository on GitHub
2. Clone your fork locally::

    git clone https://github.com/yourusername/CDLPython.git
    cd CDLPython

3. Create a virtual environment::

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

4. Install development dependencies::

    pip install -e ".[dev,docs]"

5. Create a branch for your changes::

    git checkout -b feature/your-feature-name

Development Workflow
--------------------

Running Tests
~~~~~~~~~~~~~

Run the full test suite::

    pytest tests/

Run tests with coverage::

    pytest tests/ --cov=cdl_python --cov=cdl_translator --cov-report=html

Run specific test file::

    pytest tests/test_sources.py

Run tests matching a pattern::

    pytest tests/ -k "test_pulse"

Code Style
~~~~~~~~~~

* Follow PEP 8 style guidelines
* Use meaningful variable and function names
* Add docstrings to all public functions and classes
* Keep functions focused and concise

Documentation
~~~~~~~~~~~~~

* Use Google-style docstrings
* Include type hints for function parameters and return values
* Add examples to docstrings when helpful

Example docstring::

    def add_numbers(a: float, b: float) -> float:
        """Add two numbers together.

        Args:
            a: First number
            b: Second number

        Returns:
            Sum of a and b

        Example:
            >>> add_numbers(2.0, 3.0)
            5.0
        """
        return a + b

Adding a New CDL Block
----------------------

To add a new elementary block:

1. Create the block file in the appropriate package::

    cdl_python/CDL/[Package]/[BlockName].py

2. Implement the block class::

    from typing import Dict, Any
    from cdl_python.base import CDLBlock

    class MyBlock(CDLBlock):
        """Short description of the block

        Longer description explaining what the block does,
        its parameters, and outputs.

        Parameters:
            param1: Description of parameter 1
            param2: Description of parameter 2

        Outputs:
            y: Description of output
        """

        def __init__(self, time_manager, param1=default1, param2=default2):
            super().__init__(time_manager)
            self.param1 = param1
            self.param2 = param2

        def compute(self, u: float) -> Dict[str, Any]:
            """Compute block output

            Args:
                u: Input value

            Returns:
                Dictionary with 'y': output value
            """
            # Implementation here
            y = self.param1 * u + self.param2
            return {'y': y}

3. Add exports to ``__init__.py``::

    from .MyBlock import MyBlock

    __all__ = [..., 'MyBlock']

4. Write tests in ``tests/test_[package].py``::

    def test_my_block():
        """Test MyBlock basic functionality"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION)
        block = MyBlock(time_manager=tm, param1=2.0, param2=1.0)

        result = block.compute(u=5.0)
        assert result['y'] == 11.0  # 2.0 * 5.0 + 1.0

5. Add documentation if needed

6. Run tests to verify::

    pytest tests/test_[package].py -v

Building Documentation
----------------------

To build the HTML documentation::

    cd docs
    make html

View the documentation::

    open _build/html/index.html  # macOS
    xdg-open _build/html/index.html  # Linux
    start _build/html/index.html  # Windows

To rebuild after changes::

    make clean
    make html

Submitting Changes
------------------

1. Ensure all tests pass::

    pytest tests/

2. Ensure documentation builds without errors::

    cd docs
    make html

3. Commit your changes::

    git add .
    git commit -m "Add feature: brief description"

4. Push to your fork::

    git push origin feature/your-feature-name

5. Create a Pull Request on GitHub

6. Wait for review and address any feedback

Pull Request Guidelines
-----------------------

* **Clear description**: Explain what the PR does and why
* **Tests included**: Add tests for new functionality
* **Documentation updated**: Update docs if adding features
* **Single concern**: Each PR should address one feature/fix
* **Small commits**: Break large changes into logical commits
* **Clean history**: Squash trivial commits if needed

Reporting Issues
----------------

When reporting bugs, please include:

* Python version
* Operating system
* Steps to reproduce the issue
* Expected vs actual behavior
* Error messages and stack traces
* Minimal example code if applicable

Feature requests should include:

* Clear description of the feature
* Use case and motivation
* Example of how it would be used
* Any relevant references (CDL spec, etc.)

Code of Conduct
---------------

* Be respectful and professional
* Welcome newcomers and be patient
* Focus on constructive feedback
* Respect different viewpoints and experiences

Questions?
----------

If you have questions about contributing:

* Open an issue on GitHub
* Check existing issues and documentation
* Reach out to the maintainers

Thank you for contributing to CDL Python!
