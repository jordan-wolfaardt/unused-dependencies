# Unused Dependencies

Unused Dependencies is a Python package that identifies unused dependencies in your Python projects managed with Poetry. The package scans through all the project files and compares imports with the dependencies listed in your `pyproject.toml` file. Any dependencies that are not used in your project are then printed as output.

This tool can be incredibly useful when trying to declutter your Python projects, minimize your project's footprint, and improve loading times.

## How to Use

Currently this repository has to be cloned and then run directly in your project. Next steps will be to turn this into a package downloadable from PyPI.

1. Clone the repository:
   ```
   git clone https://github.com/<username>/unused_dependencies.git
   ```

2. Navigate to the project directory:
   ```
   cd unused_dependencies
   ```

3. Run the script within your project root:
   ```
   python main.py
   ```

## Limitations

1. **Indirect Imports:** If a package A is imported and used in your code, and A internally depends on package B, but B is also listed in your project's dependencies, removing B will break A. The script will not be able to detect this kind of dependency.

2. **Optional Imports:** Dependencies that are optionally imported with a try-except block may not be correctly identified. For instance, if you have code like this in your project:
   ```python
   try:
       import optional_dependency
   except ImportError:
       optional_dependency = None
   ```
   In this case, if `optional_dependency` is not actually used in your project, Unused Dependencies may not correctly identify it as unused.

3. **Dynamic Imports:** Python allows dynamic imports using the __import__ function or importlib.import_module. If your code is using this kind of imports, these will not be picked up by the script.

4. **Non-Poetry Projects:** Unused Dependencies currently only works with Python projects managed with Poetry. Other project configurations are not supported.

5. **Command-Line Scripts:** If a package is only used in a command-line script, or in other code that isn't directly imported by the main project, it may be marked as unused.

6. **Packages Imported for Side Effects:** Some packages when imported might execute some code that affects the runtime, but their functions or classes are never directly used. These packages could also be marked as unused.

## Running Unit Tests

To run the tests, you can use the following command:

```
pytest test
```

## Type Checking and Linting

To run mypy, black, and flake8, you can use the following commands:

```
mypy .
black .
flake8
```

Please ensure that mypy, black, and flake8 are installed in your environment before running these commands.

## Future Improvements

1. Support for detecting unused indirect and optional dependencies.
2. Ability to work with other project configurations and not just Poetry.
3. More comprehensive testing.
4. Make downloadable package from PyPI.

Please feel free to contribute to Unused Dependencies or raise issues for any bugs or feature requests.

## License

This project is licensed under the terms of the MIT license.
