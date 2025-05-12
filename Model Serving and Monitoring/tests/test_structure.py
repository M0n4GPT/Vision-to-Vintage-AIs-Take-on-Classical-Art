import os
import pytest
from pathlib import Path

def test_project_structure():
    """Test that the project has the correct structure"""
    base_dir = Path(__file__).parent.parent
    
    # Required directories
    required_dirs = [
        base_dir / "app" / "core" / "models",
        base_dir / "app" / "core" / "monitoring",
        base_dir / "app" / "core" / "utils",
        base_dir / "app" / "api",
        base_dir / "app" / "api" / "config" / "docker",
        base_dir / "app" / "api" / "config" / "kubernetes",
        base_dir / "data" / "styles",
        base_dir / "data" / "metrics",
        base_dir / "data" / "reference",
        base_dir / "scripts",
        base_dir / "tests"
    ]
    
    # Check all required directories exist
    for dir_path in required_dirs:
        assert dir_path.exists(), f"Directory {dir_path} does not exist"
        assert dir_path.is_dir(), f"{dir_path} is not a directory"
    
    # Check for required files
    required_files = [
        base_dir / "requirements.txt",
        base_dir / "README.md",
        base_dir / ".gitignore"
    ]
    
    for file_path in required_files:
        assert file_path.exists(), f"File {file_path} does not exist"
        assert file_path.is_file(), f"{file_path} is not a file"
    
    # Check for empty directories
    for dir_path in required_dirs:
        if not any(dir_path.iterdir()):
            pytest.fail(f"Directory {dir_path} is empty")
    
    # Check for redundant directories
    redundant_dirs = [
        base_dir / "serving",
        base_dir / "uploads",
        base_dir / "mlruns"
    ]
    
    for dir_path in redundant_dirs:
        assert not dir_path.exists(), f"Redundant directory {dir_path} exists" 