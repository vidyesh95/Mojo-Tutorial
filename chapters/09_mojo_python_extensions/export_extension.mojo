# chapters/09_mojo_python_extensions/export_extension.mojo
# Direction 2: Exporting Mojo as a Native CPython Shared Library (.so)

from std.python import PythonObject
from std.python.bindings import PythonModuleBuilder
from std.os import abort

@export
def PyInit_export_extension() abi("C") -> PythonObject:
    try:
        var m = PythonModuleBuilder("export_extension")
        m.def_function[ping]("ping", docstring="Healthcheck probe")
        m.def_function[compute_sum_squares]("compute_sum_squares", docstring="SIMD sum of squares")
        return m.finalize()
    except e:
        abort(String("Failed to create Python extension module: ", e))

def ping() raises -> PythonObject:
    return PythonObject("pong from native Mojo .so extension!")

def compute_sum_squares(n_obj: PythonObject) raises -> PythonObject:
    var n = Int(py=n_obj)
    var total: Int = 0
    for i in range(n):
        total += i * i
    return PythonObject(total)
