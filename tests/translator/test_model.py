# ABOUTME: Tests for CDL model representation classes
import pytest
from cdl_translator.model import (
    Parameter,
    Port,
    PortType,
    BlockInstance,
    Connection,
    ModelMetadata,
    CDLModel,
)


class TestParameter:
    """Test Parameter class"""

    def test_parameter_creation(self):
        """Create a parameter"""
        param = Parameter(name="k", type="Real", value=2.0, description="Gain")
        assert param.name == "k"
        assert param.type == "Real"
        assert param.value == 2.0
        assert param.description == "Gain"

    def test_invalid_parameter_type(self):
        """Invalid parameter type should raise error"""
        with pytest.raises(ValueError):
            Parameter(name="k", type="InvalidType", value=1.0)


class TestPort:
    """Test Port class"""

    def test_port_creation_with_enum(self):
        """Create port with PortType enum"""
        port = Port(name="u", type=PortType.REAL, description="Input")
        assert port.name == "u"
        assert port.type == PortType.REAL
        assert port.description == "Input"

    def test_port_creation_with_string(self):
        """Create port with string type (auto-converted)"""
        port = Port(name="u", type="REAL")
        assert port.type == PortType.REAL


class TestBlockInstance:
    """Test BlockInstance class"""

    def test_block_instance_creation(self):
        """Create a block instance"""
        instance = BlockInstance(
            instance_name="gain",
            block_type="Buildings.Controls.OBC.CDL.Reals.MultiplyByParameter",
            parameters={"k": 2.0}
        )
        assert instance.instance_name == "gain"
        assert instance.block_type == "Buildings.Controls.OBC.CDL.Reals.MultiplyByParameter"
        assert instance.parameters["k"] == 2.0

    def test_get_python_import_path(self):
        """Test CDL to Python import path conversion"""
        instance = BlockInstance(
            instance_name="adder",
            block_type="Buildings.Controls.OBC.CDL.Reals.Add"
        )
        module_path, class_name = instance.get_python_import_path()
        assert module_path == "cdl_python.CDL.Reals"
        assert class_name == "Add"

    def test_get_python_import_path_nested(self):
        """Test import path for nested packages"""
        instance = BlockInstance(
            instance_name="dewpt",
            block_type="Buildings.Controls.OBC.CDL.Psychrometrics.DewPoint_TDryBulPhi"
        )
        module_path, class_name = instance.get_python_import_path()
        assert module_path == "cdl_python.CDL.Psychrometrics"
        assert class_name == "DewPoint_TDryBulPhi"

    def test_needs_time_manager_stateful_block(self):
        """Stateful blocks should need TimeManager"""
        # PID needs TimeManager
        pid = BlockInstance(
            instance_name="pid",
            block_type="Buildings.Controls.OBC.CDL.Reals.PID"
        )
        assert pid.needs_time_manager() is True

        # Integrator needs TimeManager
        integrator = BlockInstance(
            instance_name="int",
            block_type="Buildings.Controls.OBC.CDL.Reals.IntegratorWithReset"
        )
        assert integrator.needs_time_manager() is True

        # Timer needs TimeManager
        timer = BlockInstance(
            instance_name="timer",
            block_type="Buildings.Controls.OBC.CDL.Logical.Timer"
        )
        assert timer.needs_time_manager() is True

    def test_needs_time_manager_stateless_block(self):
        """Stateless blocks should not need TimeManager"""
        # Add doesn't need TimeManager
        adder = BlockInstance(
            instance_name="add",
            block_type="Buildings.Controls.OBC.CDL.Reals.Add"
        )
        assert adder.needs_time_manager() is False

        # And doesn't need TimeManager
        and_block = BlockInstance(
            instance_name="and1",
            block_type="Buildings.Controls.OBC.CDL.Logical.And"
        )
        assert and_block.needs_time_manager() is False


class TestConnection:
    """Test Connection class"""

    def test_block_to_block_connection(self):
        """Connection between two blocks"""
        conn = Connection(
            source_block="gain",
            source_port="y",
            target_block="limiter",
            target_port="u"
        )
        assert conn.source_block == "gain"
        assert conn.source_port == "y"
        assert conn.target_block == "limiter"
        assert conn.target_port == "u"
        assert conn.is_from_input() is False
        assert conn.is_to_output() is False

    def test_input_to_block_connection(self):
        """Connection from model input to block"""
        conn = Connection(
            source_block="",
            source_port="e",
            target_block="gain",
            target_port="u"
        )
        assert conn.is_from_input() is True
        assert conn.is_to_output() is False

    def test_block_to_output_connection(self):
        """Connection from block to model output"""
        conn = Connection(
            source_block="limiter",
            source_port="y",
            target_block="",
            target_port="y"
        )
        assert conn.is_from_input() is False
        assert conn.is_to_output() is True

    def test_connection_string_representation(self):
        """Test string representation of connections"""
        # Block to block
        conn1 = Connection("gain", "y", "limiter", "u")
        assert str(conn1) == "gain.y -> limiter.u"

        # Input to block
        conn2 = Connection("", "e", "gain", "u")
        assert str(conn2) == "e -> gain.u"

        # Block to output
        conn3 = Connection("limiter", "y", "", "y")
        assert str(conn3) == "limiter.y -> y"


class TestCDLModel:
    """Test CDLModel class"""

    def test_simple_model_creation(self):
        """Create a simple model"""
        metadata = ModelMetadata(
            name="SimpleAdder",
            description="Adds two inputs",
            inputs=[Port("u1", PortType.REAL), Port("u2", PortType.REAL)],
            outputs=[Port("y", PortType.REAL)]
        )

        instances = [
            BlockInstance("adder", "Buildings.Controls.OBC.CDL.Reals.Add")
        ]

        connections = [
            Connection("", "u1", "adder", "u1"),
            Connection("", "u2", "adder", "u2"),
            Connection("adder", "y", "", "y")
        ]

        model = CDLModel(metadata=metadata, instances=instances, connections=connections)
        assert model.metadata.name == "SimpleAdder"
        assert len(model.instances) == 1
        assert len(model.connections) == 3

    def test_get_required_imports(self):
        """Test import collection"""
        instances = [
            BlockInstance("add1", "Buildings.Controls.OBC.CDL.Reals.Add"),
            BlockInstance("mult1", "Buildings.Controls.OBC.CDL.Reals.MultiplyByParameter"),
            BlockInstance("and1", "Buildings.Controls.OBC.CDL.Logical.And")
        ]

        model = CDLModel(
            metadata=ModelMetadata(name="Test"),
            instances=instances
        )

        imports = model.get_required_imports()
        assert "cdl_python.CDL.Reals" in imports
        assert "Add" in imports["cdl_python.CDL.Reals"]
        assert "MultiplyByParameter" in imports["cdl_python.CDL.Reals"]
        assert "cdl_python.CDL.Logical" in imports
        assert "And" in imports["cdl_python.CDL.Logical"]

    def test_needs_time_manager_with_stateful_blocks(self):
        """Model with stateful blocks needs TimeManager"""
        instances = [
            BlockInstance("pid", "Buildings.Controls.OBC.CDL.Reals.PID"),
            BlockInstance("add", "Buildings.Controls.OBC.CDL.Reals.Add")
        ]

        model = CDLModel(
            metadata=ModelMetadata(name="Test"),
            instances=instances
        )

        assert model.needs_time_manager() is True

    def test_needs_time_manager_without_stateful_blocks(self):
        """Model without stateful blocks doesn't need TimeManager"""
        instances = [
            BlockInstance("add", "Buildings.Controls.OBC.CDL.Reals.Add"),
            BlockInstance("mult", "Buildings.Controls.OBC.CDL.Reals.Multiply")
        ]

        model = CDLModel(
            metadata=ModelMetadata(name="Test"),
            instances=instances
        )

        assert model.needs_time_manager() is False

    def test_computation_order_simple_chain(self):
        """Test topological sort for simple chain: A -> B -> C"""
        instances = [
            BlockInstance("blockC", "Buildings.Controls.OBC.CDL.Reals.Add"),
            BlockInstance("blockA", "Buildings.Controls.OBC.CDL.Reals.Add"),
            BlockInstance("blockB", "Buildings.Controls.OBC.CDL.Reals.Add"),
        ]

        connections = [
            Connection("blockA", "y", "blockB", "u1"),
            Connection("blockB", "y", "blockC", "u1"),
        ]

        model = CDLModel(
            metadata=ModelMetadata(name="Test"),
            instances=instances,
            connections=connections
        )

        order = model.get_computation_order()
        order_names = [inst.instance_name for inst in order]

        # A must come before B, B must come before C
        assert order_names.index("blockA") < order_names.index("blockB")
        assert order_names.index("blockB") < order_names.index("blockC")

    def test_computation_order_parallel_blocks(self):
        """Test topological sort for parallel blocks"""
        instances = [
            BlockInstance("mult", "Buildings.Controls.OBC.CDL.Reals.Multiply"),
            BlockInstance("add", "Buildings.Controls.OBC.CDL.Reals.Add"),
            BlockInstance("final", "Buildings.Controls.OBC.CDL.Reals.Add"),
        ]

        connections = [
            # add and mult can run in parallel
            Connection("add", "y", "final", "u1"),
            Connection("mult", "y", "final", "u2"),
        ]

        model = CDLModel(
            metadata=ModelMetadata(name="Test"),
            instances=instances,
            connections=connections
        )

        order = model.get_computation_order()
        order_names = [inst.instance_name for inst in order]

        # add and mult must both come before final
        assert order_names.index("add") < order_names.index("final")
        assert order_names.index("mult") < order_names.index("final")

    def test_computation_order_circular_dependency(self):
        """Circular dependency should raise error"""
        instances = [
            BlockInstance("blockA", "Buildings.Controls.OBC.CDL.Reals.Add"),
            BlockInstance("blockB", "Buildings.Controls.OBC.CDL.Reals.Add"),
        ]

        connections = [
            Connection("blockA", "y", "blockB", "u1"),
            Connection("blockB", "y", "blockA", "u1"),  # Circular!
        ]

        model = CDLModel(
            metadata=ModelMetadata(name="Test"),
            instances=instances,
            connections=connections
        )

        with pytest.raises(ValueError, match="Circular dependency"):
            model.get_computation_order()

    def test_validate_valid_model(self):
        """Valid model should pass validation"""
        metadata = ModelMetadata(
            name="Test",
            inputs=[Port("u", PortType.REAL)],
            outputs=[Port("y", PortType.REAL)]
        )

        instances = [
            BlockInstance("gain", "Buildings.Controls.OBC.CDL.Reals.MultiplyByParameter")
        ]

        connections = [
            Connection("", "u", "gain", "u"),
            Connection("gain", "y", "", "y")
        ]

        model = CDLModel(metadata=metadata, instances=instances, connections=connections)

        is_valid, errors = model.validate()
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_invalid_connection_source(self):
        """Connection to non-existent block should fail validation"""
        metadata = ModelMetadata(name="Test")
        instances = [BlockInstance("gain", "Buildings.Controls.OBC.CDL.Reals.Add")]
        connections = [
            Connection("nonexistent", "y", "gain", "u1")
        ]

        model = CDLModel(metadata=metadata, instances=instances, connections=connections)

        is_valid, errors = model.validate()
        assert is_valid is False
        assert len(errors) > 0
        assert "unknown source block" in errors[0].lower()

    def test_validate_circular_dependency(self):
        """Circular dependency should fail validation"""
        instances = [
            BlockInstance("blockA", "Buildings.Controls.OBC.CDL.Reals.Add"),
            BlockInstance("blockB", "Buildings.Controls.OBC.CDL.Reals.Add"),
        ]

        connections = [
            Connection("blockA", "y", "blockB", "u1"),
            Connection("blockB", "y", "blockA", "u1"),
        ]

        model = CDLModel(
            metadata=ModelMetadata(name="Test"),
            instances=instances,
            connections=connections
        )

        is_valid, errors = model.validate()
        assert is_valid is False
        assert any("circular" in err.lower() for err in errors)

    def test_get_instance(self):
        """Test getting instance by name"""
        instances = [
            BlockInstance("gain", "Buildings.Controls.OBC.CDL.Reals.MultiplyByParameter"),
            BlockInstance("add", "Buildings.Controls.OBC.CDL.Reals.Add")
        ]

        model = CDLModel(
            metadata=ModelMetadata(name="Test"),
            instances=instances
        )

        gain = model.get_instance("gain")
        assert gain is not None
        assert gain.instance_name == "gain"

        nonexistent = model.get_instance("nonexistent")
        assert nonexistent is None
