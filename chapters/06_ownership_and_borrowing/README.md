# Chapter 06: Ownership & Borrowing

One of Mojo's most powerful systems programming advantages is its ownership and lifetime system.

## Argument Conventions
Mojo functions can receive parameters through explicit conventions:
1. **Default (Immutable Borrow)**: Receives a read-only reference to the caller's data. Zero copies.
2. **`mut` (Mutable Borrow)**: Receives an exclusive mutable reference. The function can mutate the caller's variable in place.
3. **`var` (Owned Value)**: The function takes ownership of the argument.
4. **`out` (Uninitialized Output)**: Used primarily for struct initializers (`__init__`).

## The Transfer Operator (`^`)
The transfer operator (`^`) transfers ownership of an existing variable to a callee, moving it rather than copying the heap buffer:
```mojo
var payload = String("Payload data")
consume(payload^)  # Payload is moved without a copy
```

## Running this Chapter
```bash
uv run mojo chapters/06_ownership_and_borrowing/ownership.mojo
```
