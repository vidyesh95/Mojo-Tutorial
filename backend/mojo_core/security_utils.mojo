# backend/mojo_core/security_utils.mojo
# Systems utilities: Constant-time string comparison for secure token validation

def constant_time_compare(a: String, b: String) -> Bool:
    """
    Performs constant-time byte comparison to prevent timing attacks
    on session tokens and HMAC signatures.
    """
    if a.byte_length() != b.byte_length():
        return False

    var diff: Int = 0
    for i in range(a.byte_length()):
        var byte_a = Int(ord(a[byte=i]))
        var byte_b = Int(ord(b[byte=i]))
        diff = diff | (byte_a ^ byte_b)

    return diff == 0

def main():
    var tok1 = "better-auth-session-token-secret-12345"
    var tok2 = "better-auth-session-token-secret-12345"
    var tok3 = "better-auth-session-token-secret-99999"

    print("Constant time comparison test:")
    print("  tok1 == tok2:", constant_time_compare(tok1, tok2))
    print("  tok1 == tok3:", constant_time_compare(tok1, tok3))
