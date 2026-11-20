# Modern Mojo Tutorial 🔥: From Language Basics to Production Backend

A complete, beginner-friendly curriculum taking you from **modern Mojo (v1.2+)** fundamentals to building a production-grade backend combining **FastAPI**, **SQLx-style SQLite persistence**, and **Better Auth-compatible authentication**.

Managed with **Astral's [uv](https://astral.sh/uv)** package manager for instant, reproducible setup.

---

## ⚡ What Changed Since the Alpha Era?

If you learned Mojo during its early Alpha releases, modern Mojo has matured into a stable systems language with key syntax unifications:

| Feature | Alpha Era (Old) | Modern Mojo (v1.2+) | Why It Changed |
| :--- | :--- | :--- | :--- |
| **Package Management** | `modular` CLI / conda | `uv` / PyPI (`uv add mojo`) | Standardized under Python's fastest package ecosystem |
| **Functions** | `fn` (strict) vs `def` (loose) | **Unified `def`** | Eliminated dual-keyword fragmentation; `def` has full systems safety |
| **Variables** | `var` (mut) vs `let` (immut) | **Unified `var`** | Simplified runtime variables; compile-time constants use `comptime` |
| **Compile-Time** | `alias` | **`comptime`** | Clearer meta-programming semantics (`comptime X = 10`, `if comptime(...)`) |
| **Standard Library** | `from collections import List` | `from std.collections import List` | Standardized under the `std` root namespace |
| **Backend Architecture** | Raw sockets inside Mojo | **Compiled `.so` in FastAPI** | FastAPI handles async ASGI HTTP; Mojo handles SIMD/heavy compute |

---

## 🚀 Quickstart & Setup

### Prerequisites
- **macOS (Apple Silicon)** or **Linux**: Supported natively out of the box.
- **Python**: **Python 3.15** (managed automatically via `uv` or system Python 3.15).
- **Windows**: Install and run via **WSL2** (`wsl --install -d Ubuntu`).
- **uv**: If not installed, get it via `curl -LsSf https://astral.sh/uv/install.sh | sh` or `brew install uv`.

### Installation
Clone the repository and install all dependencies in one command:
```bash
git clone https://github.com/vinitchuri/Mojo-Tutorial.git
cd Mojo-Tutorial
uv sync
```

Verify your Mojo compiler installation:
```bash
uv run mojo --version
# Output: Mojo 1.2.0 (2016d0cd)
```

---

## 📚 Curriculum Map

### Phase 1: Core Mojo Fundamentals
- [**Chapter 01: Hello, Mojo!**](chapters/01_hello/README.md)
  The modern entry point (`def main():`), running scripts with `uv run mojo`, and compiling native binaries with `mojo build`.
- [**Chapter 02: Variables & Compile-Time Constants**](chapters/02_variables_and_comptime/README.md)
  Runtime mutable variables (`var`), type inference, and compile-time constants (`comptime`).
- [**Chapter 03: Data Types & Tuples**](chapters/03_datatypes/README.md)
  Primitive scalar types (`Int`, `Float64`, `Bool`, `String`) and heterogeneous tuples.
- [**Chapter 04: Control Flow**](chapters/04_control_flow/README.md)
  Conditionals (`if`/`elif`/`else`), loops over ranges, loop controls, and compile-time branching with `if comptime(...)`.

### Phase 2: Systems Mojo & Performance
- [**Chapter 05: Functions & Error Handling**](chapters/05_functions_and_errors/README.md)
  Typed function signatures, default arguments, error propagation with `raises`, and structured `try ... except` blocks.
- [**Chapter 06: Ownership & Borrowing Conventions**](chapters/06_ownership_and_borrowing/README.md)
  Argument conventions (`read`, `mut`, `var`, `out`), zero-cost borrowing, and the transfer operator (`^`) for moving buffers.
- [**Chapter 07: Collections & Zero-Cost Structs**](chapters/07_collections_and_structs/README.md)
  Homogeneous `List[T]`, Swiss-table `Dict[Key, Value]`, and building value `struct` models.
- [**Chapter 08: Traits, Generics & SIMD Vectorization**](chapters/08_traits_generics_and_simd/README.md)
  Polymorphic interfaces (`trait`), compile-time monomorphized generics, and hardware SIMD registers (`SIMD[DType.float32, 4]`).

### Phase 3: Integration & Extensions
- [**Chapter 09: Native Mojo Python Extensions**](chapters/09_mojo_python_extensions/README.md)
  Calling Python from Mojo, and compiling Mojo into a native CPython shared library (`.so`) using `PythonModuleBuilder` and `@export abi("C")`.
- [**Bonus Systems Lab: Raw TCP Socket HTTP Server**](chapters/bonus_raw_http_mojo/README.md)
  An educational systems lab implementing TCP socket accept loops, HTTP byte framing, and JSON response formatting directly in Mojo.

### Phase 4–6: Production Backend (`backend/`)
- [**Chapter 10: SQLx-Style Persistence with SQLite**](backend/README.md#sqlx-philosophy-with-sqlite-aiosqlite)
  Raw parameterized `.sql` queries, versioned sequential migrations, and a pre-flight SQL query verifier using `EXPLAIN` to catch schema mismatches before deployment.
- [**Chapter 11: Better Auth-Compatible Authentication**](backend/README.md#better-auth-specification)
  Exact 4-table schema (`user`, `session`, `account`, `verification`), **Argon2id** password hashing (`argon2-cffi`), and HMAC-SHA256 signed `HttpOnly; SameSite=Lax` session cookies.
- [**Chapter 12: Production FastAPI Capstone API**](backend/README.md#quickstart)
  Connecting everything together into a production REST API: protected endpoints, dependency injection guards (`CurrentUser`), and async dispatch of compute-heavy SIMD scoring to native compiled Mojo code.

---

## 🛠️ Verification & Test Suite

### 1. Run All Chapter Scripts
You can execute every tutorial chapter in sequence:
```bash
uv run mojo chapters/01_hello/hello.mojo
uv run mojo chapters/02_variables_and_comptime/variables.mojo
uv run mojo chapters/03_datatypes/datatypes.mojo
uv run mojo chapters/04_control_flow/control_flow.mojo
uv run mojo chapters/05_functions_and_errors/functions.mojo
uv run mojo chapters/06_ownership_and_borrowing/ownership.mojo
uv run mojo chapters/07_collections_and_structs/structs.mojo
uv run mojo chapters/08_traits_generics_and_simd/simd_compute.mojo
uv run mojo chapters/09_mojo_python_extensions/interop_demo.mojo
```

### 2. Test Chapter 09 Native Extension Compilation
```bash
uv run python chapters/09_mojo_python_extensions/run_extension.py
```

### 3. Run Pre-Flight SQLx Verifier & Backend Pytest Suite
```bash
uv run python -m backend.app.db.migrator
uv run python -m backend.app.db.verifier
uv run pytest backend/tests/ -v
```

### 4. Code Formatting & Static Type Checking
```bash
# Format and lint with Ruff
uv run ruff format .
uv run ruff check .

# Fast static type checking with Pyrefly
uv run pyrefly check
```

---

## 🤝 Contributing & License
Contributions, feedback, and questions are welcome! Feel free to open an issue or submit a pull request.
Licensed under the [Apache 2.0 License](LICENSE).
