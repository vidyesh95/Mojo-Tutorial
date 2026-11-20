# Chapter 02: Variables & Compile-Time Constants

Mojo gives you fine-grained control over runtime variables and compile-time expressions.

## Core Concepts

### 1. Runtime Variables (`var`)
All local runtime variables in modern Mojo are declared using `var`:
```mojo
var count: Int = 0
count += 1
```

### 2. Why Were `let` and `alias` Replaced?
During the Alpha era, `let` was used for immutable bindings and `alias` for constants. The modern Mojo design team consolidated these concepts:
- Mutable runtime state uses `var`.
- All compile-time constants and type expressions use `comptime`.

### 3. Compile-Time Constants (`comptime`)
`comptime` expressions are evaluated during compilation with zero runtime overhead:
```mojo
comptime DEFAULT_PORT = 8080
comptime SERVICE_NAME = "FastAPI-Mojo-Backend"
```

## Running this Chapter
```bash
uv run mojo chapters/02_variables_and_comptime/variables.mojo
```
