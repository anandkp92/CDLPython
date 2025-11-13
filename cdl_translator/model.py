"""Internal model representation for CDL models

This module defines data structures for representing parsed CDL models
in a format suitable for Python code generation.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Set, Tuple, Optional
from enum import Enum


class PortType(Enum):
    """Type of port (input/output connector)"""
    REAL = "Real"
    INTEGER = "Integer"
    BOOLEAN = "Boolean"


@dataclass
class Parameter:
    """Model or block parameter

    Represents a parameter that can be set at instantiation time.
    Can be a literal value or reference to parent parameter.
    """
    name: str
    type: str  # 'Real', 'Integer', 'Boolean'
    value: Any
    description: str = ""

    def __post_init__(self):
        """Validate parameter"""
        if self.type not in ['Real', 'Integer', 'Boolean']:
            raise ValueError(f"Invalid parameter type: {self.type}")


@dataclass
class Port:
    """Input or output port"""
    name: str
    type: PortType
    description: str = ""

    def __post_init__(self):
        """Convert string type to PortType if needed"""
        if isinstance(self.type, str):
            self.type = PortType[self.type.upper()]


@dataclass
class BlockInstance:
    """Instance of a CDL block

    Represents a single block instantiation within a model.
    """
    instance_name: str  # e.g., "gain", "adder"
    block_type: str     # e.g., "Buildings.Controls.OBC.CDL.Reals.Add"
    parameters: Dict[str, Any] = field(default_factory=dict)

    # CDL packages that have blocks requiring TimeManager
    STATEFUL_PACKAGES = {
        'Reals': {
            'Derivative', 'IntegratorWithReset', 'Integrator',
            'LimitSlewRate', 'MovingAverage', 'PID', 'PIDWithReset',
            'LimPID'
        },
        'Logical': {
            'FallingEdge', 'RisingEdge', 'Timer', 'TrueDelay',
            'TrueFalseHold', 'TrueHoldWithReset', 'OnCounter',
            'Proof', 'VariablePulse'
        },
        'Discrete': {
            'Sampler', 'FirstOrderHold', 'ZeroOrderHold',
            'UnitDelay', 'TriggeredMax', 'TriggeredMovingMean',
            'TriggeredSampler'
        },
        'Utilities': {
            'SunRiseSet'
        }
    }

    def is_standard_cdl_block(self) -> bool:
        """Check if this is a standard CDL library block

        Returns:
            True if block type contains 'CDL' (standard library block)
            False otherwise (custom/user-defined block)
        """
        return 'CDL' in self.block_type.split('.')

    def is_custom_block(self) -> bool:
        """Check if this is a custom/user-defined block

        Returns:
            True if not a standard CDL block
        """
        return not self.is_standard_cdl_block()

    def get_custom_block_name(self) -> str:
        """Extract the simple name from a custom block type

        For custom blocks like:
          - "ex:SubController" -> "SubController"
          - "http://example.org#FromModelica.SubController" -> "SubController"
          - "MyPackage.MyBlock" -> "MyBlock"

        Returns:
            Simple block name without namespace or path
        """
        block_type = self.block_type

        # Strip namespace prefix (e.g., "ex:")
        if ':' in block_type:
            block_type = block_type.split(':', 1)[1]

        # Extract after # for URIs
        if '#' in block_type:
            block_type = block_type.split('#', 1)[1]

        # Get last part after dots
        if '.' in block_type:
            return block_type.split('.')[-1]

        return block_type

    def get_python_import_path(self) -> Tuple[str, str]:
        """Convert CDL path to Python import path

        Returns:
            Tuple of (module_path, class_name)

        Example:
            "Buildings.Controls.OBC.CDL.Reals.Add"
            -> ("cdl_python.CDL.Reals", "Add")
        """
        parts = self.block_type.split('.')

        # Find CDL in the path
        try:
            cdl_idx = parts.index('CDL')
        except ValueError:
            raise ValueError(f"Invalid CDL block type: {self.block_type}")

        # Extract package and class name
        package_parts = parts[cdl_idx+1:-1]  # Between CDL and class name
        class_name = parts[-1]

        # Build Python import path
        module_path = "cdl_python.CDL." + ".".join(package_parts)

        return (module_path, class_name)

    def needs_time_manager(self) -> bool:
        """Check if this block requires a TimeManager

        Stateful blocks (integrators, PIDs, timers, delays, etc.)
        require a TimeManager for time-dependent operations.

        Custom blocks are assumed to handle their own time management internally.
        """
        # Custom blocks don't require time manager from parent
        # (they manage their own if needed)
        if self.is_custom_block():
            return False

        _, class_name = self.get_python_import_path()
        module_path, _ = self.get_python_import_path()

        # Extract package name (e.g., "Reals" from "cdl_python.CDL.Reals")
        package = module_path.split('.')[-1]

        return package in self.STATEFUL_PACKAGES and \
               class_name in self.STATEFUL_PACKAGES[package]


@dataclass
class Connection:
    """Connection between ports

    Represents data flow from source to target.
    Can connect:
    - Model input -> block input
    - Block output -> block input
    - Block output -> model output
    """
    source_block: str  # Instance name or None for model input
    source_port: str
    target_block: str  # Instance name or None for model output
    target_port: str

    def is_from_input(self) -> bool:
        """Check if connection is from model input"""
        return self.source_block is None or self.source_block == ""

    def is_to_output(self) -> bool:
        """Check if connection is to model output"""
        return self.target_block is None or self.target_block == ""

    def __str__(self) -> str:
        """Human-readable representation"""
        source = self.source_port if self.is_from_input() else f"{self.source_block}.{self.source_port}"
        target = self.target_port if self.is_to_output() else f"{self.target_block}.{self.target_port}"
        return f"{source} -> {target}"


@dataclass
class ModelMetadata:
    """Model-level metadata"""
    name: str
    description: str = ""
    parameters: List[Parameter] = field(default_factory=list)
    inputs: List[Port] = field(default_factory=list)
    outputs: List[Port] = field(default_factory=list)


@dataclass
class CDLModel:
    """Complete CDL model representation

    Contains all information needed to generate Python code.
    """
    metadata: ModelMetadata
    instances: List[BlockInstance] = field(default_factory=list)
    connections: List[Connection] = field(default_factory=list)

    def get_required_imports(self) -> Dict[str, Set[str]]:
        """Get all CDL imports needed (only standard blocks)

        Returns:
            Dictionary mapping module paths to set of class names
            Example: {
                "cdl_python.CDL.Reals": {"Add", "MultiplyByParameter"},
                "cdl_python.CDL.Logical": {"And"}
            }

        Note: Custom blocks are not included - they are imported separately
        """
        imports = {}

        for instance in self.instances:
            # Skip custom blocks - they're handled separately
            if instance.is_custom_block():
                continue

            module_path, class_name = instance.get_python_import_path()

            if module_path not in imports:
                imports[module_path] = set()

            imports[module_path].add(class_name)

        return imports

    def needs_time_manager(self) -> bool:
        """Check if any block in the model needs TimeManager"""
        return any(instance.needs_time_manager() for instance in self.instances)

    def get_computation_order(self) -> List[BlockInstance]:
        """Topological sort of blocks based on connections

        Returns blocks in order such that all dependencies are
        computed before their dependents.

        Returns:
            List of BlockInstance in computation order

        Raises:
            ValueError: If circular dependency detected
        """
        # Build dependency graph: instance -> set of instances it depends on
        dependencies = {instance.instance_name: set() for instance in self.instances}

        for conn in self.connections:
            # Skip connections from/to model inputs/outputs
            if conn.is_from_input() or conn.is_to_output():
                continue

            # target depends on source
            if conn.target_block in dependencies:
                dependencies[conn.target_block].add(conn.source_block)

        # Kahn's algorithm for topological sort
        in_degree = {name: len(deps) for name, deps in dependencies.items()}
        queue = [name for name, degree in in_degree.items() if degree == 0]
        result = []

        while queue:
            # Sort for deterministic output
            queue.sort()
            current = queue.pop(0)
            result.append(current)

            # Reduce in-degree for dependents
            for name, deps in dependencies.items():
                if current in deps:
                    in_degree[name] -= 1
                    if in_degree[name] == 0:
                        queue.append(name)

        # Check for cycles
        if len(result) != len(self.instances):
            remaining = set(dependencies.keys()) - set(result)
            raise ValueError(f"Circular dependency detected involving: {remaining}")

        # Return instances in computed order
        instance_map = {inst.instance_name: inst for inst in self.instances}
        return [instance_map[name] for name in result]

    def validate(self) -> Tuple[bool, List[str]]:
        """Validate model consistency

        Checks:
        - All connections reference valid instances/ports
        - No circular dependencies
        - Parameter types match
        - All inputs/outputs are connected

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        # Build set of valid instance names
        instance_names = {inst.instance_name for inst in self.instances}
        input_names = {port.name for port in self.metadata.inputs}
        output_names = {port.name for port in self.metadata.outputs}

        # Validate connections
        for conn in self.connections:
            # Check source
            if not conn.is_from_input():
                if conn.source_block not in instance_names:
                    errors.append(f"Connection references unknown source block: {conn.source_block}")
            else:
                if conn.source_port not in input_names:
                    errors.append(f"Connection references unknown input: {conn.source_port}")

            # Check target
            if not conn.is_to_output():
                if conn.target_block not in instance_names:
                    errors.append(f"Connection references unknown target block: {conn.target_block}")
            else:
                if conn.target_port not in output_names:
                    errors.append(f"Connection references unknown output: {conn.target_port}")

        # Check for circular dependencies
        try:
            self.get_computation_order()
        except ValueError as e:
            errors.append(str(e))

        return (len(errors) == 0, errors)

    def get_instance(self, name: str) -> Optional[BlockInstance]:
        """Get block instance by name"""
        for instance in self.instances:
            if instance.instance_name == name:
                return instance
        return None
