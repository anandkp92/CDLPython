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
        3. Additional search paths

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

        # Search in base directory
        for ext in extensions:
            candidate = base_dir / f"{block_name}{ext}"
            if candidate.exists():
                return candidate

        # Search in additional search paths
        for search_path in self.search_paths:
            search_path = Path(search_path).resolve()
            for ext in extensions:
                candidate = search_path / f"{block_name}{ext}"
                if candidate.exists():
                    return candidate

        return None

    def add_search_path(self, path: Path):
        """Add a directory to the search paths

        Args:
            path: Directory to add to search paths
        """
        path = Path(path).resolve()
        if path.is_dir() and path not in self.search_paths:
            self.search_paths.append(path)
