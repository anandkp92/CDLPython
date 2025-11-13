# ABOUTME: Tests for CXF JSON parser
import pytest
import json
from pathlib import Path
from cdl_translator.parser import CXFParser
from cdl_translator.model import CDLModel, PortType


class TestCXFParser:
    """Test CXF parser"""

    @pytest.fixture
    def parser(self):
        """Create parser instance"""
        return CXFParser()

    @pytest.fixture
    def fixtures_dir(self):
        """Get fixtures directory"""
        return Path(__file__).parent / "fixtures"

    def test_parse_simple_add(self, parser, fixtures_dir):
        """Parse simple Add model"""
        cxf_path = fixtures_dir / "simple_add.json"
        model = parser.parse_file(str(cxf_path))

        # Check metadata
        assert model.metadata.name == "SimpleAdder"
        assert "adds two inputs" in model.metadata.description.lower()
        assert len(model.metadata.inputs) == 2
        assert len(model.metadata.outputs) == 1

        # Check inputs
        input_names = {port.name for port in model.metadata.inputs}
        assert "u1" in input_names
        assert "u2" in input_names
        assert all(port.type == PortType.REAL for port in model.metadata.inputs)

        # Check outputs
        assert model.metadata.outputs[0].name == "y"
        assert model.metadata.outputs[0].type == PortType.REAL

        # Check instances
        assert len(model.instances) == 1
        adder = model.instances[0]
        assert adder.instance_name == "adder"
        assert adder.block_type == "Buildings.Controls.OBC.CDL.Reals.Add"

        # Check connections
        assert len(model.connections) == 3

        # Verify connection structure (input -> block -> output)
        conn_strs = [str(conn) for conn in model.connections]
        assert any("u1 -> adder.u1" in s for s in conn_strs)
        assert any("u2 -> adder.u2" in s for s in conn_strs)
        assert any("adder.y -> y" in s for s in conn_strs)

    def test_parse_custom_p_with_limiter(self, parser, fixtures_dir):
        """Parse CustomPWithLimiter model"""
        cxf_path = fixtures_dir / "custom_p_with_limiter.json"
        model = parser.parse_file(str(cxf_path))

        # Check metadata
        assert model.metadata.name == "CustomPWithLimiter"
        assert "p controller" in model.metadata.description.lower()

        # Check parameters
        assert len(model.metadata.parameters) == 1
        param = model.metadata.parameters[0]
        assert param.name == "k"
        assert param.value == 2.0
        assert param.type == "Real"

        # Check inputs
        assert len(model.metadata.inputs) == 2
        input_names = {port.name for port in model.metadata.inputs}
        assert "e" in input_names
        assert "yMax" in input_names

        # Check outputs
        assert len(model.metadata.outputs) == 1
        assert model.metadata.outputs[0].name == "y"

        # Check instances
        assert len(model.instances) == 2
        instance_names = {inst.instance_name for inst in model.instances}
        assert "gain" in instance_names
        assert "minValue" in instance_names

        # Check gain block
        gain = model.get_instance("gain")
        assert gain is not None
        assert gain.block_type == "Buildings.Controls.OBC.CDL.Reals.MultiplyByParameter"
        assert "k" in gain.parameters
        assert gain.parameters["k"] == "self.k"  # Should reference parent parameter

        # Check minValue block
        min_block = model.get_instance("minValue")
        assert min_block is not None
        assert min_block.block_type == "Buildings.Controls.OBC.CDL.Reals.Min"

        # Check connections (4 total: 2 inputs, 1 internal, 1 output)
        assert len(model.connections) == 4

    def test_parse_file_not_found(self, parser):
        """Non-existent file should raise error"""
        with pytest.raises(FileNotFoundError):
            parser.parse_file("nonexistent.json")

    def test_parse_invalid_json(self, parser, tmp_path):
        """Invalid JSON should raise error"""
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("not valid json {")

        with pytest.raises(json.JSONDecodeError):
            parser.parse_file(str(bad_file))

    def test_parse_missing_graph(self, parser):
        """CXF without @graph should raise error"""
        cxf_data = {"@context": "http://example.com"}

        with pytest.raises(ValueError, match="@graph"):
            parser.parse_dict(cxf_data)

    def test_parse_empty_graph(self, parser):
        """CXF with empty @graph should raise error"""
        cxf_data = {"@graph": []}

        with pytest.raises(ValueError, match="@graph"):
            parser.parse_dict(cxf_data)

    def test_parse_missing_id(self, parser):
        """Model without @id should raise error"""
        cxf_data = {
            "@graph": [{
                "@type": "CompositeBlock"
            }]
        }

        with pytest.raises(ValueError, match="@id"):
            parser.parse_dict(cxf_data)

    def test_parse_missing_type(self, parser):
        """Model without @type should raise error"""
        cxf_data = {
            "@graph": [{
                "@id": "TestModel"
            }]
        }

        with pytest.raises(ValueError, match="@type"):
            parser.parse_dict(cxf_data)

    def test_get_required_imports(self, parser, fixtures_dir):
        """Test import collection"""
        cxf_path = fixtures_dir / "custom_p_with_limiter.json"
        model = parser.parse_file(str(cxf_path))

        imports = model.get_required_imports()

        assert "cdl_python.CDL.Reals" in imports
        assert "MultiplyByParameter" in imports["cdl_python.CDL.Reals"]
        assert "Min" in imports["cdl_python.CDL.Reals"]

    def test_computation_order(self, parser, fixtures_dir):
        """Test topological sorting of blocks"""
        cxf_path = fixtures_dir / "custom_p_with_limiter.json"
        model = parser.parse_file(str(cxf_path))

        order = model.get_computation_order()
        order_names = [inst.instance_name for inst in order]

        # gain must come before minValue (gain.y -> minValue.u2)
        assert order_names.index("gain") < order_names.index("minValue")

    def test_model_validation(self, parser, fixtures_dir):
        """Parsed models should be valid"""
        for fixture_file in ["simple_add.json", "custom_p_with_limiter.json"]:
            cxf_path = fixtures_dir / fixture_file
            model = parser.parse_file(str(cxf_path))

            is_valid, errors = model.validate()
            assert is_valid is True, f"Model {fixture_file} invalid: {errors}"
            assert len(errors) == 0
