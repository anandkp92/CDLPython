"""CXF file resolver for custom block lookup

This module provides utilities to find CXF files for custom blocks.
"""

from pathlib import Path
from typing import Optional, List


class CXFResolver:
    """Resolves CXF file paths for custom blocks"""

    def __init__(self, search_paths: Optional[List[Path]] = None):
        """Initialize resolver with optional search paths

        Args:
            search_paths: Additional directories to search for CXF files
        """
        self.search_paths = search_paths or []

    def resolve(self, block_name: str, base_dir: Path) -> Optional[Path]:
        """Find CXF file for a custom block

        Searches in the following order:
        1. base_dir/{block_name}.jsonld
        2. base_dir/{block_name}.json
        3. Recursively in base_dir tree
        4. Additional search paths (recursively)

        Args:
            block_name: Simple name of the custom block (e.g., "SubController")
            base_dir: Directory of the file that references this block

        Returns:
            Path to CXF file if found, None otherwise
        """
        # Normalize base directory
        base_dir = Path(base_dir).resolve()

        # Try different file extensions
        extensions = ['.jsonld', '.json']

        # Search in base directory first (fast path)
        for ext in extensions:
            candidate = base_dir / f"{block_name}{ext}"
            if candidate.exists():
                return candidate

        # Search recursively in base directory tree
        # Start from the CXF root (find the top-level 'cxf' directory)
        cxf_root = self._find_cxf_root(base_dir)
        if cxf_root:
            result = self._recursive_search(block_name, cxf_root, extensions)
            if result:
                return result

        # Search in additional search paths (recursively)
        for search_path in self.search_paths:
            search_path = Path(search_path).resolve()
            result = self._recursive_search(block_name, search_path, extensions)
            if result:
                return result

        return None

    def _find_cxf_root(self, path: Path) -> Optional[Path]:
        """Find the root CXF directory by walking up the tree

        Args:
            path: Starting directory

        Returns:
            Path to CXF root directory, or None if not found
        """
        current = path
        while current.parent != current:  # Stop at filesystem root
            if current.name == 'cxf':
                return current
            current = current.parent
        return None

    def _recursive_search(self, block_name: str, root: Path, extensions: List[str]) -> Optional[Path]:
        """Recursively search for a block in a directory tree

        Args:
            block_name: Block name to search for
            root: Root directory to search from
            extensions: File extensions to try

        Returns:
            Path to CXF file if found, None otherwise
        """
        # Use glob to search recursively for matching files
        for ext in extensions:
            pattern = f"**/{block_name}{ext}"
            matches = list(root.glob(pattern))
            if matches:
                # Return the first match
                return matches[0]
        return None

    def add_search_path(self, path: Path):
        """Add a directory to the search paths

        Args:
            path: Directory to add to search paths
        """
        path = Path(path).resolve()
        if path.is_dir() and path not in self.search_paths:
            self.search_paths.append(path)
