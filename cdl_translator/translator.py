"""Recursive CDL to Python translator

This module provides the main translator class that handles recursive
translation of CDL models with custom blocks.
"""

import json
from pathlib import Path
from typing import Dict, Set, List, Optional
from collections import defaultdict

from .parser import CXFParser
from .codegen import CodeGenerator
from .model import CDLModel, BlockInstance
from .resolver import CXFResolver


class RecursiveTranslator:
    """Translates CDL models recursively, handling custom blocks"""

    def __init__(self, search_paths: Optional[List[Path]] = None):
        """Initialize translator

        Args:
            search_paths: Additional directories to search for custom block CXF files
        """
        self.parser = CXFParser()
        self.codegen = CodeGenerator()
        self.resolver = CXFResolver(search_paths)

        # Track translated blocks to avoid duplicates
        self.translated: Set[str] = set()

        # Store generated code: block_name -> python_code
        self.generated_code: Dict[str, str] = {}

        # Track dependency chain to detect circular dependencies
        self.dependency_chain: List[str] = []

    def translate_file(
        self,
        cxf_path: Path,
        output_dir: Optional[Path] = None
    ) -> Dict[str, str]:
        """Translate a CXF file and all its custom block dependencies

        Args:
            cxf_path: Path to the main CXF file
            output_dir: Optional directory to write generated files (if None, just return code)

        Returns:
            Dictionary mapping block names to generated Python code

        Raises:
            FileNotFoundError: If CXF file not found
            ValueError: If circular dependency detected
        """
        cxf_path = Path(cxf_path).resolve()

        if not cxf_path.exists():
            raise FileNotFoundError(f"CXF file not found: {cxf_path}")

        # Reset state for new translation
        self.translated.clear()
        self.generated_code.clear()
        self.dependency_chain.clear()

        # Translate recursively
        base_dir = cxf_path.parent
        with open(cxf_path, 'r') as f:
            cxf_data = json.load(f)

        model = self.parser.parse_dict(cxf_data)
        self._translate_model_recursive(model, base_dir)

        # Write files if output directory specified
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            for block_name, code in self.generated_code.items():
                output_file = output_dir / f"{block_name}.py"
                with open(output_file, 'w') as f:
                    f.write(code)

        return self.generated_code

    def _translate_model_recursive(self, model: CDLModel, base_dir: Path):
        """Recursively translate a model and its dependencies

        Args:
            model: Parsed CDL model
            base_dir: Base directory for resolving custom block files

        Raises:
            ValueError: If circular dependency detected
        """
        model_name = model.metadata.name

        # Check for circular dependency
        if model_name in self.dependency_chain:
            chain_str = ' -> '.join(self.dependency_chain + [model_name])
            raise ValueError(f"Circular dependency detected: {chain_str}")

        # Skip if already translated
        if model_name in self.translated:
            return

        # Add to dependency chain
        self.dependency_chain.append(model_name)

        try:
            # Find all custom blocks used by this model
            custom_blocks = self._find_custom_blocks(model)

            # Recursively translate custom block dependencies first
            for custom_instance in custom_blocks:
                block_name = custom_instance.get_custom_block_name()

                # Skip if already translated
                if block_name in self.translated:
                    continue

                # Find CXF file for this custom block
                cxf_path = self.resolver.resolve(block_name, base_dir)

                if cxf_path is None:
                    raise FileNotFoundError(
                        f"Could not find CXF file for custom block: {block_name}\n"
                        f"Searched in: {base_dir}\n"
                        f"Expected files: {block_name}.jsonld or {block_name}.json"
                    )

                # Parse and translate recursively
                with open(cxf_path, 'r') as f:
                    custom_cxf_data = json.load(f)

                custom_model = self.parser.parse_dict(custom_cxf_data)
                custom_base_dir = cxf_path.parent

                # Recursive call
                self._translate_model_recursive(custom_model, custom_base_dir)

            # Now generate code for this model
            # (all dependencies have been translated)
            code = self._generate_code_with_custom_imports(model, custom_blocks)

            # Store generated code
            self.generated_code[model_name] = code
            self.translated.add(model_name)

        finally:
            # Remove from dependency chain
            self.dependency_chain.pop()

    def _find_custom_blocks(self, model: CDLModel) -> List[BlockInstance]:
        """Find all custom block instances in a model

        Args:
            model: CDL model

        Returns:
            List of custom block instances
        """
        return [inst for inst in model.instances if inst.is_custom_block()]

    def _generate_code_with_custom_imports(
        self,
        model: CDLModel,
        custom_blocks: List[BlockInstance]
    ) -> str:
        """Generate Python code with proper custom block imports

        Args:
            model: CDL model
            custom_blocks: List of custom block instances used

        Returns:
            Generated Python code
        """
        # Get custom block names for imports
        custom_block_names = set(block.get_custom_block_name() for block in custom_blocks)

        # Generate code using modified code generator
        # We need to pass custom block information
        code = self.codegen.generate(model, custom_imports=custom_block_names)

        return code


def translate_cxf(
    cxf_path: Path,
    output_dir: Optional[Path] = None,
    search_paths: Optional[List[Path]] = None
) -> Dict[str, str]:
    """Translate a CXF file to Python code

    Automatically handles both:
    - Simple models (only standard CDL blocks) - generates one Python file
    - Complex models (with custom blocks) - recursively translates all dependencies

    Args:
        cxf_path: Path to the main CXF file
        output_dir: Optional directory to write generated files
        search_paths: Additional directories to search for custom blocks

    Returns:
        Dictionary mapping block names to generated Python code

    Examples:
        Simple model (no custom blocks):
        >>> generated = translate_cxf('SimpleController.jsonld', output_dir='generated/')
        >>> # Creates: generated/SimpleController.py

        Complex model (with custom blocks):
        >>> generated = translate_cxf('MyController.jsonld', output_dir='generated/')
        >>> # Creates: generated/SubController.py, generated/MyController.py
    """
    translator = RecursiveTranslator(search_paths)
    return translator.translate_file(cxf_path, output_dir)


# Keep old name for backward compatibility
def translate_cxf_recursive(
    cxf_path: Path,
    output_dir: Optional[Path] = None,
    search_paths: Optional[List[Path]] = None
) -> Dict[str, str]:
    """Deprecated: Use translate_cxf() instead

    This function is kept for backward compatibility.
    """
    return translate_cxf(cxf_path, output_dir, search_paths)
