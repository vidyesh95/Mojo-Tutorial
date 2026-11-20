# Chapter 03: Data Types

Mojo features a rich, statically checked type system backed by MLIR and LLVM.

## Primitive Types
- `Int`: Platform-native signed integer (64-bit on 64-bit architectures).
- `Int8`, `Int16`, `Int32`, `Int64`: Fixed-width signed integers.
- `UInt8`, `UInt16`, `UInt32`, `UInt64`: Fixed-width unsigned integers.
- `Float32`, `Float64`: IEEE 754 floating point numbers.
- `Bool`: Standard boolean (`True` or `False`).
- `String`: Dynamically-sized UTF-8 text string.

## Heterogeneous Tuples
Tuples group fixed-size collections of potentially different types without heap allocation:
```mojo
var session = (1, "user@domain.com", True)
print(session[0], session[1])
```

## Running this Chapter
```bash
uv run mojo chapters/03_datatypes/datatypes.mojo
```
