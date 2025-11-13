"""Test suite for CXF to Python translation

Tests the complete pipeline:
1. Parse CXF (JSON-LD) files
2. Validate parsed models
3. Generate Python code
4. Verify syntax
5. Test execution
"""

import json
import os
import ast
import pytest
from pathlib import Path

from cdl_translator.parser import CXFParser
from cdl_translator.codegen import CodeGenerator


# Test data directory
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "modelica-json" / "cxf"

# Standard CDL test files (exclude MyController as it uses custom blocks)
TEST_FILES = [
    "Block1.jsonld",
    "Parameter1.jsonld",
    "BlockInputOutput.jsonld",
    "CustomPWithLimiter.jsonld",
]


class TestCXFParser:
    """Test CXF parsing with S231P namespace format"""

    @pytest.fixture
    def parser(self):
        return CXFParser()

    @pytest.mark.parametrize("filename", TEST_FILES)
    def test_parse_cxf_files(self, parser, filename):
        """Test that all CXF files parse successfully"""
        filepath = FIXTURES_DIR / filename

        with open(filepath, 'r') as f:
            data = json.load(f)

        model = parser.parse_dict(data)

        # Basic checks
        assert model is not None
        assert model.metadata is not None
        assert model.metadata.name is not None
        assert isinstance(model.instances, list)
        assert isinstance(model.connections, list)

    @pytest.mark.parametrize("filename", TEST_FILES)
    def test_validate_parsed_models(self, parser, filename):
        """Test that all parsed models pass validation"""
        filepath = FIXTURES_DIR / filename

        with open(filepath, 'r') as f:
            data = json.load(f)

        model = parser.parse_dict(data)
        valid, errors = model.validate()

        assert valid, f"Validation failed: {errors}"
        assert len(errors) == 0


class TestCodeGeneration:
    """Test Python code generation from parsed models"""

    @pytest.fixture
    def parser(self):
        return CXFParser()

    @pytest.fixture
    def codegen(self):
        return CodeGenerator()

    @pytest.mark.parametrize("filename", TEST_FILES)
    def test_generate_python_code(self, parser, codegen, filename):
        """Test that Python code is generated for all models"""
        filepath = FIXTURES_DIR / filename

        with open(filepath, 'r') as f:
            data = json.load(f)

        model = parser.parse_dict(data)
        code = codegen.generate(model)

        # Basic checks
        assert code is not None
        assert len(code) > 0
        assert f"class {model.metadata.name}" in code
        assert "def __init__" in code
        assert "def compute" in code

    @pytest.mark.parametrize("filename", TEST_FILES)
    def test_generated_code_syntax(self, parser, codegen, filename):
        """Test that generated code has valid Python syntax"""
        filepath = FIXTURES_DIR / filename

        with open(filepath, 'r') as f:
            data = json.load(f)

        model = parser.parse_dict(data)
        code = codegen.generate(model)

        # Parse as AST to verify syntax
        try:
            ast.parse(code)
        except SyntaxError as e:
            pytest.fail(f"Generated code has syntax error: {e}")


class TestBlock1:
    """Test Block1 - minimal block with no instances"""

    def test_parse_block1(self):
        parser = CXFParser()

        with open(FIXTURES_DIR / "Block1.jsonld", 'r') as f:
            data = json.load(f)

        model = parser.parse_dict(data)

        assert model.metadata.name == "Block1"
        assert len(model.instances) == 0
        assert len(model.connections) == 0

    def test_generate_block1(self):
        parser = CXFParser()
        codegen = CodeGenerator()

        with open(FIXTURES_DIR / "Block1.jsonld", 'r') as f:
            data = json.load(f)

        model = parser.parse_dict(data)
        code = codegen.generate(model)

        assert "class Block1:" in code
        assert "def compute(self)" in code


class TestParameter1:
    """Test Parameter1 - block with parameter"""

    def test_parse_parameter1(self):
        parser = CXFParser()

        with open(FIXTURES_DIR / "Parameter1.jsonld", 'r') as f:
            data = json.load(f)

        model = parser.parse_dict(data)

        assert model.metadata.name == "Parameter1"
        assert len(model.instances) == 0
        # Check parameter exists
        assert hasattr(model.metadata, 'parameters')
        assert len(model.metadata.parameters) > 0


class TestBlockInputOutput:
    """Test BlockInputOutput - block with input and output"""

    def test_parse_block_input_output(self):
        parser = CXFParser()

        with open(FIXTURES_DIR / "BlockInputOutput.jsonld", 'r') as f:
            data = json.load(f)

        model = parser.parse_dict(data)

        assert model.metadata.name == "BlockInputOutput"
        assert len(model.instances) == 0
        # Check inputs and outputs
        assert len(model.metadata.inputs) == 1
        assert len(model.metadata.outputs) == 1
        assert model.metadata.inputs[0].name == "u"
        assert model.metadata.outputs[0].name == "y"


class TestCustomPWithLimiter:
    """Test CustomPWithLimiter - complex block with instances and connections"""

    def test_parse_custom_p_with_limiter(self):
        parser = CXFParser()

        with open(FIXTURES_DIR / "CustomPWithLimiter.jsonld", 'r') as f:
            data = json.load(f)

        model = parser.parse_dict(data)

        assert model.metadata.name == "CustomPWithLimiter"
        assert len(model.instances) == 2
        assert len(model.connections) == 4

        # Check instances
        instance_names = [inst.instance_name for inst in model.instances]
        assert "gain" in instance_names
        assert "minValue" in instance_names

        # Check connections
        # Expected: e->gain.u, yMax->minValue.u1, gain.y->minValue.u2, minValue.y->y
        connection_strs = []
        for conn in model.connections:
            src = f"{conn.source_block}.{conn.source_port}" if conn.source_block else conn.source_port
            tgt = f"{conn.target_block}.{conn.target_port}" if conn.target_block else conn.target_port
            connection_strs.append(f"{src}->{tgt}")

        assert "e->gain.u" in connection_strs
        assert "yMax->minValue.u1" in connection_strs
        assert "gain.y->minValue.u2" in connection_strs
        assert "minValue.y->y" in connection_strs

    def test_generate_custom_p_with_limiter(self):
        parser = CXFParser()
        codegen = CodeGenerator()

        with open(FIXTURES_DIR / "CustomPWithLimiter.jsonld", 'r') as f:
            data = json.load(f)

        model = parser.parse_dict(data)
        code = codegen.generate(model)

        # Check generated code structure
        assert "class CustomPWithLimiter:" in code
        assert "self.gain = MultiplyByParameter" in code
        assert "self.minValue = Min" in code
        assert "gain_output = self.gain.compute(u=e)" in code
        assert "minValue_output = self.minValue.compute(u1=yMax, u2=gain_output['y'])" in code
        assert "return {" in code
        assert "'y': minValue_output['y']" in code

    def test_execute_custom_p_with_limiter(self, tmp_path):
        """Test execution of generated CustomPWithLimiter code"""
        parser = CXFParser()
        codegen = CodeGenerator()

        with open(FIXTURES_DIR / "CustomPWithLimiter.jsonld", 'r') as f:
            data = json.load(f)

        model = parser.parse_dict(data)
        code = codegen.generate(model)

        # Write to temp file and import
        py_file = tmp_path / "CustomPWithLimiter.py"
        py_file.write_text(code)

        # Import and test
        import sys
        sys.path.insert(0, str(tmp_path))

        try:
            from CustomPWithLimiter import CustomPWithLimiter

            # Create instance
            block = CustomPWithLimiter(k=2.0)

            # Test: y = min(yMax, k*e) = min(10, 2*3) = 6
            result = block.compute(e=3.0, yMax=10.0)
            assert 'y' in result
            assert abs(result['y'] - 6.0) < 1e-6

            # Test: y = min(yMax, k*e) = min(5, 2*3) = 5
            result = block.compute(e=3.0, yMax=5.0)
            assert abs(result['y'] - 5.0) < 1e-6

        finally:
            sys.path.remove(str(tmp_path))


class TestS231PFormatSupport:
    """Test S231P namespace format support"""

    def test_namespace_extraction(self):
        """Test that S231P: prefixed properties are extracted correctly"""
        parser = CXFParser()

        # All test files use S231P namespace
        with open(FIXTURES_DIR / "CustomPWithLimiter.jsonld", 'r') as f:
            data = json.load(f)

        # Verify @context has S231P namespace
        assert '@context' in data
        assert 'S231P' in data['@context']

        # Parse and verify properties were extracted
        model = parser.parse_dict(data)
        assert model.metadata.name == "CustomPWithLimiter"
        assert len(model.metadata.inputs) == 2  # e and yMax
        assert len(model.metadata.outputs) == 1  # y

    def test_id_resolution(self):
        """Test that @id references are resolved correctly"""
        parser = CXFParser()

        with open(FIXTURES_DIR / "CustomPWithLimiter.jsonld", 'r') as f:
            data = json.load(f)

        model = parser.parse_dict(data)

        # Check that contained blocks were resolved from @id references
        assert len(model.instances) == 2

        # Check that connections reference resolved ports
        assert len(model.connections) == 4
