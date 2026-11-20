# 06_ownership_and_borrowing: Memory Conventions & Transfer Operator

# 1. Default convention: Immutable reference (read)
def print_record(record_name: String):
    print("Reading record (immutable borrow):", record_name)

# 2. 'mut' convention: Mutable reference
def increment_counter(mut counter: Int):
    counter += 1

# 3. 'var' convention: Takes ownership of the value
def consume_buffer(var buffer: String):
    buffer += " [PROCESSED]"
    print("Consumed in owned function:", buffer)

def main():
    var project = String("Mojo Backend Framework")
    print_record(project)

    var count: Int = 100
    increment_counter(count)
    print("Mutated count:", count)

    # 4. Transfer Operator (^)
    # Moves the memory buffer into 'consume_buffer' without copying the underlying heap data
    var big_payload = String("High-Throughput In-Memory Buffer")
    consume_buffer(big_payload^)
    print("Buffer was moved with ^ to eliminate allocation overhead.")
