# 03_datatypes: Primitive Types & Tuples

def main():
    # Integer scalar types
    var standard_int: Int = 42
    var small_int: Int32 = 100
    var big_int: Int64 = 9_000_000_000

    # Floating point types
    var float_single: Float32 = 3.14159
    var float_double: Float64 = 2.718281828459

    # Boolean and String
    var is_active: Bool = True
    var service_name: String = "better-auth-service"

    print("Integers:", standard_int, small_int, big_int)
    print("Floats:", float_single, float_double)
    print("Bool & String:", is_active, service_name)

    # Heterogeneous Tuples
    var session_pair = (101, "admin@example.com", True)
    print("Tuple user_id:", session_pair[0])
    print("Tuple email:", session_pair[1])
    print("Tuple is_verified:", session_pair[2])
