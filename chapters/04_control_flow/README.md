# Chapter 04: Control Flow

This chapter covers conditionals, iterative loops, and Mojo's compile-time branching.

## Conditionals
Mojo uses standard Python-like indentation for `if`, `elif`, and `else` blocks:
```mojo
if score > 80:
    print("Low Risk")
else:
    print("High Risk")
```

## Loops & Ranges
`for` loops iterate over numeric ranges or collections:
```mojo
for i in range(10):
    print(i)
```

## Compile-Time Branching (`if comptime(...)`)
Mojo evaluates compile-time branches and strips unreachable branches from the compiled machine code:
```mojo
comptime DEBUG_MODE = False

if comptime(DEBUG_MODE):
    print("Verbose debug tracing...")
```

## Running this Chapter
```bash
uv run mojo chapters/04_control_flow/control_flow.mojo
```
