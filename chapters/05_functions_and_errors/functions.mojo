# 05_functions_and_errors: Function Signatures & Error Propagation

def calculate_discount(price: Float64, discount_pct: Float64 = 10.0) -> Float64:
    return price * (1.0 - discount_pct / 100.0)

def validate_positive_amount(amount: Float64) raises -> Float64:
    if amount <= 0.0:
        raise Error("Amount must be strictly positive")
    return amount

def main() raises:
    # 1. Calling standard functions with default arguments
    var original_price: Float64 = 120.0
    var discounted = calculate_discount(original_price)
    print("Original:", original_price, "-> Discounted (10%):", discounted)

    # 2. Structured error handling with try ... except
    try:
        var valid = validate_positive_amount(50.0)
        print("Validated amount:", valid)
        
        # This will trigger an error
        var invalid = validate_positive_amount(-15.0)
        print("Invalid amount (unreachable):", invalid)
    except e:
        print("Caught expected validation error:", e)
