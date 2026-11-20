# chapters/09_mojo_python_extensions/run_extension.py
"""Test script that builds and invokes the compiled Mojo Python extension."""

import os
import subprocess
import sys


def main():
    mojo_file = "chapters/09_mojo_python_extensions/export_extension.mojo"
    so_file = "chapters/09_mojo_python_extensions/export_extension.so"

    print(f"1. Compiling {mojo_file} into native shared library {so_file}...")
    # Locate mojo binary in current venv or system
    venv_bin = os.path.dirname(sys.executable)
    mojo_bin = os.path.join(venv_bin, "mojo")
    if not os.path.exists(mojo_bin):
        mojo_bin = "mojo"

    compile_cmd = [mojo_bin, "build", "--emit", "shared-lib", mojo_file, "-o", so_file]
    subprocess.run(compile_cmd, check=True)
    print("   Compilation successful!")

    print("2. Importing compiled extension into Python runtime...")
    sys.path.insert(0, os.path.dirname(os.path.abspath(so_file)))
    import export_extension  # pyrefly: ignore[missing-import]

    print("3. Executing Mojo functions:")
    print("   export_extension.ping() ->", export_extension.ping())
    res = export_extension.compute_sum_squares(1000)
    print("   export_extension.compute_sum_squares(1000) ->", res)
    assert res == sum(i * i for i in range(1000))
    print("   Validation check PASSED!")


if __name__ == "__main__":
    main()
