# chapters/bonus_raw_http_mojo/server.mojo
# Educational Systems Lab: Raw Socket TCP HTTP Server in Mojo

from std.python import Python

def main() raises:
    var py_socket = Python.import_module("socket")
    var server = py_socket.socket(py_socket.AF_INET, py_socket.SOCK_STREAM)
    server.setsockopt(py_socket.SOL_SOCKET, py_socket.SO_REUSEADDR, 1)

    var host_port = Python.evaluate("('127.0.0.1', 8090)")
    server.bind(host_port)
    server.listen(5)
    print("🔥 Pure-Mojo Raw TCP HTTP Server listening at http://127.0.0.1:8090")
    print("   Test with: curl -i http://127.0.0.1:8090/health")
    print("   (Listening for 1 request then exiting cleanly)")

    # Accept single incoming connection to demonstrate TCP socket framing
    var conn_tuple = server.accept()
    var client_sock = conn_tuple[0]
    var client_addr = conn_tuple[1]
    print("Accepted incoming connection from:", client_addr)

    var raw_request = client_sock.recv(4096)
    var request_str = String(raw_request.decode("utf-8"))
    print("Received HTTP request line:", request_str.split("\r\n")[0])

    var json_body = '{"status":"ok","engine":"pure-mojo-raw-socket","timestamp":"2026-11-20"}'
    var body_len = len(json_body)

    var response = String(
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: " + String(body_len) + "\r\n"
        "Connection: close\r\n"
        "\r\n" + json_body
    )

    client_sock.sendall(response.encode("utf-8"))
    client_sock.close()
    server.close()
    print("HTTP response sent and socket cleanly closed.")
