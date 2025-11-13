"""Tests for recursive CDL translation with custom blocks"""

import pytest
from pathlib import Path
import sys
import json
import tempfile
import shutil

from cdl_translator.translator import RecursiveTranslator, translate_cxf_recursive
from cdl_translator.parser import CXFParser
from cdl_translator.model import BlockInstance


class TestRecursiveTranslation:
    """Test recursive translation of CDL models with custom blocks"""

    @pytest.fixture
    def fixtures_dir(self):
        """Get path to test fixtures directory"""
        return Path(__file__).parent / "fixtures" / "modelica-json" / "cxf"

    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    def test_custom_block_detection(self, fixtures_dir):
        """Test that custom blocks are correctly identified"""
        # Parse MyController which has custom blocks
        with open(fixtures_dir / "MyController.jsonld", 'r') as f:
            data = json.load(f)

        parser = CXFParser()
        model = parser.parse_dict(data)

        # Check instances
        assert len(model.instances) == 3

        # Find custom blocks
        custom_blocks = [inst for inst in model.instances if inst.is_custom_block()]
        standard_blocks = [inst for inst in model.instances if inst.is_standard_cdl_block()]

        # Should have 2 custom blocks (subCon1, subCon2) and 1 standard (add2)
        assert len(custom_blocks) == 2
        assert len(standard_blocks) == 1

        # Check custom block names
        custom_names = {inst.instance_name for inst in custom_blocks}
        assert custom_names == {'subCon1', 'subCon2'}

        # Check custom block type extraction
        for custom_inst in custom_blocks:
            assert custom_inst.get_custom_block_name() == 'SubController'

    def test_multiple_connections_parsing(self, fixtures_dir):
        """Test that parser handles ports with multiple connections"""
        # Parse MyController where u2 connects to 3 targets
        with open(fixtures_dir / "MyController.jsonld", 'r') as f:
            data = json.load(f)

        parser = CXFParser()
        model = parser.parse_dict(data)

        # Should find all 5 connections:
        # - u1 -> add2.u1
        # - u2 -> add2.u2
        # - u2 -> subCon1.u
        # - u2 -> subCon2.u
        # - add2.y -> y
        assert len(model.connections) == 5

        # Check u2 connections specifically
        u2_connections = [
            conn for conn in model.connections
            if conn.is_from_input() and conn.source_port == 'u2'
        ]
        assert len(u2_connections) == 3

        # Check target blocks
        u2_targets = {conn.target_block for conn in u2_connections}
        assert u2_targets == {'add2', 'subCon1', 'subCon2'}

    def test_recursive_translation_generates_two_files(self, fixtures_dir, temp_output_dir):
        """Test that recursive translation generates files for all blocks"""
        cxf_path = fixtures_dir / "MyController.jsonld"

        # Translate recursively
        generated = translate_cxf_recursive(cxf_path, temp_output_dir)

        # Should generate 2 files: SubController.py and MyController.py
        assert len(generated) == 2
        assert 'SubController' in generated
        assert 'MyController' in generated

        # Check that files were written
        assert (temp_output_dir / "SubController.py").exists()
        assert (temp_output_dir / "MyController.py").exists()

    def test_dependency_order(self, fixtures_dir, temp_output_dir):
        """Test that dependencies are translated before dependents"""
        cxf_path = fixtures_dir / "MyController.jsonld"

        translator = RecursiveTranslator()
        generated = translator.translate_file(cxf_path, temp_output_dir)

        # SubController should be translated before MyController
        # This is implicit in the code - if it runs without error, order is correct
        assert 'SubController' in generated
        assert 'MyController' in generated

        # MyController should import SubController
        my_controller_code = generated['MyController']
        assert 'from SubController import SubController' in my_controller_code

    def test_generated_code_is_valid_python(self, fixtures_dir, temp_output_dir):
        """Test that generated code is syntactically valid Python"""
        cxf_path = fixtures_dir / "MyController.jsonld"
        generated = translate_cxf_recursive(cxf_path, temp_output_dir)

        # Try to compile both files
        for block_name, code in generated.items():
            try:
                compile(code, f"{block_name}.py", 'exec')
            except SyntaxError as e:
                pytest.fail(f"Generated code for {block_name} has syntax error: {e}")

    def test_generated_code_executes(self, fixtures_dir, temp_output_dir):
        """Test that generated code can be imported and executed"""
        cxf_path = fixtures_dir / "MyController.jsonld"
        translate_cxf_recursive(cxf_path, temp_output_dir)

        # Add output directory to path
        sys.path.insert(0, str(temp_output_dir))

        try:
            # Import generated modules
            from SubController import SubController
            from MyController import MyController

            # Test SubController
            sub = SubController()
            result = sub.compute(u=10.0)
            assert result['y'] == 5.0  # 10.0 * 0.5 = 5.0

            # Test MyController
            controller = MyController()
            result = controller.compute(u1=10.0, u2=20.0)
            assert result['y'] == 30.0  # 10.0 + 20.0 = 30.0

            # Test with different inputs
            result = controller.compute(u1=5.0, u2=15.0)
            assert result['y'] == 20.0  # 5.0 + 15.0 = 20.0

        finally:
            # Clean up sys.path
            sys.path.remove(str(temp_output_dir))
            # Remove imported modules
            if 'SubController' in sys.modules:
                del sys.modules['SubController']
            if 'MyController' in sys.modules:
                del sys.modules['MyController']

    def test_custom_blocks_instantiated_correctly(self, fixtures_dir):
        """Test that custom blocks are instantiated with correct names"""
        cxf_path = fixtures_dir / "MyController.jsonld"
        generated = translate_cxf_recursive(cxf_path)

        my_controller_code = generated['MyController']

        # Check that custom blocks are instantiated correctly
        assert 'self.subCon1 = SubController(' in my_controller_code
        assert 'self.subCon2 = SubController(' in my_controller_code

        # Check that standard block is instantiated correctly
        assert 'self.add2 = Add(' in my_controller_code

    def test_custom_blocks_called_in_compute(self, fixtures_dir):
        """Test that custom blocks are called in compute method"""
        cxf_path = fixtures_dir / "MyController.jsonld"
        generated = translate_cxf_recursive(cxf_path)

        my_controller_code = generated['MyController']

        # Check that all blocks are called in compute
        assert 'add2_output = self.add2.compute(' in my_controller_code
        assert 'subCon1_output = self.subCon1.compute(' in my_controller_code
        assert 'subCon2_output = self.subCon2.compute(' in my_controller_code

        # Check that correct inputs are passed
        assert 'u1=u1, u2=u2' in my_controller_code  # add2
        assert 'u=u2' in my_controller_code  # subCon1 and subCon2

    def test_no_duplicate_translation(self, fixtures_dir):
        """Test that blocks are not translated multiple times"""
        cxf_path = fixtures_dir / "MyController.jsonld"

        translator = RecursiveTranslator()
        generated = translator.translate_file(cxf_path)

        # SubController is used twice in MyController, but should only be translated once
        assert len(generated) == 2
        assert 'SubController' in generated

        # Check that translator tracked it as translated
        assert 'SubController' in translator.translated

    def test_custom_block_does_not_require_time_manager(self):
        """Test that custom blocks don't require time manager from parent"""
        # Create a custom block instance
        custom_inst = BlockInstance(
            instance_name='myCustomBlock',
            block_type='ex:CustomBlock',
            parameters={}
        )

        # Custom blocks should not require time manager
        assert custom_inst.is_custom_block()
        assert not custom_inst.needs_time_manager()

    def test_cxf_file_not_found_error(self, fixtures_dir):
        """Test that appropriate error is raised when custom block CXF not found"""
        # Create a temporary CXF that references non-existent custom block
        temp_cxf = {
            "@context": {
                "S231P": "https://data.ashrae.org/S231P#",
                "ex": "http://example.org#"
            },
            "@graph": [
                {
                    "@id": "http://example.org#TestModel",
                    "@type": "S231P:Block",
                    "S231P:label": "TestModel",
                    "S231P:containsBlock": [
                        {"@id": "http://example.org#TestModel.custom"}
                    ]
                },
                {
                    "@id": "http://example.org#TestModel.custom",
                    "@type": "ex:NonExistentBlock",
                    "S231P:label": "custom"
                }
            ]
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir) / "TestModel.jsonld"
            with open(temp_path, 'w') as f:
                json.dump(temp_cxf, f)

            translator = RecursiveTranslator()
            with pytest.raises(FileNotFoundError, match="Could not find CXF file for custom block"):
                translator.translate_file(temp_path)


class TestCXFResolver:
    """Test CXF file resolution for custom blocks"""

    def test_resolve_in_base_directory(self, tmp_path):
        """Test resolving CXF file in base directory"""
        from cdl_translator.resolver import CXFResolver

        # Create test CXF file
        (tmp_path / "CustomBlock.jsonld").touch()

        resolver = CXFResolver()
        result = resolver.resolve("CustomBlock", tmp_path)

        assert result is not None
        assert result == tmp_path / "CustomBlock.jsonld"

    def test_resolve_json_extension(self, tmp_path):
        """Test resolving .json files in addition to .jsonld"""
        from cdl_translator.resolver import CXFResolver

        # Create .json file
        (tmp_path / "CustomBlock.json").touch()

        resolver = CXFResolver()
        result = resolver.resolve("CustomBlock", tmp_path)

        assert result is not None
        assert result == tmp_path / "CustomBlock.json"

    def test_resolve_in_search_paths(self, tmp_path):
        """Test resolving CXF file in additional search paths"""
        from cdl_translator.resolver import CXFResolver

        # Create subdirectory with CXF file
        search_dir = tmp_path / "custom_blocks"
        search_dir.mkdir()
        (search_dir / "CustomBlock.jsonld").touch()

        resolver = CXFResolver(search_paths=[search_dir])
        result = resolver.resolve("CustomBlock", tmp_path)

        assert result is not None
        assert result == search_dir / "CustomBlock.jsonld"

    def test_resolve_not_found(self, tmp_path):
        """Test that None is returned when file not found"""
        from cdl_translator.resolver import CXFResolver

        resolver = CXFResolver()
        result = resolver.resolve("NonExistent", tmp_path)

        assert result is None
