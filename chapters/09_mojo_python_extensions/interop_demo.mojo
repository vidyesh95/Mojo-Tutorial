# chapters/09_mojo_python_extensions/interop_demo.mojo
# Direction 1: Calling Python from Mojo

from std.python import Python

def main() raises:
    # 1. Import Python standard library modules
    var py_math = Python.import_module("math")
    var py_json = Python.import_module("json")

    # 2. Execute Python calculations
    var sqrt_val = py_math.sqrt(256)
    print("Python math.sqrt(256) called from Mojo:", sqrt_val)

    # 3. Parse JSON strings using Python inside Mojo
    var raw_json = '{"service": "fastapi-backend", "engine": "mojo", "status": "active"}'
    var parsed_dict = py_json.loads(raw_json)
    print("Parsed JSON dict service field:", parsed_dict["service"])
