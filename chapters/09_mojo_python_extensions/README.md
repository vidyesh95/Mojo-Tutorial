# Chapter 09: Native Mojo Python Extensions

This chapter bridges systems Mojo with modern Python/FastAPI backends.

## The Two Interoperability Directions

### Direction 1: Calling Python from Mojo (`interop_demo.mojo`)
Use `from std.python import Python` for rapid prototyping or scripts requiring Python libraries:
```bash
uv run mojo chapters/09_mojo_python_extensions/interop_demo.mojo
```

### Direction 2: Compiling Mojo into a Native Python Shared Library (`export_extension.mojo`)
This is the **production architecture pattern**:
1. Implement heavy numeric, algorithmic, or SIMD routines in Mojo.
2. Expose the CPython initialization hook `@export def PyInit_<module_name>() abi("C")` using `PythonModuleBuilder`.
3. Compile with `mojo build --emit shared-lib`:
   ```bash
   uv run mojo build --emit shared-lib chapters/09_mojo_python_extensions/export_extension.mojo -o chapters/09_mojo_python_extensions/export_extension.so
   ```
4. Import directly into standard Python (or FastAPI) without subprocesses or socket overhead:
   ```python
   import export_extension
   print(export_extension.ping())
   ```

## Running the Automated Test
```bash
uv run python chapters/09_mojo_python_extensions/run_extension.py
```
