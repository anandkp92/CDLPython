"""Python Code Generator

Generates executable Python code from CDLModel internal representation.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Set
from jinja2 import Environment, FileSystemLoader, select_autoescape
from cdl_translator.model import CDLModel, BlockInstance, Connection


class CodeGenerator:
    """Generate Python code from CDLModel

    Uses Jinja2 templates to generate clean, executable Python code that
    uses the CDL Python library.
    """

    def __init__(self, template_dir: str = None):
        """Initialize code generator

        Args:
            template_dir: Directory containing Jinja2 templates (optional)
        """
        if template_dir is None:
            # Use default templates directory
            template_dir = Path(__file__).parent / "templates"

        self.template_dir = Path(template_dir)

        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def generate(self, model: CDLModel) -> str:
        """Generate complete Python code from model

        Args:
            model: CDLModel to generate code from

        Returns:
            Python source code as string
        """
        # Validate model first
        is_valid, errors = model.validate()
        if not is_valid:
            raise ValueError(f"Cannot generate code from invalid model: {'; '.join(errors)}")

        # Get template
        template = self.env.get_template("class_template.py.jinja2")

        # Prepare template context
        imports = model.get_required_imports()
        compute_body = self._generate_compute_body(model)

        # Render template
        code = template.render(
            model=model,
            imports=imports,
            compute_body=compute_body
        )

        return code

    def _generate_compute_body(self, model: CDLModel) -> str:
        """Generate compute method body

        Args:
            model: CDLModel

        Returns:
            Compute method body (indented Python code)
        """
        lines = []
        indent = "        "  # 8 spaces for method body

        # Build map of instance name -> BlockInstance
        instance_map = {inst.instance_name: inst for inst in model.instances}

        # Track which block outputs we've computed
        computed_outputs = {}  # block.port -> variable_name

        # Get connections in order
        ordered_instances = model.get_computation_order()

        # Process each instance
        for instance in ordered_instances:
            # Find all input connections for this instance
            input_connections = [
                conn for conn in model.connections
                if conn.target_block == instance.instance_name
            ]

            if not input_connections:
                # No inputs connected - skip (might be a constant block)
                continue

            # Build compute call arguments
            args = []
            for conn in input_connections:
                if conn.is_from_input():
                    # Connection from model input
                    args.append(f"{conn.target_port}={conn.source_port}")
                else:
                    # Connection from another block's output
                    source_var = f"{conn.source_block}_output"
                    if source_var not in computed_outputs:
                        # Need to compute source block first
                        lines.append(f"{indent}# {conn.source_block}.{conn.source_port} → {instance.instance_name}.{conn.target_port}")
                        lines.append(f"{indent}{source_var} = self.{conn.source_block}.compute()")
                        computed_outputs[source_var] = True

                    args.append(f"{conn.target_port}={source_var}['{conn.source_port}']")

            # Generate compute call
            output_var = f"{instance.instance_name}_output"
            args_str = ", ".join(args)
            lines.append(f"{indent}{output_var} = self.{instance.instance_name}.compute({args_str})")
            computed_outputs[output_var] = True

        # Add blank line before return
        lines.append("")

        # Build return statement
        return_dict = {}
        for output_port in model.metadata.outputs:
            # Find connection to this output
            for conn in model.connections:
                if conn.is_to_output() and conn.target_port == output_port.name:
                    # Found connection to output
                    source_var = f"{conn.source_block}_output"
                    return_dict[output_port.name] = f"{source_var}['{conn.source_port}']"
                    break

        # Generate return statement
        lines.append(f"{indent}return {{")
        for port_name, value_expr in return_dict.items():
            lines.append(f"{indent}    '{port_name}': {value_expr},")
        lines.append(f"{indent}}}")

        return "\n".join(lines)

    def _sanitize_name(self, name: str) -> str:
        """Convert CDL names to valid Python identifiers

        Args:
            name: CDL name

        Returns:
            Valid Python identifier
        """
        # Replace dots with underscores
        name = name.replace('.', '_')

        # Replace other non-alphanumeric characters with underscores
        name = ''.join(c if c.isalnum() or c == '_' else '_' for c in name)

        # Ensure it doesn't start with a number
        if name and name[0].isdigit():
            name = '_' + name

        return name
