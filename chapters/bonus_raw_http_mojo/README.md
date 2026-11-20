# Bonus Lab: Raw Socket TCP HTTP Server in Mojo

This bonus chapter is an **educational systems programming lab** illustrating how network sockets and HTTP protocol framing operate under the hood.

## Why Separate This From Production?
- **Low-level TCP framing**: Demonstrates socket binding, TCP handshakes, receiving byte buffers, parsing HTTP request lines, and formatting `HTTP/1.1 200 OK` headers.
- **Production Tradeoff**: While writing raw socket servers in Mojo is great for systems education, production web backends delegate HTTP connection pools, TLS termination, async coroutines, and WebSocket handling to ASGI frameworks (FastAPI/Uvicorn), while delegating heavy math and SIMD computing to compiled Mojo extensions.

## Running the Lab
1. Start the server:
   ```bash
   uv run mojo chapters/bonus_raw_http_mojo/server.mojo
   ```
2. In another terminal, make a request:
   ```bash
   curl -i http://127.0.0.1:8090/health
   ```
