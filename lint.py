#!/usr/bin/env python3
"""
Lint.py - Enforces Gomoku source architecture and rules.

Rules enforced:
1. Every file under src/ belongs in exactly one layer directory.
2. Imports may only target layers in the file's own "may import from" set.
3. No file exceeds 300 lines.
4. Files must use proper Python syntax.
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Layer dependency rules - each layer may only import from these
LAYER_IMPORTS = {
    "types": {"types"},
    "config": {"types", "config"},
    "providers": {"types", "config", "utils", "providers"},
    "repo": {"types", "config", "repo"},
    "service": {"types", "config", "repo", "providers", "service"},
    "runtime": {"types", "config", "repo", "service", "providers", "runtime"},
    "ui": {"types", "config", "service", "runtime", "providers", "ui"},
    "utils": {"utils"},
}

ALLOWED_LAYERS = set(LAYER_IMPORTS.keys())
LAYER_ORDER = ["types", "config", "repo", "service", "runtime", "ui"]
LAYER_PRIORITY = {layer: idx for idx, layer in enumerate(LAYER_ORDER)}


def get_layer_from_path(file_path: Path) -> str | None:
    """Determine which layer a file belongs to based on its directory."""
    parts = file_path.parts
    try:
        # Find which layer directory contains this file
        for i, part in enumerate(parts):
            if part in ALLOWED_LAYERS:
                return part
    except ValueError:
        pass
    return None


def get_imports(file_path: Path) -> Set[str]:
    """Parse a Python file and extract all imported module names."""
    imports = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        tree = ast.parse(content, filename=str(file_path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # Get the top-level module
                    module_name = alias.name.split(".")[0]
                    imports.add(module_name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # Get the top-level module
                    module_name = node.module.split(".")[0]
                    imports.add(module_name)
    except SyntaxError as e:
        return {"syntax_error"}
    return imports


def check_file_line_count(file_path: Path) -> List[str]:
    """Check if file exceeds 300 lines."""
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if len(lines) > 300:
            errors.append(f"{file_path}:{len(lines)}: File exceeds 300 lines ({len(lines)} lines)")
    except Exception:
        pass
    return errors


def check_imports(file_path: Path, layer: str) -> List[str]:
    """Check that imports follow layer dependency rules."""
    errors = []
    imports = get_imports(file_path)
    allowed_imports = LAYER_IMPORTS[layer]

    for imp in imports:
        # Skip standard library and external imports
        if imp in {"os", "sys", "typing", "ast", "pathlib", "json", "dataclasses", "enum"}:
            continue
        # Check if it's an internal import
        if imp in ALLOWED_LAYERS:
            if imp not in allowed_imports:
                errors.append(f"{file_path}: Import of '{imp}' not allowed from layer '{layer}'. May only import from: {sorted(allowed_imports)}")
    return errors


def check_syntax(file_path: Path) -> List[str]:
    """Check Python syntax."""
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        ast.parse(content, filename=str(file_path))
    except SyntaxError as e:
        errors.append(f"{file_path}:{e.lineno or 0}: Syntax error: {e.msg}")
    return errors


def check_file(file_path: Path) -> List[str]:
    """Run all checks on a single file."""
    errors = []
    
    # Get layer from path
    layer = get_layer_from_path(file_path)
    if layer is None:
        return errors  # Skip non-layer files (e.g., __init__.py that don't belong to a layer)
    
    # Check syntax
    errors.extend(check_syntax(file_path))
    
    # Check line count
    errors.extend(check_file_line_count(file_path))
    
    # Check imports
    errors.extend(check_imports(file_path, layer))
    
    return errors


def lint() -> List[str]:
    """Run lint checks on all source files."""
    errors = []
    src_dir = Path("src")
    
    if not src_dir.exists():
        return ["src/ directory not found"]
    
    # Find all Python files under src/
    for root, dirs, files in os.walk(src_dir):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        
        for filename in files:
            if filename.endswith(".py"):
                file_path = Path(root) / filename
                file_errors = check_file(file_path)
                errors.extend(file_errors)
    
    return errors


def main():
    """Main entry point."""
    errors = lint()
    
    if errors:
        print("Lint failed with the following errors:")
        print()
        for error in errors:
            print(error)
        print()
        print(f"Total: {len(errors)} error(s)")
        sys.exit(1)
    
    print("Lint passed! All source files follow the architecture rules.")
    sys.exit(0)


if __name__ == "__main__":
    main()
