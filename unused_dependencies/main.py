import ast
import os
from pathlib import Path
from typing import Generator, Set

import toml


def get_imports(filepath: str) -> Generator[str, None, None]:
    with open(filepath, "r") as file:
        root = ast.parse(file.read())

    for node in ast.walk(root):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.asname if alias.asname else alias.name.split(".")[0]
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module is not None:
                yield node.module.split(".")[0]


def get_all_python_files(path: str) -> Generator[Path, None, None]:
    return Path(path).rglob("*.py")


def get_poetry_deps(path: str) -> Set[str]:
    pyproject_toml_path = os.path.join(path, "pyproject.toml")
    with open(pyproject_toml_path, "r") as file:
        pyproject = toml.load(file)

    dependencies = set(pyproject["tool"]["poetry"]["dependencies"].keys())
    # Exclude 'python' as it's always listed as a dependency, but not used as a module
    dependencies.discard("python")
    return dependencies


def main() -> None:
    project_path = os.getcwd()
    all_imports: set[str] = set()

    for python_file in get_all_python_files(project_path):
        all_imports.update(get_imports(str(python_file)))

    poetry_deps = get_poetry_deps(project_path)
    unused_deps = poetry_deps - all_imports

    if unused_deps:
        print("Unused dependencies:")
        for dep in unused_deps:
            print(dep)
    else:
        print("No unused dependencies found.")


if __name__ == "__main__":
    main()
