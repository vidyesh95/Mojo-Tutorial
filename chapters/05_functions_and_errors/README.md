# Chapter 05: Functions & Error Handling

Mojo combines the ergonomics of Python function definitions with C++ type safety and explicit error propagation.

## Function Signatures
In modern Mojo, all functions are declared with `def`. You can specify parameter types, return types, and default arguments:
```mojo
def calculate_tax(amount: Float64, rate: Float64 = 0.08) -> Float64:
    return amount * rate
```

## Error Propagation (`raises`)
Functions that can fail must be annotated with `raises`. Any caller must handle the error with `try ... except` or propagate it:
```mojo
def parse_id(id_val: Int) raises -> Int:
    if id_val <= 0:
        raise Error("ID must be positive")
    return id_val
```

## Running this Chapter
```bash
uv run mojo chapters/05_functions_and_errors/functions.mojo
```
