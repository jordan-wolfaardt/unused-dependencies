from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from unused_dependencies.main import get_all_python_files, get_imports, get_poetry_deps, main


# To test the get_poetry_deps function
def test_get_poetry_deps(tmp_path: Path) -> None:
    test_toml = tmp_path / "pyproject.toml"
    test_toml.write_text(
        """
    [tool.poetry.dependencies]
    requests = "*"
    numpy = "*"
    """
    )

    assert get_poetry_deps(str(tmp_path)) == {"requests", "numpy"}


# To test the get_imports function
def test_get_imports(tmp_path: Path) -> None:
    test_py = tmp_path / "test.py"
    test_py.write_text("import requests\nfrom os import path")

    assert set(get_imports(str(test_py))) == {"requests", "os"}


# To test the get_all_python_files function
def test_get_all_python_files(tmp_path: Path) -> None:
    test_py1 = tmp_path / "test1.py"
    test_py2 = tmp_path / "test2.py"
    test_py1.touch()
    test_py2.touch()

    assert set(get_all_python_files(str(tmp_path))) == {test_py1, test_py2}


# To test the main function, mocking the functions get_poetry_deps, get_all_python_files and get_imports
@patch("unused_dependencies.main.get_poetry_deps")
@patch("unused_dependencies.main.get_all_python_files")
@patch("unused_dependencies.main.get_imports")
def test_main(
    mock_get_imports: Mock,
    mock_get_all_python_files: Mock,
    mock_get_poetry_deps: Mock,
    capsys: pytest.CaptureFixture,
) -> None:
    mock_get_poetry_deps.return_value = {"requests", "numpy"}
    mock_get_all_python_files.return_value = ["file1.py", "file2.py"]
    mock_get_imports.return_value = ["requests"]

    main()
    captured = capsys.readouterr()
    assert "numpy" in captured.out
