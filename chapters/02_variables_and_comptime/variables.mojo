# 02_variables_and_comptime: Mutability & Compile-time Constants

def main():
    # 1. Variables are declared with 'var' and are mutable by default
    var counter: Int = 10
    counter += 5
    print("Mutable counter:", counter)

    # 2. Type inference automatically detects primitive types
    var greeting = "Mojo delivers C-level performance"
    print("Greeting:", greeting)

    # 3. In Mojo v1.2+, 'let' and 'alias' were replaced by 'comptime'
    # For compile-time evaluation and constants, use 'comptime':
    comptime MAX_BUFFER_SIZE = 4096
    comptime PLATFORM_TAG = "mojo-arm64"
    print("Buffer limit (comptime):", MAX_BUFFER_SIZE)
    print("Platform tag:", PLATFORM_TAG)
