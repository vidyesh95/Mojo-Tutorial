# Chapter 01: Hello, Mojo!

Welcome to Mojo! This chapter introduces modern Mojo syntax and the `uv` toolchain workflow.

## Key Changes from Alpha Era
- **Unified Function Keyword**: In Alpha versions of Mojo, `fn` declared strict, statically typed functions, while `def` was dynamic. In Mojo v1.2+, `fn` has been removed and all functions use `def` with full systems capabilities.
- **Modern Package Tooling**: Mojo is now managed via `uv`, Astral's fast Python and package manager.

## Running the Code
Execute the script directly within your project's managed environment:
```bash
uv run mojo chapters/01_hello/hello.mojo
```

## Compiling a Standalone Binary
Mojo compiles directly to native machine code with zero external runtime overhead:
```bash
uv run mojo build chapters/01_hello/hello.mojo -o chapters/01_hello/hello_bin
./chapters/01_hello/hello_bin
```

## What's Next?
Head over to [Chapter 02: Variables & Compile-time Constants](../02_variables_and_comptime/README.md) to learn about mutability and compile-time evaluations.
