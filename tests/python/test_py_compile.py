# sonar-ignore-file
# pragma: no cover
import py_compile
import sys
import warnings
from pathlib import Path

try:
    import pytest

    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False


def find_project_root(target_folder="rinexpos"):
    """Find the project root by looking for target folder name."""
    current = Path.cwd()

    # Check if we're already in the target folder
    if current.name == target_folder:
        return current

    # Look up the directory tree for the target folder
    for parent in current.parents:
        if parent.name == target_folder:
            return parent

    # If not found, check if target folder exists as a subdirectory
    for path in current.rglob(target_folder):
        if path.is_dir():
            return path

    # Fallback to current working directory
    return current


def get_python_files():
    python_files = []

    # Find project root dynamically
    project_root = find_project_root()

    print(f"Scanning from: {project_root}")

    for py_file in project_root.rglob("*.py"):
        # Skip cache and build directories
        if any(skip in str(py_file) for skip in ["__pycache__", "build", "dist"]):
            continue
        python_files.append(py_file)

    return python_files


def check_syntax():
    """Main syntax checking function that works for both pytest and standalone."""
    python_files = get_python_files()
    errors = []

    print(f"Checking syntax for {len(python_files)} Python files...")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        for py_file in python_files:
            try:
                py_compile.compile(str(py_file), doraise=True)
            except py_compile.PyCompileError as e:
                errors.append(f"{py_file}: {e}")

    if errors:
        print(f"\n❌ Found {len(errors)} files with syntax errors:")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print(f"✅ All {len(python_files)} Python files passed syntax check")
        return True


def test_python_syntax():
    """Pytest test function."""
    if not check_syntax():
        if HAS_PYTEST:
            pytest.fail("Python syntax errors found")
        else:
            raise AssertionError("Python syntax errors found")


if __name__ == "__main__":
    # Run as standalone script
    success = check_syntax()
    sys.exit(0 if success else 1)
